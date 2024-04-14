
class ProgramConfig:
    """数据类，用于存储程序配置信息。"""

    def __init__(self):
        """初始化程序配置的基本参数。"""
        self.debug_mode = True  # 调试模式开关
        self.version = "1.0"  # 版本信息

    def __str__(self):
        """返回配置信息的友好字符串表示。"""
        return f"Debug Mode: {self.debug_mode}, Version: {self.version}"