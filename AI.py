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
        self.mouse = MouseController()
        self.manager: AIProcessManager
        self.communicator: AICommunicator
        self.gomokuInterfaces: GomokuInterfaces

    def getReady(self):
        executable_path = r"D:\PythonProject\Ai\Gomoku\AI\pbrain-embryo21_e.exe"
        self.manager = AIProcessManager(executable_path)
        stdin, stdout, stderr = self.manager.start_process()
        self.communicator = AICommunicator(stdin, stdout, stderr)
        interface = CMDInterface(self.communicator)
        time.sleep(0.5)
        self.gomokuInterfaces = GomokuInterfaces(self.communicator)
        self.gomokuInterfaces.sendDefault()
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

    def getend(self):
        self.manager.stop_process()
        self.communicator.close()

    def breaking_through_levels(self):
        """残局闯关"""
        '''
        新的一局
        先判断先手存入变量,
        识别棋子
        准备ai
        board
        '''

        print('=棋局开始=')
        # 棋局开始后需等待三秒才能操作
        time.sleep(5)
        # 获取屏幕
        screen = self.bdrc.get_screen()

        # 是否先手
        is_playFirst = self.bdrc.is_playFirst(screen)

        # 读取棋盘 然后处理
        boardDict = self.bdrc.get_point_coordinates()
        self.bdrc.find_new_point(screen, boardDict, is_playFirst, True)
        boardlist = []
        for (X, Y), data in boardDict.items():
            if data[0] != 0:
                boardlist.append([X, Y, data[0]])
        point = self.gomokuInterfaces.board(boardlist)
        # 操作点击point
        self.mouse.slow_click(self.window.left
                              + boardDict[(int(point[0]), int(point[1]))][1],
                              self.window.top
                              + boardDict[(int(point[0]), int(point[1]))][2])
        boardDict[(int(point[0]), int(point[1]))][0] = 1

        # 循环
        while True:
            while True:
                self.screen = self.bdrc.get_screen()
                x, y = self.bdrc.find_new_point(self.screen, boardDict, is_playFirst, is_show_testResults=False)
                print('等待对方落子...')
                if y != -1:
                    break
                else:
                    time.sleep(1)
            point = self.gomokuInterfaces.turn(x, y)

            # 操作点击point
            if point[0] == -1:
                if point[1] == -300:
                    print("结束")
                    break
                elif point[1] == -200:
                    print("输入点位不能被操作")
                elif point[1] == -100:
                    print("回复识别出错")
                elif point[1] == -99:
                    print("回复点位识别出错")
                else:
                    print("未知错误")
            else:
                print(f'AI建议落子 -> {point}')
                try:
                    self.mouse.slow_click(self.window.left + boardDict[(int(point[0]), int(point[1]))][1],
                                          self.window.top + boardDict[(int(point[0]), int(point[1]))][2])
                    boardDict[(int(point[0]), int(point[1]))][0] = 1
                except KeyError as e:
                    print(f"操作失败，无法找到点位 {point}: {e}")
                except Exception as e:
                    print(f"发生错误: {e}")

        print('while True Done')

    def run_breaking_through_levels(self):
        while True:
            self.getReady()
            print('=== 残局闯关 ===')
            self.breaking_through_levels()
            # 下一关
            time.sleep(2)
            print('下一关')
            self.mouse.click(self.window.left + 210, self.window.top + 655)
            self.getend()

    def pk(self):
        # 棋力评测
        print('=棋力评测=')
        self.getReady()

        # 获取屏幕
        screen = self.bdrc.get_screen()
        # 是否先手
        is_playFirst = self.bdrc.is_playFirst(screen)

        boardDict = self.bdrc.get_point_coordinates()

        if is_playFirst:
            point = self.gomokuInterfaces.begin()
            # 操作点击point
            self.mouse.slow_click(self.window.left
                                  + boardDict[(int(point[0]), int(point[1]))][1],
                                  self.window.top
                                  + boardDict[(int(point[0]), int(point[1]))][2])
            boardDict[(int(point[0]), int(point[1]))][0] = 1

        # 循环
        while True:
            # time.sleep(3)  # 机器人落子的时间,需等待

            while True:

                self.screen = self.bdrc.get_screen()
                x, y = self.bdrc.find_new_point(self.screen, boardDict, is_playFirst, is_show_testResults=False)
                print('等待对方落子...')
                if y != -1:
                    break
                else:
                    time.sleep(1)
            point = self.gomokuInterfaces.turn(x, y)

            # 操作点击point
            if point[0] == -1:
                if point[1] == -300:
                    print("结束")
                    break
                elif point[1] == -200:
                    print("输入点位不能被操作")
                elif point[1] == -100:
                    print("回复识别出错")
                elif point[1] == -99:
                    print("回复点位识别出错")
                else:
                    print("未知错误")
            else:
                print(f'AI建议落子 -> {point}')
                try:
                    self.mouse.slow_click(self.window.left + boardDict[(int(point[0]), int(point[1]))][1],
                                          self.window.top + boardDict[(int(point[0]), int(point[1]))][2])
                    boardDict[(int(point[0]), int(point[1]))][0] = 1
                except KeyError as e:
                    print(f"操作失败，无法找到点位 {point}: {e}")
                except Exception as e:
                    print(f"发生错误: {e}")

        print('while True Done')
        self.getend()

    def run_pk(self):
        while True:
            self.mouse.click(self.window.left + 210, self.window.top + 410)
            while True:
                time.sleep(0.5)
                screen = self.bdrc.get_screen()
                if self.bdrc.is_color_match(screen, 210, 450,target_color_bgr=(182, 230, 247)):
                    break
                print('正在匹配对手...')

            self.pk()
            time.sleep(0.8)
            self.mouse.click(self.window.left + 45, self.window.top + 745)
            time.sleep(0.2)
