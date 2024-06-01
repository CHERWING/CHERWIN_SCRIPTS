# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# ✨✨✨ @Author CHERWIN✨✨✨
# -------------------------------
# cron "0 6 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('中通快递小程序签到')

import os
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

class RUN:
    def __init__(self,info,index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        token = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            print('检测到设置了UID')
            print(last_info)
            self.send_UID = last_info
        self.index = index + 1
        self.s = requests.session()
        self.s.verify = False
        self.token = f'ECO_TOKEN={token};'
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/9079',
                'Cookie':self.token,
                'Referer': 'https://servicewechat.com/wxa1ebeeb0ed47f0b2/633/page-frame.html'
            }

    def do_request(self, method, url, params=None, data=None, headers=None):
        if not headers:
            headers = self.headers
        try:
            response = self.s.request(method, url, params=params, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求错误: {e}")
            return None

    def login(self):
        try:
            data= {
                "code": self.token,
                "loginType": "AUTH_CODE_SESSION_KEY_WECHAT_MINI",
                "sysCode": "WECHAT_MINI"
            }
            response = self.do_request('POST', 'https://www.deppon.com/ndcc-gwapi/userService/eco/user/login',data=data)
            if response and response.get('status') == 'success':
                mobile = response['result']['mobile']
                self.mobile = mobile[:3] + "*" * 4 + mobile[7:]
                Log(f'\n手机号：【{self.mobile}】')
                return self.generate_tmp_token()
            else:
                Log(f"查询账户失败: {response.get('message')}")
                return False
        except Exception as e:
            print(f"查询账户异常: {e}")
            return False

    def queryUserInfo(self):
        try:
            self.headers['Content-Type'] = 'application/json'
            self.headers['Accept'] = '*/*'
            response = self.do_request('GET', 'https://www.deppon.com/ndcc-gwapi/userService/eco/user/secure/queryUserInfo')
            if response and response.get('message') == 'ok':
                # print(response)
                result = response.get('result', {})
                phone = result.get('mobile', '')
                self.mobile = phone[:3] + "*" * 4 + phone[7:]
                self.userName = result.get('userName', '')
                Log(f'\n用户名：【{self.userName}】\n手机号：【{self.mobile}】')
                return True
            else:
                Log(f"登录验证失败: {response}")
                return False
        except Exception as e:
            print(f"登录验证异常: {e}")
            return False

    def generate_tmp_token(self):
        try:
            response = self.do_request('GET',              'https://www.deppon.com/ndcc-gwapi/userService/eco/user/token/secure/generateTmpToken')
            if response and response.get('status') == 'success':
                print(f'临时Token获取成功！')
                return self.login_verify(response['result'])
            else:
                print(f"获取临时token失败: {response}")
                return False
        except Exception as e:
            print(f"获取临时token异常: {e}")
            return False

    def login_verify(self, code):
        try:
            data = {'code': code, 'flag': True}
            self.headers['Content-Type'] = 'application/json'
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/login/verify', data=data)
            if response and response.get('code') == 200:
                # print(response)
                Log(f"登录验证成功！")
                data = response.get('data', {})
                self.token = data.get('token','')
                self.phone = data.get('mobile','')
                self.headers['token'] = self.token
                self.headers['mobile'] = self.phone
                # print(f"PHONE：【{self.phone}】")
                # print(f"TOKEN：【{self.token}】")
                return True
            else:
                Log(f"登录验证失败: {response}")
                return False
        except Exception as e:
            print(f"登录验证异常: {e}")
            return False

    def getSvipNewestInfo(self,end="执行前"):
        print('\n获取用户最新信息------>>>')
        try:
            # data ={"phone":self.phone}
            response = self.do_request('GET', 'https://www.deppon.com/ndcc-gwapi/memberService/eco/member/grade/secure/getSvipNewestInfo')
            if response and response.get('status') == "success":
                data = response.get('result', {})
                points = data.get('points', 0)
                Log(f'{end}积分：【{points}】')
            else:
                Log(f"获取用户最新信息失败: {response}")
                return None
        except Exception as e:
            print(f"获取用户最新信息异常: {e}")
            return None


    def signIn_info(self):
        print('获取签到信息------>>>')
        try:
            data = {"phone": self.phone}
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/deppon/signIn/info',data = data)
            if response and response.get('code') == 200:
                data = response.get('data', {})
                is_sign_in = data.get('isSignIn')
                sign_in_day = data.get('signInDay')
                record_dtos = data.get('recordDTOS')
                if not is_sign_in and record_dtos and record_dtos[0]:
                    self.remark = record_dtos[0].get('remark','')
                    self.name = record_dtos[0].get('name','')
                    self.taskRuleId = record_dtos[0].get('taskRuleId','')
                    self.signIn()
                else:
                    Log(f'[领券签到]今天已签到, 已签到{sign_in_day}天')
                return response['data']
            else:
                print(f"获取签到信息失败: {response}")
                return None
        except Exception as e:
            print(f"获取签到信息异常: {e}")
            return None

    def signIn(self):
        print('执行签到------>>>')
        try:
            data = {"phone": self.phone,'taskRuleId':self.taskRuleId}
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/deppon/signIn',data=data)
            if response and response.get('code') == 200:
                data = response.get('data', [])
                remarks = []
                for item in data:
                    if item.get('remark'):
                        remarks.append(item['remark'])
                remarks_str = ', '.join(remarks) if remarks else ''
                Log('签到成功: ' + remarks_str)
            else:
                print(f"签到失败: {response}")
        except Exception as e:
            print(f"签到异常: {e}")
            return None

    def points_signIn_info(self):
        print('获取积分签到信息------>>>')
        try:
            data = {"phone": self.phone}
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/deppon/points/task/signIn/info',data = data)
            if response and response.get('code') == 200:
                data = response.get('data', {})
                is_sign_in = data.get('isSignIn')
                sign_in_day = data.get('signInDay')
                sign_in_day_info = data.get('signInDayInfo')
                record_DTOS = data.get('recordDTOS', [])
                if is_sign_in:
                    for record in record_DTOS:
                        note = sign_in_day_info
                        self.name = record.get('name', '')
                        self.taskRuleId = record.get('taskRuleId', '')
                        self.task_receive(note)
                else:
                    Log(f'[积分签到]今天已签到, 已签到{sign_in_day}天')
            else:
                print(f"获取积分签到信息失败: {response}")
                return None
        except Exception as e:
            print(f"获取积分签到信息异常: {e}")
            return None

    def task_list(self):
        print('获取任务列表------>>>')
        try:
            data = {"phone": self.phone}
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/deppon/points/task/list',data = data)
            if response and response.get('code') == 200:
                data = response.get('data',{})
                taskList = data.get('taskList',[{}])
                for task in taskList:
                    self.taskRuleId = task.get('taskRuleId',0)
                    self.remark = task.get('remark','')
                    self.name = task.get('name','')
                    print(f'\n当前任务：【{self.name}】 taskRuleId：【{self.taskRuleId}】')
                    rightsClaimStatus = task.get('rightsClaimStatus',0)
                    if rightsClaimStatus == 0:
                        if self.taskRuleId in [8, 9, 11]:
                            print('任务不支持，跳过')
                            break
                        self.changeStatus()
                        self.task_receive()
                    elif rightsClaimStatus == 1:
                        self.task_receive()
                    else:
                        print('任务已完成！')
                return response['data']
            else:
                print(f"获取任务列表失败: {response}")
                return None
        except Exception as e:
            print(f"获取任务列表异常: {e}")
            return None

    def changeStatus(self):
        print('完成任务------>>>')
        try:
            data ={
                "phone":self.phone,
                "rightsClaimStatus":1,
                "taskRuleId":self.taskRuleId
                   }
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/deppon/points/task/changeStatus',data = data)
            if response and response.get('code') == 200:
                Log(f'完成任务：【{self.name}】成功！')
                return response['msg']
            else:
                print(f"完成任务【{self.name}】失败: {response}")
                return None
        except Exception as e:
            print(f"获取SVIP最新信息异常: {e}")
            return None

    def task_receive(self,note=None):
        print('领取奖励------>>>')
        try:
            data = {"phone": self.phone, "taskRuleId": self.taskRuleId,"ruleId":self.taskRuleId,"note":note}
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/deppon/points/task/receive',data = data)
            if response and response.get('code') == 200:
                Log(f'领取：【{self.name}】任务奖励成功！')
                return response['msg']
            else:
                print(f"领取【{self.name}】任务奖励失败: {response}")
                return None
        except Exception as e:
            print(f"领取任务奖励异常: {e}")
            return None

    def lottery(self):
        try:
            data = {"mobile": self.phone,"gameId":'67'}
            response = self.do_request('POST', 'https://mas.deppon.com/admin/envelops/game/lottery',data = data)

            if response and response.get('code') == 0:
                # print(response)
                data = response.get('data','')
                name = data.get('name','')
                Log(f'抽奖成功,获得：{name}')
                return
            else:
                print(f"抽奖失败: {response}")
                return None
        except Exception as e:
            print(f"获取任务列表异常: {e}")
            return None

    def lottery_query2(self):
        print('查询抽奖次数')
        try:
            data = {"phone": self.phone}
            response = self.do_request('POST', 'https://mas.deppon.com/crm-api/points/balance/query2',data = data)

            if response and response.get('code') == 200:
                # print(response)
                data = {} if response.get('data', {})==None else response.get('data', {})
                self.pointsAvailableValue = data.get('pointsAvailableValue', 0)
                print(f'可以抽奖【{self.pointsAvailableValue}】次')
                while self.pointsAvailableValue >0:
                    self.lottery()
                    self.pointsAvailableValue -= 1

                return response['msg']
            else:
                print(f"查询抽奖失败: {response}")
                return None
        except Exception as e:
            print(f"查询抽奖次数异常: {e}")
            return None



    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        # if self.login():

        if self.queryUserInfo():
            self.generate_tmp_token()
            self.getSvipNewestInfo()
            self.signIn_info()
            self.points_signIn_info()
            self.task_list()
            self.lottery()
            self.getSvipNewestInfo('执行后')
            self.sendMsg()
            return True
        else:
            self.sendMsg()
            return False

    def sendMsg(self):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME)
            print(push_res)
            return True


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


if __name__ == '__main__':
    APP_NAME = '德邦快递小程序'
    ENV_NAME = 'DBKD'
    CK_NAME = 'ECO_TOKEN=里面的值;'
    CK_URL = 'https://www.deppon.com/ndcc-gwapi/userService/eco/user/secure/queryUserInfo'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找{CK_URL}请求Cookies里面的[{CK_NAME}]
      复制里面的[{CK_NAME}]参数值
参数示例：0f1bjLFa1ZdedHxxxxxxxx
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：0 6 * * *
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
                print('脚本依赖下载失败，请到https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/CHERWIN_TOOLS.py下载最新版本依赖')
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
            run_result = RUN(infos, index).main()
            if not run_result: continue
        # if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
