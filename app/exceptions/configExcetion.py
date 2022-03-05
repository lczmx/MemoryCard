class MissingRequireConfig(Exception):
    def __init__(self, config):
        self.config = config

    def __str__(self):
        return f"缺失必须的配置{self.config}!\n请查看README: https://github.com/lczmx/MemoryCard"
