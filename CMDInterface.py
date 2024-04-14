import time

from AICommunicator import AICommunicator
from AIProcessManager import AIProcessManager
from GomokuInterfaces import GomokuInterfaces


class CMDInterface:
    """提供用户界面，接收用户命令，
    利用 AICommunicator 发送这些命令，并显示响应。"""

    def __init__(self, communicator):
        self.communicator = communicator

    def run(self):
        """运行命令行接口。"""
        try:
            while True:
                command = input(">>> ")
                if command.lower() == 'quit':
                    break
                self.communicator.send_command(command)
                print(self.communicator.get_response())
        finally:
            print("Cleaning up resources...")
            self.communicator.stdin.close()


if __name__ == "__main__":
    executable_path = r"D:\PythonProject\Ai\Gomoku\AI\pbrain-embryo21_e.exe"
    manager = AIProcessManager(executable_path)
    stdin, stdout, stderr = manager.start_process()
    communicator = AICommunicator(stdin, stdout, stderr)
    interface = CMDInterface(communicator)
    time.sleep(0.5)
    gomokuInterfaces = GomokuInterfaces(communicator)
    gomokuInterfaces.sendDefault()
    time.sleep(0.5)
    # print('t', gomokuInterfaces.turn(4, 5))
    # print('b', gomokuInterfaces.begin())
    # print('r', gomokuInterfaces.restart())
    # boardlist = [
    #     [1, 1, 1],
    #     [4, 1, 1],
    #     [2, 2, 2],
    #     [5, 1, 2],
    # ]
    # print('bo', gomokuInterfaces.board(boardlist))

    interface.run()
    manager.stop_process()
