class ClassA:
    def __init__(self, path):
        self.path = path

    def A(self):
        # 这里你可以处理path或做其他操作
        self.path="awdadadawd"
        return self.path


class ClassB:
    def B(self, path):
        # 在这个方法中打印从ClassA传来的path
        print("Received path:", path)


# 创建ClassA的实例，并初始化path
a = ClassA("/my/example/path")

# 调用ClassA的方法A来获取path
path_from_a = a.A()

# 创建ClassB的实例
b = ClassB()

# 将path传递给ClassB的方法B
b.B(path_from_a)
