# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : cherwin
# -------------------------------
# cron "59 59 9 1 2-7 *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('统一茄皇监控')
import hashlib
import json
import os
import random
import string
import time
from datetime import datetime
from os import environ, path

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

IS_DEV = False
if os.path.isfile('DEV_ENV.py'):
    import DEV_ENV

    IS_DEV = True

if os.path.isfile('notify.py'):
    from notify import send

    print("加载通知服务成功！")
else:
    print("加载通知服务失败!")
send_msg = ''
one_msg = ''


def Log(cont=''):
    global send_msg, one_msg
    print(cont)
    if cont:
        one_msg += f'{cont}\n'
        send_msg += f'{cont}\n'


USER_INFO = {}


class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        self.third_id = split_info[0]
        self.wid = split_info[1]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            self.send_UID = last_info

        self.user_index = index + 1
        print(f"\n---------开始执行第{self.user_index}个账号>>>>>")
        self.s = requests.session()
        self.s.verify = False

        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/8555'

        self.headers = {
            'User-Agent': self.UA,
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Origin': 'https://thekingoftomato.ioutu.cn',
            'Referer': 'https://thekingoftomato.ioutu.cn/'

        }
        self.base_url = 'https://qiehuang-apig.xiaoyisz.com/qiehuangsecond/ga'
        self.goodsid = None
        self.Login_res = self.login()

    def load_json(self):
        try:
            with open(f"INVITE_CODE/{ENV_NAME}_INVITE_CODE.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print("未找到文件，返回空字典")
            return {}
        except Exception as e:
            print(f"发生错误：{e}")
            return {}

    def make_request(self, url, method='post', headers={}, params={}):
        if headers == {}:
            headers = self.headers
        if params == {}:
            params = self.params
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, verify=False)

            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, json=params, verify=False)
            else:
                raise ValueError("不支持的请求方法: " + method)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法：", e)
        except Exception as e:
            print("发生了未知错误：", e)

    def gen_sign(self, parameters={}, body=None):
        sign_header = CHERWIN_TOOLS.TYQH_SIGN(parameters, body)
        self.headers.update(sign_header)
        return self.headers

    def login(self):
        login_successful = False
        try:
            login_params = {
                'thirdId': self.third_id,
                'wid': self.wid
            }
            sign_header = self.gen_sign({}, login_params)
            # print(self.headers)
            # Hypothetically speaking, this is how you might perform a POST request in Python with the requests library.
            response = self.s.post(f'{self.base_url}/public/api/login', json=login_params, headers=sign_header)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('code', -1) == 0:
                    auth = response_data['data']['token'] or ''
                    if auth:
                        login_successful = True
                        print(f'账号【{self.user_index}】登录成功')
                        Authorization = {'Authorization': auth}
                        self.headers.update(Authorization)
                    else:
                        print(f'账号【{self.user_index}】登录获取auth失败')
                else:
                    print(f"登录获取auth失败[{response_data['code']}]: {response_data['message']}")
            elif response.status_code == 403:
                print('登录失败[403]: 黑IP了, 换个IP试试吧')
        except Exception as e:
            print(e)
        finally:
            return login_successful

    def get_CapCode(self, slideImgInfo):
        slidingImage = slideImgInfo.get('slidingImage', None)
        backImage = slideImgInfo.get('backImage', None)
        dddddocr_api = os.environ.get('OCR_API', False)
        if not dddddocr_api:
            print('未定义变量【OCR_API】\n取消验证码识别\n搭建方式：https://github.com/CHERWING/CHERWIN_SCRIPTS')
            return False
        if slidingImage and backImage:
            data = {
                "slidingImage": slidingImage,
                "backImage": backImage
            }
            response = requests.post(f"{dddddocr_api}/capcode", data=json.dumps(data),
                                     headers={'Content-Type': 'application/json'})
            print(response.json())
            self.capcode = response.json().get('result', '')
            if self.capcode:
                return True
            else:
                return False

    def get_CapCode_local(self, slideImgInfo):
        slidingImage = slideImgInfo.get('slidingImage', None)
        backImage = slideImgInfo.get('backImage', None)
        if slidingImage and backImage:
            self.capcode = CHERWIN_TOOLS.CAPCODE(slidingImage, backImage)
            if self.capcode:
                return True
            else:
                return False

    def checkUserCapCode(self):
        print(f'提交验证码--->>>')
        # try:
        print(f'验证码：{self.capcode}')
        params = {'xpos': self.capcode}
        print(params)
        sign_header = self.gen_sign(body=params)
        url = f'{self.base_url}/checkUserCapCode'
        response = self.s.post(url, headers=sign_header, json=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            data = data.get('data', 0)
            print(f"验证码正确，获取到[{data}]")
            return True
        else:
            message = data.get('message', '')
            print(f"验证码错误[{message}]")
            return False
        # except Exception as e:
        #     print(e)

    def exchange_find(self):
        print(f'获取兑换列表--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/exchange/find'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                data = data.get('data', {})[1]
                num = data.get('num', 0)
                if num < 0:
                    Log('兑换上限,跳过')
                    return False
                # print(f"兑换列表：{data}")
                exchangePrizeVoList = data.get('exchangePrizeVoList', None)
                if exchangePrizeVoList:
                    for goods in exchangePrizeVoList:
                        name = goods.get('name', '')
                        self.goodsid = goods.get('id', '')
                        usableStock = goods.get('usableStock', '')
                        if usableStock > 0:
                            Log(f'ID：【{self.goodsid}】 【{name}】 当前剩余：{usableStock}【可兑换】')
                            self.sendMsg()
                            if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
                            if TYQH_DHID and TYQH_DHID == self.goodsid:
                                self.exchange_reward(TYQH_DHID)
                            elif TYQH_DHID == '0':
                                self.exchange_reward(self.goodsid)
                            else:
                                continue
                        else:
                            print(f'ID：【{self.goodsid}】【{name}】 当前剩余：{usableStock}【不可兑换】')
            else:
                message = data.get('message', '')
                print(f'{message}')
        except Exception as e:
            print(e)

    def exchange_reward(self, reward_id):
        print(f'尝试兑换--->>>')
        try:
            params = {'id': reward_id}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/exchange/reward'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                data = data.get('data', {}).get('name') or ''
                Log(f"兑换[{data}]成功")
            elif code == 4000:
                slideImgInfo = data.get('data', {}).get('slideImgInfo', None)
                validateCount = data.get('data', {}).get('validateCount', None)
                if slideImgInfo and validateCount:
                    print(f"兑换需要滑块验证")
                    if self.get_CapCode(slideImgInfo):
                        if self.checkUserCapCode():
                            self.exchange_reward(reward_id)
                else:
                    print(f"兑换验证码上限")
            else:
                message = data.get('message', '')
                print(f'兑换[id={reward_id}]: {message}')
        except Exception as e:
            print(e)

    def userTask(self):
        print('\n--------------- 开始日常任务 ---------------')
        if not self.Login_res:
            return False
        self.exchange_find()
        time.sleep(0.5)
        return True

    def sendMsg(self, help=False):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME, help)
            print(push_res)


def down_file(filename, file_url):
    print(f'开始下载：{filename}，下载地址：{file_url}')
    try:
        response = requests.get(file_url, verify=False, timeout=10)
        response.raise_for_status()
        with open(filename + '.tmp', 'wb') as f:
            f.write(response.content)
        print(f'【{filename}】下载完成！')

        # 检查临时文件是否存在
        temp_filename = filename + '.tmp'
        if os.path.exists(temp_filename):
            # 删除原有文件
            if os.path.exists(filename):
                os.remove(filename)
            # 重命名临时文件
            os.rename(temp_filename, filename)
            print(f'【{filename}】重命名成功！')
            return True
        else:
            print(f'【{filename}】临时文件不存在！')
            return False
    except Exception as e:
        print(f'【{filename}】下载失败：{str(e)}')
        return False


def import_Tools():
    global CHERWIN_TOOLS, ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode
    import CHERWIN_TOOLS
    ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode = CHERWIN_TOOLS.main(APP_NAME, local_script_name, ENV_NAME,
                                                                    local_version)


import threading


def execute_task(infos, index):
    run_result = RUN(infos, index).userTask()
    if not run_result:
        return


if __name__ == '__main__':
    APP_NAME = '统一茄皇监控'
    ENV_NAME = 'TYQH_JK'
    print(f'''
✨✨✨ {APP_NAME}脚本 ✨✨✨
✨ 功能：
      奖品监控
✨ 设置青龙变量：
export TYQH= '' 使用相同TYQH变量
export TYQH_DHID= '112' 设置兑换ID则开启自动兑换，设置为0遍历兑换全部可兑换商品
export OCR_API= 'http://localhost:3721' 
✨ 由于青龙python版本问题无法直接使用dddocr需要自行搭建API，搭建方式：https://github.com/CHERWING/CHERWIN_OCR
✨ 如果你的环境可以安装dddocr库则可以替换代码内的【self.get_CapCode】为【self.get_CapCode_local】
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ 推荐定时：59 59 9 1 2-7 * (2-7月每月1日9点59)
✨ 第一个账号助力作者，其余互助
✨✨✨ @Author CHERWIN✨✨✨
                ''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.06.02'
    if IS_DEV:
        import_Tools()
    else:
        if os.path.isfile('CHERWIN_TOOLS.py'):
            import_Tools()
        else:
            if down_file('CHERWIN_TOOLS.py', 'https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/CHERWIN_TOOLS.py'):
                print('脚本依赖下载完成请重新运行脚本')
                import_Tools()
            else:
                print(
                    '脚本依赖下载失败，请到https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/CHERWIN_TOOLS.py下载最新版本依赖')
                exit()
    print(TIPS)
    token = ''
    ENV = os.environ.get('TYQH', '')
    TYQH_DHID = os.environ.get('TYQH_DHID', None)
    if TYQH_DHID == '0':
        Log(f'\n当前已设置TYQH_DHID变量，将自动遍历兑换商品')
    elif TYQH_DHID:
        Log(f'\n当前已设置TYQH_DHID变量，将自动兑换id【{TYQH_DHID}】商品')
    else:
        Log('\n未定义TYQH_DHID变量，取消自动兑换')
    token = ENV if ENV else token
    if not token:
        print(f"未填写TYQH变量\n青龙可在环境变量设置TYQH 或者在本脚本文件上方将ck填入token =''")
        exit()
    tokens = CHERWIN_TOOLS.ENV_SPLIT(token)
    # print(tokens)
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>> 共获取到{len(tokens)} 个账号 <<<<<<<<<<")
        # access_token = []
        # threads = []
        # for index, infos in enumerate(tokens):
        #     thread = threading.Thread(target=execute_task, args=(infos, index))
        #     threads.append(thread)
        #     thread.start()
        #
        # for thread in threads:
        #     thread.join()
    while True:
        current_time = time.localtime()
        if (current_time.tm_hour == 9 and current_time.tm_min == 59 and current_time.tm_sec >= 59) or \
                (current_time.tm_hour == 10 and current_time.tm_min == 1 and current_time.tm_sec <= 59):
            if len(tokens) > 0:
                print(f"\n>>>>>>>>>> 共获取到{len(tokens)} 个账号 <<<<<<<<<<")
                access_token = []
                threads = []
                for index, infos in enumerate(tokens):
                    thread = threading.Thread(target=execute_task, args=(infos, index))
                    threads.append(thread)
                    thread.start()
                for thread in threads:
                    thread.join()
        elif current_time.tm_hour == 10 and current_time.tm_min > 5:
            break
        else:
            time.sleep(1)
