import time
from MouseClick import MouseController
from AICommunicator import AICommunicator
from AIProcessManager import AIProcessManager
from CMDInterface import CMDInterface
from GomokuInterfaces import GomokuInterfaces
from boardRecognition import boardRecognition


class AI:
    """AI类，目前是一个空的实现，预留扩展功能的位置。"""

    def __init__(self):
        self.bdrc = boardRecognition()
        self.window = self.bdrc.window
        self.boardDict = self.bdrc.get_point_coordinates()
        self.gomokuInterfaces = self.getReady()
        self.screen = ''
        self.mouse = MouseController()

    def getReady(self):
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

        # interface.run()
        # manager.stop_process()

        return gomokuInterfaces

    def Breaking_through_levels(self):
        """残局闯关"""
        print('=== 残局闯关 ===')
        '''
        新的一局
        先判断先手存入变量,
        识别棋子
        准备ai
        board
        '''
        # 获取屏幕
        self.screen = self.bdrc.get_screen()

        # 是否先手
        is_playFirst = self.bdrc.is_playFirst(self.screen)

        # 读取棋盘 然后处理
        self.bdrc.find_new_point(self.screen, self.boardDict, is_playFirst, True)
        boardlist = []
        for (X, Y), data in self.boardDict.items():
            if data[0] != 0:
                boardlist.append([X, Y, data[0]])
        point = self.gomokuInterfaces.board(boardlist)
        # 操作点击point
        self.mouse.slow_click(self.window.left
                              + self.boardDict[(int(point[0]), int(point[1]))][1],
                              self.window.top
                              + self.boardDict[(int(point[0]), int(point[1]))][2])
        self.boardDict[(int(point[0]), int(point[1]))][0] = 1

        # 循环
        while True:
            time.sleep(1)
            self.screen = self.bdrc.get_screen()
            import cv2
            x, y = self.bdrc.find_new_point(self.screen, self.boardDict, is_playFirst)
            point = self.gomokuInterfaces.turn(x, y)
            print(point)
            # 操作点击point
            self.mouse.slow_click(self.window.left
                                  + self.boardDict[(int(point[0]), int(point[1]))][1],
                                  self.window.top
                                  + self.boardDict[(int(point[0]), int(point[1]))][2])
            self.boardDict[(int(point[0]), int(point[1]))][0] = 1