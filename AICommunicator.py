import threading
from multiprocessing import Pipe


class AICommunicator:
    """负责实现与 AI 进程的通信，发送命令并异步收集响应。"""

    def __init__(self, stdin, stdout, stderr):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.parent_conn, self.child_conn = Pipe()

        # 创建并启动线程来读取 AI 的标准输出和错误输出
        threading.Thread(target=self.handle_ai_output, args=(self.stdout,)).start()
        threading.Thread(target=self.handle_ai_output, args=(self.stderr,)).start()

    def handle_ai_output(self, pipe):
        """处理 AI 的标准输出或错误输出。"""
        try:
            while True:
                line = pipe.readline()
                if line:
                    self.parent_conn.send(line.strip())
                else:
                    break
        finally:
            pipe.close()

    def send_command(self, command):
        """向 AI 发送命令。"""
        self.stdin.write(command + "\n")
        self.stdin.flush()

    def get_response(self, timeout=0.1):
        """从 AI 获取响应。"""
        responses = []
        while self.child_conn.poll(timeout):
            responses.append(self.child_conn.recv())
        return '\n'.join(responses)
