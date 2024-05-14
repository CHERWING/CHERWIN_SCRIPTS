# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : cherwin
# -------------------------------
# cron "25 10-22/2 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('统一快乐星球小程序-茄皇的家')

import json
import os
import random
import time
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
one_msg=''
def Log(cont=''):
    global send_msg,one_msg
    print(cont)
    if cont:
        one_msg += f'{cont}\n'
        send_msg += f'{cont}\n'

USER_INFO = {}

class RUN:
    def __init__(self, info,index):
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
        self.sun = 0
        self.land = {}
        self.refresh_land_step = False
        self.need_help_unlock = True
        self.need_help_task = True
        self.need_help_risk = True

        self.can_go_risk = True
        self.can_add_friend = True

        self.can_help_task = True
        self.can_help_risk = True
        self.can_help_unlock = True
        self.role_id =''
        self.role_progress=''
        self.role_max=''
        self.all_land_unlock = True
        self.all_role_unlock = True
        self.help_task_config = {}
        self.help_role_config = {}
        self.group_step = ['发育期', '幼苗期', '开花期', '结果期', '收获期']
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

    def userInfo_get(self,END=False):
        print(f'获取用户[{self.user_index}]信息--->>>')
        try:
            sign_header = self.gen_sign()
            # print(self.headers)
            url = f'{self.base_url}/userInfo/get'
            # 发起GET请求
            response = self.s.get(url, headers=sign_header, verify=False)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                data = data.get('data', {})
                self.userId = data['userId']
                self.gold = int(data['gold'])
                self.score = int(data['score'])
                self.sun = int(data['sun'])
                self.sunMax = int(data['sunMax'])
                self.nickName = data['nickName']
                if self.nickName == None:self.nickName = '未命名'
                new_data = {
                    self.userId:
                        {
                            'name': self.nickName
                        }
                }
                USER_INFO.update(new_data)
                CHERWIN_TOOLS.SAVE_INVITE_CODE(f"INVITE_CODE/{ENV_NAME}_INVITE_CODE.json", new_data)
                if END:
                    Log(f"-----用户[{self.user_index}]信息-----\n用户Id:{self.userId}\n用户名:{self.nickName}\n调料🧂x{self.gold}\n番茄🍅x{self.score}\n阳光☀x{self.sun}\n------用户[{self.user_index}]信息END------")
                else:
                    print(f"-----用户[{self.user_index}]信息-----\n用户Id:{self.userId}\n用户名:{self.nickName}\n调料🧂x{self.gold}\n番茄🍅x{self.score}\n阳光☀x{self.sun}\n------用户[{self.user_index}]信息END------")

            else:
                error_message = data.get('message', '')
                print(f"获取账号信息失败[{str(code)}]: {error_message}")
        except Exception as e:
            print(e)
        finally:
            return

    def userInfo_autoSun(self):
        print('收集阳光--->>>')
        sign_header = self.gen_sign()
        url = f'{self.base_url}/userInfo/autoSun'
        response = self.s.get(url, headers=sign_header)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            sun = data.get('data', {}).get('sun', 0)
            print(f"刷新收集到【{sun}】阳光---√")
        else:
            print(f"刷新收集阳光失败[{data['code']}]: {str(code)}")

    def task_get(self):
        print(f'获取任务列表--->>>')
        sign_header = self.gen_sign()
        url = f'{self.base_url}/task/get'
        response = self.s.get(url, headers=sign_header)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            tasks = data.get('data', [])
            for task in tasks:
                self.task_id = task['id']
                self.task_title = task['title']
                task_status = task['status']
                self.task_progress = task.get('currentProgress', 0)
                self.task_max_progress = task.get('progress', 1)

                print(f"任务：【{self.task_title}】进度：【{self.task_progress}/{self.task_max_progress}】")
                if self.task_title == '邀请好友助力':
                    if self.task_progress == self.task_max_progress:
                        self.need_help_task = False
                    # new_data = {
                    #     self.userId: {
                    #         'task_id': self.task_id,
                    #         'task_stu': self.can_help_task,
                    #         'current_progress': self.task_progress
                    #     }
                    # }
                    # USER_INFO.update(new_data)
                    # CHERWIN_TOOLS.SAVE_INVITE_CODE("INVITE_CODE/QH_INVITE_CODE.json", new_data)
                    print(f"任务 '{self.task_title}' 【跳过】---》")
                    continue
                elif self.task_title == '邀请新人助力':
                    print(f"任务 '{self.task_title}' 【跳过】---》")
                    continue

                if task_status == 0 and self.task_progress < self.task_max_progress:
                    # 此任务尚未完成，根据具体业务逻辑进行处理，如启动任务
                    print(f"任务【{self.task_title}】【未完成】执行任务---》")
                    self.task_doTask()  # 取消这行注释来执行任务

                elif task_status == 1:
                    # 任务已完成但奖励未被领取，根据业务逻辑领取奖励
                    print(f"任务【{self.task_title}】【已完成】领取奖励---》")
                    self.task_reward()  # 取消这行注释来领取奖励
        else:
            print(f"获取任务列表失败[{data['code']}]: {str(code)}")

    def task_doHelpTask(self,help_data):
        # print('开始助力任务---》')
        params = {'id': help_data["task_id"]}
        sign_header = self.gen_sign(params)
        url = f'{self.base_url}/task/doTask'
        response = self.s.get(url, headers=sign_header,params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            print(f"助力账号[{help_data['index']}][{help_data['name']}]成功---√")
        elif '已超出' in data.get('message', ''):
            self.can_help_task = False
            error_message = data.get('message', '')
            print(f"助力账号[{help_data['index']}][{help_data['name']}]失败[{code}]: {error_message}")
        else:
            error_message = data.get('message', '')
            print(f"助力账号[{help_data['index']}][{help_data['name']}]失败[{code}]: {error_message}")
            if '助力次数' in error_message:
                self.can_help_task = False

    def task_doTask(self):
        sign_header = self.gen_sign({'id': self.task_id})
        url = f'{self.base_url}/task/doTask'
        params = {'id': self.task_id}
        response = self.s.get(url, headers=sign_header, params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            print(f"完成任务[{self.task_title}]成功---√")
        else:
            print(f"完成任务[{self.task_title}]失败[{str(code)}]: {data.get('message', '')}")

    def task_reward(self):
        sign_header = self.gen_sign({'id': self.task_id})
        url = f'{self.base_url}/task/reward'
        params = {'id': self.task_id}
        response = self.s.get(url, headers=sign_header, params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            print(f"领取任务[{self.task_title}]奖励成功---√")
        else:
            print(f"领取任务[{self.task_title}]奖励失败[{str(code)}]: {data.get('message', '')}")

    def user_role_get(self):
        print('\n查询角色信息--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/user-role/get'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                data = data.get('data')
                if data and data.get('isReward'):
                    print('可领取定时奖励，开始领取---》')
                    self.user_role_reward()  # 此处调用 user_role_reward 函数
                for role in data.get('roleList', []):
                    if role['status'] > 0:
                        print(f"角色【{role['name']}】已解锁---√")
                        continue
                    if role['unlockType'] == 1:
                        if self.gold >= role['unlockNum']:
                            print(f"调料包充足，开始解锁角色【{role['name']}】---》")
                            self.user_role_goldUnlock(role)  # 此处调用 user_role_goldUnlock 函数
                        else:
                            print(f"调料包不足解锁角色【{role['name']}】---！")
                    elif role['unlockType'] == 2:
                        self.user_role_findFriendHelpInfo(role)  # 此处调用 user_role_findFriendHelpInfo 函数
            else:
                message = data.get('message', '')
                print(f'角色信息失败【{code}】: {message}')
        except Exception as e:
            print(e)

    def user_role_findFriendHelpInfo(self, role):
        print(f'查询角色邀请进度--->>>')
        try:
            params = {'userRoleId': role['id']}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/user-role/findFriendHelpInfo'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                data = data.get('data')
                self.help_role_config = {
                    'id': role['id'],
                    'progress': len(data) if data else 0,
                    'max': role['unlockNum']
                }
                self.role_id = role['id']
                self.role_progress = len(data) if data else 0
                self.role_max = role['unlockNum']
                if role['unlockNum'] == len(data) if data else 0:
                    self.need_help_unlock=False
                # new_data = {
                #     self.userId:
                #         {
                #             'role_id': self.role_id,
                #             'role_can_help': self.can_help_unlock,
                #             'role_progress': self.role_progress,
                #             'role_max': self.role_max
                #         }
                # }
                # USER_INFO.update(new_data)
                # CHERWIN_TOOLS.SAVE_INVITE_CODE("INVITE_CODE/QH_INVITE_CODE.json", new_data)
                print(f'查询角色【{role["name"]}】邀请进度成功---√')
            else:
                message = data.get('message', '')
                print(f'查询角色【{role["name"]}】邀请进度失败[{code}]: {message}')
        except Exception as e:
            print(e)

    def user_role_friendHelpUnlock(self, help_data):
        print('开始角色解锁互助--->>>')
        # try:
        params = {'userRoleId': help_data['role_id']}
        sign_header = self.gen_sign(params)
        url = f'{self.base_url}/user-role/friendHelpUnlock'
        response = self.s.get(url, headers=sign_header, params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            help_data['role_progress'] += 1
            print(f'助力账号[{help_data["index"]}][{help_data["name"]}]解锁角色成功---√')
        else:
            message = data.get('message', '')
            print(f'助力账号[{help_data["index"]}][{help_data["name"]}]解锁角色失败[{code}]: {message}')
        # except Exception as e:
        #     print(e)

    def user_role_goldUnlock(self, role):
        print(f'解锁角色开始--->>>')
        try:
            params = {'roleId': role['roleId']}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/user-role/goldUnlock'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                self.gold -= role['unlockNum']
                print(f'解锁角色[{role["name"]}]成功')
                self.user_role_reward()  # 此处调用 user_role_reward 函数
            else:
                message = data.get('message', '')
                print(f'解锁角色[{role["name"]}]失败[{code}]: {message}')
        except Exception as e:
            print(e)

    def user_role_reward(self):
        print(f'领取伴手礼--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/user-role/reward'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                data = data.get('data')
                name = data.get('name') if data else 'unknown'
                print(f'领取伴手礼【{name}】成功')
            else:
                message = data.get('message', '')
                print(f'领取伴手礼失败[{code}]: {message}')
        except Exception as e:
            print(e)

    def user_land_get(self):
        print(f'\n刷新土地信息--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/user-land/get'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print('土地信息刷新成功---√')
                for land in data.get('data', {}).get('gaUserLandList', []):
                    ga_user_land_list = data.get('data', {}).get('gaUserLandList', [])
                    for land_info in ga_user_land_list:
                        land_id = land_info['id']
                        land_no = land_info['no']
                        status = land_info['status']
                        step = land_info['step']
                        left_sun_count = land_info['leftSunCount']
                        sum_sun_count = land_info['sumSunCount']
                        sun_time = land_info['sunTime']
                        sun_timestamp = land_info['sunTimestamp']
                        need_sun = land_info['needSun']
                        use_sun_count = land_info['useSunCount']
                        unlock_gold = land_info['unlockGold']

                        if not self.land.get(land_no):
                            self.land[land_no] = {}

                        self.land[land_no].update({
                            'id': land_id,
                            'no': land_no,
                            'status': status,
                            'step': step,
                            'leftSunCount': left_sun_count,
                            'sumSunCount': sum_sun_count,
                            'sunTime': sun_time,
                            'sunTimestamp': sun_timestamp,
                            'needSun': need_sun,
                            'useSunCount': use_sun_count,
                            'unlockGold': unlock_gold
                        })
                    if land['status'] == 0:
                        # 检查是否应该解锁土地
                        if self.gold >= land['unlockGold']:
                            print('开始解锁新土地---》')
                            self.user_land_unlock(self.land[land_no])
                        else:
                            # print('调料包不足以解锁新土地')
                            self.all_land_unlock = False
            else:
                message = data.get('message', '')
                # 这里应该是日志记录的代码
                print('获取账号信息失败[{}]: {}'.format(str(code), message))
        except Exception as e:
            print(e)

    def user_land_unlock(self, land_info):
        print(f'解锁土地--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/user-land/unlock'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print(f"[{land_info['no']}号土地]解锁成功---√")
                self.gold -= land_info['unlockGold']
                self.user_land_get()
            else:
                message = data.get('message', '')
                print(f"[{land_info['no']}号土地]解锁失败[{str(code)}]:{message}")
        except Exception as e:
            print(e)

    def user_land_result(self, land_info):
        print(f'收获番茄--->>>')
        try:
            params = {'no': land_info['no']}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/user-land/result'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                self.refresh_land_step = True
                print(f'[{land_info["no"]}号土地]收获成功: 番茄x{data.get("data", 0)}---√')
                self.user_land_get()
            else:
                message = data.get('message', '')
                print(f"[{land_info['no']}号土地]收获失败[{str(code)}]: {message}")
        except Exception as e:
            print(e)

    def user_land_sow(self, land_info):
        print(f'播种--->>>')
        try:
            params = {'no': land_info['no']}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/user-land/sow'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                self.refresh_land_step = True
                print(f"[{land_info['no']}号土地]种植成功---√")
                self.user_land_get()
            else:
                message = data.get('message', '')
                print(f"[{land_info['no']}号土地]种植失败[{str(code)}]: {message}")
        except Exception as e:
            print(e)

    def user_land_sun(self, land_info):
        print(f'撒阳光--->>>')
        try:
            params = {'no': land_info['no']}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/user-land/sun'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print(f"[{land_info['no']}号土地]撒阳光成功---√")
                time.sleep(1)
                self.sun -= land_info['needSun']
                self.user_land_get()
            else:
                message = data.get('message', '')
                print(f"[{land_info['no']}号土地]撒阳光失败[{str(code)}]:{message}")
        except Exception as e:
            print(e)

    def user_land_level(self, land_info):
        print(f'浇水升级--->>>')
        try:
            params = {'no': land_info['no']}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/user-land/level'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                self.refresh_land_step = True
                print(f"[{land_info['no']}号土地]浇水升级成功---√")
                self.user_land_get()
            else:
                message = data.get('message', '')
                print(f"[{land_info['no']}号土地]浇水升级失败[{str(code)}]: {message}")
        except Exception as e:
            print(e)

    def take_risk_online(self):
        print(f'进入冒险页--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/take-risk/online'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code != 0:
                message = data.get('message', '')
                print(f'进入冒险页失败{str(code)}: {message}')
            else:
                print(f'进入冒险页成功---√')
                end = data.get('data', {}).get('end', True)
                if end == True:
                    self.need_help_risk = False
        except Exception as e:
            print(e)

    def take_risk_get(self):
        print(f'查询冒险次数--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/common/take-risk/get'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                self.risk_num = data.get('data', {}).get('num', 0)
                if data.get('data', {}).get('complete', False) == False:
                    self.take_risk_up(data.get('data', {}).get('gameMapEvent'))
                    print(f"剩余冒险【{self.risk_num}】次")
            else:
                message = data.get('message', '')
                print(f'查询冒险次数失败: {message}' )
        except Exception as e:
            print(e)

    def take_risk_go(self):
        print(f'开始冒险--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/common/take-risk/go'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            # print(data)
            code = data.get('code', -1)
            if code == 0:
                self.risk_num = data.get('data', {}).get('num', 0)
                if data.get('data', {}).get('complete'):
                    game_map_event_answer_list = data.get('data', {}).get('gameMapEvent', {}).get(
                        'gameMapEventAnswerList', [])
                    filtered_list = filter(lambda x: x.get('dropReward', {}).get('finalNum'),game_map_event_answer_list)
                    rewards = []
                    for item in filtered_list:
                        reward_name = item['dropReward']['name']
                        final_num = item['dropReward']['finalNum']
                        rewards.append(f'{reward_name}x{final_num}')
                    if rewards:
                        print(f'冒险奖励: {rewards}---√')
                    else:
                        print('触发冒险事件没有获取奖励')
                else:
                    # print(data.get('data', {}).get('gameMapEvent'))
                    self.take_risk_up(data.get('data', {}).get('gameMapEvent'))
            elif code == 4000:
                slideImgInfo = data.get('data', {}).get('slideImgInfo', None)
                validateCount = data.get('data', {}).get('validateCount', None)
                if slideImgInfo and validateCount:
                    print('本次冒险需要验证码')
                    self.can_go_risk = False
                    if self.get_CapCode(slideImgInfo):
                        if self.checkUserCapCode():
                            self.take_risk_go()
                else:
                    print(f"验证次数上限")
                    self.can_go_risk = False
            else:
                message = data.get('message', '')
                print(f'冒险失败{code}]: {message}')
                if message and '冒险暂停中' in message or code == 4000:
                    self.can_go_risk = False

        except Exception as e:
            print(e)

    def take_risk_up(self, game_map_event):
        print(f'触发冒险事件--->>>')
        # try:
        gameMapEventAnswerList = game_map_event.get('gameMapEventAnswerList', [])
        index = random.randint(0, len(gameMapEventAnswerList) - 1)
        gameMapEventAnswer = gameMapEventAnswerList[index]
        json_id = gameMapEventAnswer['jsonId']
        # print(json_id)
        params = {'jsonId': json_id}
        sign_header = self.gen_sign(params)
        url = f'{self.base_url}/common/take-risk/up'
        response = self.s.get(url, headers=sign_header, params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            self.risk_num = data.get('data', {}).get('num', 0)
            print(f'剩余次数：【{self.risk_num}】')

            game_map_event_list = data.get('data', {}).get('gameMapEvent', {}).get('gameMapEventAnswerList', [])

            reward_list = [event['dropReward']['name'] + 'x' + str(event['dropReward']['finalNum']) for event in
                           game_map_event_list if event.get('dropReward', {}).get('finalNum')]
            if reward_list:
                print(f'冒险奖励: {reward_list}---√')
            else:
                print('触发冒险事件没有获取奖励')
        else:
            message = data.get('message', '')
            print(f'触发冒险事件[ {json_id} ]失败{code}]: {message}')
        # except Exception as e:
        #     print(e)

    def take_risk_reward(self):
        print(f'领取冒险定时奖励--->>>')
        try:
            url = f'{self.base_url}/take-risk/reward'
            sign_header = self.gen_sign()
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print('领取冒险定时奖励成功---√')
            else:
                message = data.get('message', '').replace('\r', '').split('\n')
                message = ','.join(filter(lambda x: x, message))
                print(f'领取冒险定时奖励失败{code}]: {message}')
        except Exception as e:
            print(e)

    def randomString(self,length, chars='abcdef0123456789'):
        return ''.join(random.choice(chars) for _ in range(length))

    def friend_help_task_risk(self, friend_info):
        print('开始冒险互助--->>>')
        # try:
        params = {
            'userId': friend_info['userId'],
            'type': 0x1,
            'randomId': self.randomString(32, '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
        }
        sign_header = self.gen_sign(params)
        url = f'{self.base_url}/friend-help/help'
        response = self.s.get(url, headers=sign_header,params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            if data.get('data'):
                self.can_help_risk = False
                print(f"冒险助力账号[{friend_info['index']}][{friend_info['name']}]成功---√")
            else:
                message = data.get('message', '').replace('\r', '').split('\n')
                message = ','.join(filter(lambda x: x, message))
                print(f"冒险助力账号[{friend_info['index']}][{friend_info['name']}]失败{message}")
                if '助力次数' in message:
                    self.can_help_risk = False
                elif '挂机时间已完成' in message:
                    friend_info['need_help_risk'] = False
        # except Exception as e:
        #     print(e)

    def friend_help(self, friend_info):
        print(f'开始阳光互助--->>>')
        # try:
        params = {
            'userId': friend_info['userId'],
            'type': 0x0,
            'randomId': self.randomString(32, '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')
        }
        sign_header = self.gen_sign(params)
        url = f'{self.base_url}/friend-help/help'
        response = self.s.get(url, headers=sign_header,params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            if data.get('data'):
                # print(f"请求助力账号[{friend_info['index']}][{friend_info['name']}] 成功---√")
                self.task_doHelpTask(friend_info)
            else:
                message = data.get('message', '').replace('\r', '').split('\n')
                message = ','.join(filter(lambda x: x, message))
                print(f"请求助力账号[{friend_info['index']}][{friend_info['name']}] 失败: {message}")
                if '助力次数' in message:
                    self.can_help_task = False
        # except Exception as e:
        #     print(e)

    def friend_findRecommend(self):
        print(f'查询添加好友列表--->>>')
        try:
            url = f'{self.base_url}/friend/findRecommend'
            sign_header = self.gen_sign()
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print(f'查询添加好友列表成功---√')
                for user_info in data.get('data', []):
                    if not self.can_add_friend:
                        print('好友已满')
                        break
                    # if len(list(filter(lambda user: user['userId'] == user_info['userId'], self.user_list))) > 0:
                    #     continue
                    self.friend_addFriend(user_info)
                    # self.friend_deleteFriend(user_info)
            else:
                message = data.get('message', '')
                print(f'查询添加好友列表失败{code}]: {message}')
        except Exception as e:
            print(e)

    def friend_addFriend(self, user_data):
        print(f'添加好友--->>>')
        try:
            friend_user_id = user_data['userId']
            params = {'friendUserId': friend_user_id}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/friend/addFriend'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print(f"添加好友[{user_data['nickName']}]成功---√")
            else:
                message = data.get('message', '')
                print(f'添加好友{user_data["nickName"]}失败{code}]: {message}')
                if message and '达到好友上限' in message:
                    self.can_add_friend = False
        except Exception as e:
            print(e)

    def friend_deleteFriend(self, user_data):
        print(f'删除好友--->>>')
        try:
            friend_user_id = user_data['userId']
            params = {'friendUserId': friend_user_id}
            sign_header = self.gen_sign(params)
            url = f'{self.base_url}/friend/delFriend'
            response = self.s.get(url, headers=sign_header, params=params)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print(f"删除好友[{user_data['nickName']}]成功---√")
            else:
                message = data.get('message', '')
                print(f'删除好友{user_data["nickName"]}失败{code}]: {message}')
        except Exception as e:
            print(e)

    def friend_findFriend(self):
        print(f'\n查询好友列表--->>>')
        try:
            sign_header = self.gen_sign()
            url = f'{self.base_url}/friend/findFriend'
            response = self.s.get(url, headers=sign_header)
            data = response.json()
            code = data.get('code', -1)
            if code == 0:
                print(f'查询好友列表成功---√')
                friend_list = data.get('data', {}).get('friendList', [])
                friend_list.sort(key=lambda x: x['gold'], reverse=True)
                for friend in friend_list:
                    if friend.get('stealFlag', False):
                        if not self.friend_stealGold(friend):
                            break

            else:
                message = data.get('message', '')
                print(f'查询好友列表失败[{str(code)}]:{message}')
        except Exception as e:
            print(e)

    def get_CapCode(self, slideImgInfo):
        slidingImage = slideImgInfo.get('slidingImage', None)
        backImage = slideImgInfo.get('backImage', None)
        dddddocr_api = os.environ.get('OCR_API',False)
        if not dddddocr_api:
            print('未定义变量【OCR_API】\n取消验证码识别\n搭建方式：https://github.com/CHERWING/CHERWIN_OCR')
            return False
        if slidingImage and backImage:
            data = {
                "slidingImage": slidingImage,
                "backImage": backImage
            }
            response = requests.post(f"{dddddocr_api}/capcode", data=json.dumps(data),headers={'Content-Type': 'application/json'})
            print(response.json())
            self.capcode = response.json().get('result','')
            if self.capcode:
                return True
            else:
                return False

    def get_CapCode_local(self, slideImgInfo):
        slidingImage = slideImgInfo.get('slidingImage', None)
        backImage = slideImgInfo.get('backImage', None)
        if slidingImage and backImage:
            self.capcode =CHERWIN_TOOLS.CAPCODE(slidingImage,backImage)
            if self.capcode:
                return True
            else:
                return False

    def friend_stealGold(self, user_data):
        print(f'偷取好友--->>>')
        # try:
        friend_user_id = user_data['userId']
        params = {'friendUserId': friend_user_id}
        sign_header = self.gen_sign(params)
        url = f'{self.base_url}/friend/stealGold'
        response = self.s.get(url, headers=sign_header, params=params)
        data = response.json()
        code = data.get('code', -1)
        if code == 0:
            print(f"偷取好友[{user_data['nickName']}]: 阳光x{data.get('data', 0)}")
            return True
        elif code == 4000:

            slideImgInfo = data.get('data', {}).get('slideImgInfo', None)
            validateCount = data.get('data', {}).get('validateCount', None)
            if slideImgInfo and validateCount:
                print(f"偷取好友[{user_data['nickName']}]，需要滑块验证")
                self.can_stealGold = False
                if self.get_CapCode(slideImgInfo):
                    if self.checkUserCapCode():
                        self.friend_stealGold(user_data)
            else:
                print(f"偷取好友[{user_data['nickName']}]验证码上限")
                self.can_stealGold = False
        else:
            message = data.get('message', '')
            print(f"偷取好友[{user_data['nickName']}]阳光失败[{str(code)}]: {message}")

            return False
        # except Exception as e:
        #     print(e)

    def checkUserCapCode(self):
        print(f'提交验证码--->>>')
        # try:
        print(f'验证码：{self.capcode}')
        params = {'xpos':self.capcode}
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

    def risk_task(self):
        self.take_risk_get()
        self.take_risk_online()
        self.take_risk_reward()
        print(f'可以冒险【{self.risk_num}】次')
        while self.risk_num > 0 and self.can_go_risk == True:
            self.take_risk_go()
            time.sleep(2)

    def land_task(self):
        self.user_land_get()
        if self.all_land_unlock and self.all_role_unlock:
            pass
        for land_number, land_info in self.land.items():
            # print(land_number)
            # print(land_info)
            if land_info['status'] == 0:
                continue
            step, use_sun_count, left_sun_count = land_info['step'], land_info['useSunCount'], land_info['leftSunCount']

            total_sun_count = (use_sun_count if use_sun_count else 0) + (left_sun_count if left_sun_count else 0)

            print(f"\n---[{land_info['no']}号土地]---\n{self.group_step[step-1]},阶段{step}, 进度{use_sun_count}/{total_sun_count}")

            self.refresh_land_step = True
            while self.refresh_land_step:
                self.refresh_land_step = False
                if land_info['status'] == 0:
                    break
                if step == 0:
                    self.user_land_sow(land_info)
                else:
                    if left_sun_count == 0:
                        if step == 5:
                            self.user_land_result(land_info)
                        else:
                            current_time = int(time.time() * 1000)
                            if current_time >= (land_info['sunTime'] + land_info['sunTimestamp']) * 1000:
                                self.user_land_level(land_info)
                    else:
                        if self.sun >= land_info['needSun']:
                            current_time = int(time.time() * 1000)
                            if current_time >= (land_info['sunTime'] + land_info['sunTimestamp']) * 1000:
                                self.user_land_sun(land_info)
                # time.sleep(2)

    def userTask(self):
        print('\n--------------- 开始日常任务 ---------------')
        wait_time = random.randint(1000, 3000) / 1000.0  # 转换为秒
        if not self.Login_res:
            return False
        self.userInfo_autoSun()

        self.userInfo_get()

        self.task_get()

        self.user_role_get()

        self.risk_task()

        self.land_task()

        self.steal_task()

        self.userInfo_get(END=True)
        new_data = {
            self.userId: {
                'userId': self.userId,
                'task_id': self.task_id,
                'task_can_help': self.can_help_task,
                'task_need_help': self.need_help_task,
                'task_progress': self.task_progress,
                'task_max_progress': self.task_max_progress,
                'role_id': self.role_id,
                'role_can_help': self.can_help_unlock,
                'role_need_help': self.need_help_unlock,
                'role_progress': self.role_progress,
                'role_max': self.role_max,
                'risk_can_help': self.can_help_risk,
                'risk_need_help': self.need_help_task,
                'can_go_risk': self.can_go_risk,
                'can_add_friend': self.can_add_friend

            }
        }
        # print(new_data)
        USER_INFO.update(new_data)
        CHERWIN_TOOLS.SAVE_INVITE_CODE(f"INVITE_CODE/{ENV_NAME}_INVITE_CODE.json", new_data)
        self.steal_task()
        self.sendMsg()
        return True

    def helpEachOther(self):
        print('--------------- 开始互助 ---------------')

        if not self.Login_res:
            return False

        self.userInfo_get()

        if self.user_index == 1:
            print('第一个账号助力作者--->>>')
            data_li = AuthorCode
            help_type = '作者'
        else:
            print('其余账号互助--->>>')
            json_data = self.load_json()
            data_li = list(json_data.values())
            help_type = '本地'


        # print(data_li)
        for index, code_li in enumerate(data_li):
            # print(f"Index: {index}")
            # print(f"Data: {code_li}")
            if code_li.get('userId','') == self.userId:
                continue
            task_need_help = code_li.get("task_need_help", '')
            role_need_help = code_li.get("role_need_help", '')
            risk_need_help = code_li.get("task_can_help", '')
            code_li["index"] = index+1
            print(f'\n------助力{help_type}账号【{index+1}】开始------')
            # print(code_li)
            # 冒险助力
            if self.can_help_risk and risk_need_help:
                self.friend_help_task_risk(code_li)
            else:
                print(f'好友冒险助力已完成或冒险助力次数已耗尽')

            # 解锁角色助力
            if self.can_help_unlock and role_need_help:
                self.user_role_friendHelpUnlock(code_li)
            else:
                print(f'好友解锁角色助力已完成或解锁角色助力次数已耗尽')

            # 阳光助力
            if self.can_help_task and task_need_help:
                self.friend_help(code_li)
            else:
                print(f'阳光助力次数已耗尽')

            print(f'------助力{help_type}账号【{index+1}】结束------')
            time.sleep(1)


        new_data = {
            self.userId: {
                'task_can_help': self.can_help_task,
                'role_can_help': self.can_help_unlock,
                'risk_can_help': self.can_help_risk
            }
        }
        CHERWIN_TOOLS.SAVE_INVITE_CODE(f"INVITE_CODE/{ENV_NAME}_INVITE_CODE.json", new_data)
        self.sendMsg(True)
        return True

    def steal_task(self, count=5):
        if not self.Login_res:
            return False
        json_data = self.load_json()
        self.can_add_friend = json_data.get(self.userId, {}).get('can_add_friend', '')
        for i in range(count):
            if self.can_add_friend:
                self.friend_findRecommend()
            time.sleep(2)
        self.friend_findFriend()
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
    global CHERWIN_TOOLS,ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode
    import CHERWIN_TOOLS
    ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode = CHERWIN_TOOLS.main(APP_NAME, local_script_name, ENV_NAME,local_version)


if __name__ == '__main__':
    APP_NAME = '统一茄皇'
    ENV_NAME = 'TYQH'
    CK_NAME = 'thirdId@wid'
    CK_URL = '.../public/api/login'
    print(f'''
✨✨✨ {APP_NAME}脚本 ✨✨✨
✨ 功能：
      日常任务
      互助任务
✨ 抓包步骤：
      统一快乐星球小程序-活动
      开始抓包-茄皇的家第三期
      抓{CK_URL}取{CK_NAME}
✨ 设置青龙变量：
export {ENV_NAME}= '{CK_NAME}'多账号#分割或&
export OCR_API= 'http://localhost:3721' 
✨ 由于青龙python版本问题无法直接使用dddocr需要自行搭建API，搭建方式：https://github.com/CHERWING/CHERWIN_OCR
✨ 如果你的环境可以安装dddocr库则可以替换代码内的【self.get_CapCode】为【self.get_CapCode_local】
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ 推荐定时：25 10-22/2 * * *
✨ 第一个账号助力作者，其余互助
✨✨✨ @Author CHERWIN✨✨✨
                ''')

    local_script_name = os.path.basename(__file__)
    local_version = '2024.05.15'
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
    token = ENV if ENV else token
    if not token:
        print(f"未填写{ENV_NAME}变量\n青龙可在环境变量设置 {ENV_NAME} 或者在本脚本文件上方将{CK_NAME}填入token =''")
        exit()
    tokens = CHERWIN_TOOLS.ENV_SPLIT(token)
    # print(tokens)
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
        access_token = []
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).userTask()
            if not run_result: continue

        for index, infos in enumerate(tokens):
            run_result =RUN(infos, index).helpEachOther()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
