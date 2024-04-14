import subprocess


class AIProcessManager:
    """负责管理外部 AI 进程的生命周期，包括启动和停止进程。"""

    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.process = None
        self.thread_out = None
        self.thread_err = None

    def start_process(self):
        """启动 AI 进程并返回标准输入和输出管道。"""
        self.process = subprocess.Popen(
            [self.executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        return self.process.stdin, self.process.stdout, self.process.stderr

    def stop_process(self):
        """停止 AI 进程。"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
