
import asyncio
import os
import random
import time
from typing import List, Union, Dict, Callable

import anthropic
import httpx
import openai
from anthropic import AsyncAnthropic
from anthropic._types import NOT_GIVEN
from anthropic.types import Message
from openai import AsyncClient as AsyncGPTClient
from openai.types.chat import ChatCompletion

from lrc.exceptions import ChatBotException, LengthExceedException
from lrc.logger import logger
from lrc.utils import get_messages_token_number, get_text_token_number

model2chatbot = {
    'gpt-4-0125-preview': 'gptbot',
    'gpt-4-turbo-preview': 'gptbot',
    'gpt-3.5-turbo-0125': 'gptbot',
    'gpt-3.5-turbo': 'gptbot',

    'claude-3-opus-20240229': 'claudebot',
    'claude-3-sonnet-20240229': 'claudebot',
    'claude-3-haiku-20240307': 'claudebot'
}

chatbot_map = {}


def _register_chatbot(cls):
    chatbot_map[cls.__name__.lower()] = cls
    return cls


class ChatBot:
    def __init__(self, pricing, temperature=1, top_p=1, retry=8, max_async=16, fee_limit=0.05):
        self.pricing = pricing
        self._model = None

        self.temperature = temperature
        self.top_p = top_p
        self.retry = retry
        self.max_async = max_async
        self.fee_limit = fee_limit

        self.api_fees = []

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if model not in self.pricing:
            raise ValueError(f'Invalid model {model}.')
        self._model = model

    def estimate_fee(self, messages: List[Dict]):
        """
        Estimate the total fee for the given messages.
        """
        token_map = {'system': 0, 'user': 0, 'assistant': 0}
        for message in messages:
            token_map[message['role']] += get_text_token_number(message['content'])

        prompt_price, completion_price = self.pricing[self.model]

        total_price = (sum(token_map.values()) * prompt_price + token_map['user'] * completion_price * 2) / 1000000

        return total_price

    def update_fee(self, response):
        raise NotImplementedError()

    def get_content(self, response):
        raise NotImplementedError()

    async def _create_achat(self, messages: List[Dict], output_checker: Callable = lambda *args, **kw: True):
        raise NotImplementedError()

    async def _amessage(self, messages_list: List[List[Dict]], output_checker: Callable = lambda *args, **kw: True):
        """
        Async send messages to the GPT chatbot.
        """

        results = await asyncio.gather(
            *(self._create_achat(message, output_checker=output_checker) for message in messages_list)
        )

        return results

    def message(self, messages_list: Union[List[Dict], List[List[Dict]]],
                output_checker: Callable = lambda *args, **kw: True):
        """
        Send chunked messages to the GPT chatbot.
        """
        assert messages_list, 'Empty message list.'

        if isinstance(messages_list[0], dict):  # convert messages List[Dict] to messages_list List[List[Dict]]
            messages_list = [messages_list]

        # Calculate the total sending token number and approximated billing fee.
        token_numbers = [get_messages_token_number(message) for message in messages_list]
        logger.info(f'Max token num: {max(token_numbers):.0f}, '
                    f'Avg token num: {sum(token_numbers) / len(token_numbers):.0f}')

        # if the approximated billing fee exceeds the limit, raise an exception.
        approximated_fee = sum([self.estimate_fee(messages) for messages in messages_list])
        logger.info(f'Approximated billing fee: {approximated_fee:.4f} USD')
        self.api_fees += [0]  # Actual fee for this translation call.
        if approximated_fee > self.fee_limit:
            raise ChatBotException(f'Approximated billing fee {approximated_fee} '
                                   f'exceeds the limit: {self.fee_limit}$.')

        try:
            results = asyncio.run(self._amessage(messages_list, output_checker=output_checker))
        except ChatBotException as e:
            logger.error(f'Failed to message with GPT. Error: {e}')
            raise e
        finally:
            logger.info(f'Translation fee for this call: {self.api_fees[-1]:.4f} USD')
            logger.info(f'Total bot translation fee: {sum(self.api_fees):.4f} USD')

        return results


