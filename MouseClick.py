import pyautogui
import time


class MouseController:
    def __init__(self):
        """初始化鼠标控制器"""
        pyautogui.FAILSAFE = True  # 启用自动防故障功能

    def click(self, x, y):
        """模拟鼠标单击"""
        pyautogui.click(x, y)

    def slow_click(self, x, y, interval=0.2):
        """模拟鼠标慢速单击"""
        pyautogui.doubleClick(x, y, interval=interval)
        # pyautogui.click(x, y)
        # time.sleep(interval)
        # pyautogui.click(x, y)


    def double_click(self, x, y, interval=0.1):
        """模拟鼠标快速双击"""
        pyautogui.doubleClick(x, y, interval=interval)

    def move_to(self, x, y, duration=0.5):
        """移动鼠标到指定坐标"""
        pyautogui.moveTo(x, y, duration=duration)

    def get_screen_coords(self, window_coords, window_position):
        """计算指定窗口里的坐标换算成屏幕坐标"""
        # window_position 应该是一个元组，格式为 (窗口左上角的x坐标, 窗口左上角的y坐标)
        screen_x = window_position[0] + window_coords[0]
        screen_y = window_position[1] + window_coords[1]
        return screen_x, screen_y


# 使用示例
if __name__ == "__main__":
    mouse = MouseController()
    # 假设窗口在屏幕上的位置
    window_position = (100, 100)

    # 窗口内坐标
    window_coords = (50, 50)

    # 计算屏幕坐标
    screen_coords = mouse.get_screen_coords(window_coords, window_position)
    print("Screen Coordinates:", screen_coords)

    # 移动鼠标并单击
    mouse.move_to(*screen_coords)
    mouse.click(*screen_coords)

    # 慢速单击
    mouse.slow_click(*screen_coords)

    # 快速双击
    mouse.double_click(*screen_coords)
