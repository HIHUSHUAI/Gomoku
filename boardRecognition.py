import time
from typing import Tuple, Any

import cv2
import numpy as np
import pygetwindow as gw
import pyautogui

"""
对 白 88  114
我 黑 329 666
棋盘   格长25pix   半格12.5pix
       216
15.5   14     400
       603
x1  y1        x2  y2
32 235   25   385 586
"""


class boardRecognition:
    def __init__(self, window_title: str = '欢乐五子棋'):
        self.window = gw.getWindowsWithTitle(window_title)[0]

    def get_screen(self):
        # 将窗口置于前台（可选，取决于系统和权限）
        # self.window.activate()
        # self.window.restore()
        screenshot = pyautogui.screenshot(region=self.window.box)
        # 将屏幕截图转换为OpenCV图像格式
        screenshot_cv = np.array(screenshot)
        screenshot_cv = screenshot_cv[:, :, ::-1].copy()  # 转换RGB到BGR
        # 棋盘裁切
        # screenshot_board = screenshot_cv[218:603, 16:399]

        return screenshot_cv

    # # 应用高斯模糊
    # blur = cv2.GaussianBlur(adjusted, (5, 5), 0)
    # # 对图像进行对比度和亮度调整
    # adjusted = cv2.convertScaleAbs(blur, alpha=1, beta=0)
    # # 二值化
    # _, binary_image = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)
    # # cv2.THRESH_BINARY + cv2.THRESH_OTSU

    def get_screen_binarization(self, screenshot_cv):
        # 图像处理
        gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        # adjusted = cv2.convertScaleAbs(gray, alpha=1.3, beta=-350)
        _, binary_image_white = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)
        binary_image_white_ = cv2.bitwise_not(binary_image_white)
        _, binary_image_black = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
        binary_image_white_and_black = cv2.bitwise_xor(binary_image_white_, binary_image_black)

        return binary_image_white, binary_image_black, binary_image_white_and_black

    def get_point_coordinates(self):
        """生成棋盘点位,return->字典{(x,y):[0,p_x,p_y]}"""
        x1, y1 = 32, 235
        # x2, y2 = 385, 586
        pane = 25
        point_coordinates = {}
        for x in range(0, 15):
            for y in range(0, 15):
                point_coordinates[(x, y)] = [0, x1 + pane * x, y1 + pane * y]
        return point_coordinates

    def displays_points(self, screenshot_cv, point_coordinates):
        """*检查函数:检查生成的点位置对不对"""
        for X, Y in point_coordinates:
            print(X, Y)
            print(point_coordinates[(X, Y)])
            _, x, y = point_coordinates[(X, Y)]
            # 在图像上画点，这里设置点的半径为1，颜色为红色(BGR值(0, 0, 255))，厚度为-1表示填充圆
            cv2.circle(screenshot_cv, (x, y), radius=10, color=(0, 0, 255), thickness=1)
        return screenshot_cv

    def find_new_point(self, screenshot_cv, boardDict, is_playFirst, update_all=False, is_show_testResults=False):
        binary_image_white_and_black = self.get_screen_binarization(screenshot_cv)[2]
        # binary_image = cv2.GaussianBlur(binary_image_white_and_black, (13, 13), 0)
        binary_image = cv2.GaussianBlur(binary_image_white_and_black, (7, 7), 0)
        if is_show_testResults:
            cv2.imshow('Window binary_image', binary_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # 检测圆形
        # circles = cv2.HoughCircles(binary_image, cv2.HOUGH_GRADIENT, 1, 10, param1=30, param2=30, minRadius=3, maxRadius=25)
        circles = cv2.HoughCircles(binary_image, cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=30, param2=15,
                                   minRadius=3, maxRadius=25)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # print(center)
                # 画圆心
                # cv2.circle(screenshot_cv, center, 1, (0, 100, 100), 3)
                # 画圆轮廓
                if is_show_testResults:
                    radius = i[2]
                    cv2.circle(binary_image, center, radius, (255, 0, 255), 1)
                    cv2.circle(screenshot_cv, center, radius, (255, 0, 255), 1)
                # 判断是否在coordinates
                # for X, Y in boardDict:
                #     if abs(boardDict[(X, Y)][1] - i[0]) < 10 and \
                #             abs(boardDict[(X, Y)][2] - i[1]) < 10 and \
                #             boardDict[(X, Y)][0] == 0:
                #         print('检测到新棋子:', X, Y)
                #         # 判断是否是新棋子(对方的,不会是自己的,自己的在下棋时就更新了)
                #         boardDict[(X, Y)][0] = 1
                for (X, Y), data in boardDict.items():
                    if abs(data[1] - i[0]) < 10 \
                            and abs(data[2] - i[1]) < 10 \
                            and data[0] == 0:
                        print(f'检测到新棋子: {X}, {Y}')
                        if not update_all:
                            if is_playFirst:
                                data[0] = 2
                                print('data[0] = 2')
                            else:
                                data[0] = 1
                                print('data[0] = 1')
                            return X, Y
                        else:
                            # 识别颜色
                            # 先判断是否先手,先手是黑
                            if is_playFirst:
                                if self.is_whiteOrBlack(screenshot_cv, data[1], data[2]):
                                    print(f'更新对手棋子: {X}, {Y}为 白')
                                    data[0] = 2
                                else:
                                    print(f'更新my棋子: {X}, {Y}为 黑')
                                    data[0] = 1
                            else:
                                if self.is_whiteOrBlack(screenshot_cv, data[1], data[2]):
                                    print(f'更新my棋子: {X}, {Y}为 白')
                                    data[0] = 1
                                else:
                                    print(f'更新对手棋子: {X}, {Y}为 黑')
                                    data[0] = 2

        if is_show_testResults:
            cv2.imshow('Window binary_image', binary_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return -1, -1

    def is_playFirst(self, screenshot_cv):
        # 获取点(x, y)的颜色
        up_color = screenshot_cv[114, 88]
        my_color = screenshot_cv[666, 329]
        # 将BGR颜色值转换为灰度值
        gray_value_up = cv2.cvtColor(np.uint8([[up_color]]), cv2.COLOR_BGR2GRAY)[0][0]
        gray_value_my = cv2.cvtColor(np.uint8([[my_color]]), cv2.COLOR_BGR2GRAY)[0][0]
        # 判断颜色
        # 设置一个阈值来区分偏白还是偏黑，一般128是中间值，可根据实际情况调整
        if gray_value_up > 128 and gray_value_up > gray_value_my:
            print("我先手!")
            return True
        elif gray_value_my > 128 and gray_value_up < gray_value_my:
            print("对方先手!")
            return False

    def is_whiteOrBlack(self, screenshot_cv, x, y):
        # 获取点(x, y)的颜色
        point_color = screenshot_cv[y, x]
        # 将BGR颜色值转换为灰度值
        gray_value_point = cv2.cvtColor(np.uint8([[point_color]]), cv2.COLOR_BGR2GRAY)[0][0]
        # 判断颜色
        # 设置一个阈值来区分偏白还是偏黑，一般128是中间值，可根据实际情况调整
        if gray_value_point > 128:
            print("白!")
            return True
        else:
            print("黑!")
            return False

    def is_color_match(self, screenshot_cv, x, y, target_color_bgr=(137, 119, 255)):
        point_color = screenshot_cv[y, x]
        # print(f'point_color:{point_color}')
        if np.all(point_color == target_color_bgr):
            return True
        else:
            return False


if __name__ == '__main__':
    bdrc = boardRecognition()

    screenshot_cv = bdrc.get_screen()

    boardDict = bdrc.get_point_coordinates()

    bdrc.find_new_point(screenshot_cv, boardDict, bdrc.is_playFirst(screenshot_cv), True, is_show_testResults=True)
    # # 检查棋盘坐标
    # # displays_points(screenshot_cv, coordinates)
    #
    # print(boardDict)
    #
    # bdrc.is_playFirst(screenshot_cv)

    # 显示结果（可选）
    cv2.imshow('Window Screenshot', screenshot_cv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