@_register_chatbot
class GPTBot(ChatBot):
    def __init__(self, model='gpt-3.5-turbo-0125', temperature=1, top_p=1, retry=8, max_async=16, json_mode=False,
                 fee_limit=0.05, proxy=None):
        # Pricing for 1M tokens, info from https://openai.com/pricing
        pricing = {
            'gpt-3.5-turbo-0125': (0.5, 1.5),
            'gpt-3.5-turbo': (0.5, 1.5),
            'gpt-4-0125-preview': (10, 30),
            'gpt-4-turbo-preview': (10, 30)
        }

        super().__init__(pricing, temperature, top_p, retry, max_async, fee_limit)

        self.async_client = AsyncGPTClient(api_key=os.environ['OPENAI_API_KEY'], http_client=httpx.AsyncClient(
            proxies=proxy,
        ))

        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.retry = retry
        self.max_async = max_async
        self.json_mode = json_mode
        self.fee_limit = fee_limit

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.async_client.close()

    def update_fee(self, response: ChatCompletion):
        prompt_price, completion_price = self.pricing[self.model]

        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        self.api_fees[-1] += (prompt_tokens * prompt_price + completion_tokens * completion_price) / 1000000

    def get_content(self, response):
        return response.choices[0].message.content

    async def _create_achat(self, messages: List[Dict], output_checker: Callable = lambda *args, **kw: True):
        logger.debug(f'Raw content: {messages}')

        response = None
        for i in range(self.retry):
            try:
                response = await self.async_client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    response_format={'type': 'json_object' if self.json_mode else 'text'}
                )
                self.update_fee(response)
                if response.choices[0].finish_reason == 'length':
                    raise LengthExceedException(response)
                if not output_checker(messages, response.choices[0].message.content):
                    logger.warning(f'Invalid response format. Retry num: {i + 1}.')
                    continue

                break
            except openai.RateLimitError:
                sleep_time = random.randint(30, 60)
                logger.warning(f'Rate limit exceeded. Wait {sleep_time}s before retry. Retry num: {i + 1}.')
                time.sleep(sleep_time)
            except openai.APITimeoutError:
                logger.warning(f'Timeout. Wait 3 before retry. Retry num: {i + 1}.')
                time.sleep(3)
            except openai.APIConnectionError:
                logger.warning(f'API connection error. Wait 15s before retry. Retry num: {i + 1}.')
                time.sleep(15)
            except openai.APIError:
                logger.warning(f'API error. Wait 15s before retry. Retry num: {i + 1}.')
                time.sleep(15)

        if not response:
            raise ChatBotException('Failed to create a chat.')

        return response


@_register_chatbot
class ClaudeBot(ChatBot):
    def __init__(self, model='claude-3-sonnet-20240229', temperature=1, top_p=1, retry=8, max_async=16, fee_limit=0.2,
                 proxy=None):
        # Pricing for 1M tokens, info from https://docs.anthropic.com/claude/docs/models-overview#model-comparison
        pricing = {
            'claude-3-opus-20240229': (15, 75),
            'claude-3-sonnet-20240229': (3, 15),
            'claude-3-haiku-20240307': (0.25, 1.25)
        }

        super().__init__(pricing, temperature, top_p, retry, max_async, fee_limit)

        self.async_client = AsyncAnthropic(api_key=os.environ['ANTHROPIC_API_KEY'], http_client=httpx.AsyncClient(
            proxies=proxy,
        ))

        self.model = model
        self.retry = retry
        self.max_async = max_async
        self.fee_limit = fee_limit

    def update_fee(self, response: Message):
        prompt_price, completion_price = self.pricing[self.model]

        prompt_tokens = response.usage.input_tokens
        completion_tokens = response.usage.output_tokens

        self.api_fees[-1] += (prompt_tokens * prompt_price + completion_tokens * completion_price) / 1000000

    def get_content(self, response):
        return response.content[0].text

    async def _create_achat(self, messages: List[Dict], output_checker: Callable = lambda *args, **kw: True):
        logger.debug(f'Raw content: {messages}')

        # Move "system" role into the parameters
        system_msg = NOT_GIVEN
        if messages[0]['role'] == 'system':
            system_msg = messages.pop(0)['content']

        response = None
        for i in range(self.retry):
            try:
                response = await self.async_client.messages.create(
                    max_tokens=4096,
                    model=self.model,
                    messages=messages,
                    system=system_msg,
                    temperature=self.temperature,
                    top_p=self.top_p,
                )
                self.update_fee(response)

                if response.stop_reason == 'max_tokens':
                    raise LengthExceedException(response)
                if not output_checker(messages, response.content[-1].text):
                    logger.warning(f'Invalid response format. Retry num: {i + 1}.')
                    continue

                break
            except anthropic.RateLimitError:
                sleep_time = random.randint(30, 60)
                logger.warning(f'Rate limit exceeded. Wait {sleep_time}s before retry. Retry num: {i + 1}.')
                time.sleep(sleep_time)
            except anthropic.APITimeoutError:
                logger.warning(f'Timeout. Wait 3 before retry. Retry num: {i + 1}.')
                time.sleep(3)
            except anthropic.APIConnectionError:
                logger.warning(f'API connection error. Wait 15s before retry. Retry num: {i + 1}.')
                time.sleep(15)
            except anthropic.APIError as e:
                logger.warning(f'API error: {e}. Wait 15s before retry. Retry num: {i + 1}.')
                time.sleep(15)

        if not response:
            raise ChatBotException('Failed to create a chat.')

        return response
