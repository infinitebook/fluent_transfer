import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

completion = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[
    {"role":"user", "content":"Say this is a test!"}
    ])
print(completion.choices[0].message.content)
