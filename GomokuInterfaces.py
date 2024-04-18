import re
import time


class GomokuInterfaces:
    """脚本接口"""

    def __init__(self, communicator):
        self.communicator = communicator

    def sendDefault(self):
        self.communicator.send_command('START 15')
        # time.sleep(1)
        if self.communicator.get_response() != 'OK':
            # 未收到OK确定,错误
            print('START 15 未收到OK确定,错误')
            return False
        print('START 15 收到OK确定')
        info = 'INFO max_memory 1073741824' \
               '\nINFO timeout_match 420000' \
               '\nINFO timeout_turn 10000' \
               '\nINFO game_type 1' \
               '\nINFO rule 0' \
               '\nINFO time_left 179953' \
               '\nINFO folder D:\\ProgramData' \
               '\n'
        self.communicator.send_command(info)
        time.sleep(0.2)
        response = self.communicator.get_response().strip()
        if response != '':
            print(f'INFO 发送错误, response = {response}')
            return False
        print('INFO 发送成功')
        return True

    def get_response(self):
        response: str = self.communicator.get_response()
        attempt = 0
        max_attempts = 100  # 设置最大尝试次数以避免潜在的无限循环

        while response == '' and attempt < max_attempts:
            # 一直获取结果
            print('getting response...')
            response = self.communicator.get_response()
            attempt += 1
            time.sleep(0.1)

        if attempt == max_attempts:
            print("Response timeout or failure.")
            return False

        return response

    def response_processing(self, response):
        print(f"\nresponse: \n{response}\n")

        # if response == 'OK':
        #     print("response == 'OK'")
        #     return response
        if self.check_ends_with_none_zero_zero(response):
            print(f'self.check_ends_with_none_zero_zero')
            return -1, -300
        if self.check_error_opponents_move(response):
            print(f'not self.check_error_opponents_move')
            return -1, -200
        if not response.startswith('DEBUG Thread'):
            print("not response.startswith('DEBUG Thread')")
            return -1, -100

        points = self.extract_last_two_numbers(response)
        if points is None:
            print('extract_last_two_numbers error :', points)
            return -1, -99

        print('response_processing() -> points :', points)
        return points

    def check_error_opponents_move(self, response: str):
        # 使用正则表达式检查文本中是否包含 "ERROR opponent's move"
        return bool(re.search(r"ERROR opponent's move", response))

    def extract_last_two_numbers(self, response: str):
        # 从文本中提取最后两个数字
        points = re.findall(r"\b(\d+),(\d+)\b", response)
        return points[-1] if points else None

    def check_ends_with_none_zero_zero(self, response: str):
        # 检查文本是否以 "(none)0,0" 结尾
        return bool(re.search(r"\(none\)\n0,0$", response))

    def is_OK(self, response):
        if response == 'OK':
            return True
        else:
            return False

    def is_unknown(self, response):
        if response.startswith('UNKNOWN'):
            return True
        else:
            return False

    def turn(self, x: int, y: int):
        self.communicator.send_command(f'TURN {x},{y}')
        response = self.get_response()
        return self.response_processing(response)

    def begin(self):
        self.communicator.send_command(f'BEGIN')
        response = self.get_response()
        return self.response_processing(response)

    def restart(self):
        self.communicator.send_command(f'RESTART')
        response = self.get_response()
        return self.is_OK(response)

    def board(self, boardlist: list):
        self.communicator.send_command('BOARD')
        for i in boardlist:
            self.communicator.send_command(f'{i[0]},{i[1]},{i[2]}')
            print(f'{i[0]},{i[1]},{i[2]}')
        self.communicator.send_command(f'DONE')
        response = self.get_response()

        if self.is_unknown(response):
            return False

        return self.response_processing(response)
