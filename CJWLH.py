# !/usr/bin/python3
# -- coding: utf-8 --
# cron "20 8 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('春茧未来荟小程序')
import hashlib
import json
import os
import random
import time
from datetime import datetime, time as times
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

IS_DEV = os.path.isfile('DEV_ENV.py')
if IS_DEV:import DEV_ENV

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


class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        self.X_XSRF_TOKEN = split_info[0]
        self.cookies = split_info[1]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            print('检测到设置了UID')
            print(last_info)
            self.send_UID = last_info
        self.index = index + 1
        # print(self.access_token)
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129"
        PROXY_URL = os.environ.get(f'{ENV_NAME}_PROXY_URL', False)
        if PROXY_URL:
            print(f'【已设置反代】：{PROXY_URL}✅')
            self.baseUrl = f'{PROXY_URL}szbay/api/services/app/'
        else:
            print(
                f'【未设置反代，使用官方域名】❌ 脚本如果报错（unsafe legacy renegotiation）请自行搭建反代，搭建方法见：https://github.com/CHERWING/CHERWIN_SCRIPTS/tree/main/Cloudflare%20Workers%20Proxy(代理变量名【{ENV_NAME}_PROXY_URL】)')
            self.baseUrl = 'https://program.springcocoon.com/szbay/api/services/app/'

        self.headers ={
            'Host': self.baseUrl.split('/')[2],
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With':'XMLHttpRequest',
            'Accept-Language':'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding':'gzip, deflate, br',
            'X-XSRF-TOKEN':self.X_XSRF_TOKEN,
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'https://program.springcocoon.com',
            'site':'program.springcocoon.com',
            'User-Agent':self.UA,
            'Referer':'https://program.springcocoon.com/szbay/AppInteract/SignIn/Index?isWeixinRegister=true',
            'Connection':'keep-alive',
            'Cookie':self.cookies
        }
        self.s = requests.session()
        self.s.verify = False
        # self.baseUrl = 'https://proxy.cherwin.workers.dev/szbay/api/services/app/'

    def make_request(self, url, method='post', headers={}, json_data={}, params=None, data=None):
        if headers == {}:
            headers = self.headers
        try:
            if method.lower() == 'get':
                response = self.s.get(url, headers=headers, verify=False, params=params)
            elif method.lower() == 'post':
                response = self.s.post(url, headers=headers, json=json_data, data=data, params=params, verify=False)
            else:
                raise ValueError("不支持的请求方法❌: " + method)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常❌：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法❌：", e)
        except Exception as e:
            print("发生了未知错误❌：", e)

    def get_user_info(self, END=False):
        act_name = '获取用户信息'
        if END:
            Log(f'\n====== {act_name} ======')
        else:
            print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}CRCWeixinEmpMerge/QueryMergeDataAsync"
        data = {
            'isGetEmpMoney': 'true',
            'isGetEmpPoint': 'true',
            'isGetEmpGrowth': 'true',
            'isGetCouponNum': 'false',
            'isShowPerfectEmpInfo': 'false',
            'isShowSignIn': 'false',
            'isShowWeixinEmpSubscribe': 'false',
        }
        response = self.make_request(url, data=data)

        if response.get('result', False) != False:
            print(f'{act_name}成功！✅')
            result = response.get('result', {})
            empID = result.get('empID', '')
            empDisplayName = result.get('empDisplayName', '')
            phone = result.get('phone', '')
            empPoint = result.get('empPoint', '')
            mobile = phone[:3] + "*" * 4 + phone[7:]
            if END:
                Log(f"> 执行后积分：{empPoint}")
            else:
                Log(f"> 用户名：{empDisplayName}\n> 手机号：{mobile}\n> 当前积分：{empPoint}")
            return True
        elif not response:
            print(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False


    def GetSignInRecordAsync(self):
        act_name = '获取签到状态'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}SignInRecord/GetSignInRecordAsync"
        data = {
            'id': '6c3a00f6-b9f0-44a3-b8a0-d5d709de627d',
            'webApiUniqueID': '54f08e2f-c832-8b82-8077-4473aea84800'
        }
        response = self.make_request(url, data=data)

        if response.get('result', False) != False:
            print(f'{act_name}成功！✅')
            result = response.get('result', {})
            isSignInToday = result.get('isSignInToday', '')
            if isSignInToday:
                Log(f"> 今日已签到！✅")
            else:
                Log(f"> 今日未签到！❌")
                self.SignInAsync()
            return True
        elif not response:
            print(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False


    def SignInAsync(self):
        act_name = '签到'
        Log(f'====== {act_name} ======')
        url = f"{self.baseUrl}SignInRecord/SignInAsync"
        data = {
            'id': '6c3a00f6-b9f0-44a3-b8a0-d5d709de627d',
            'webApiUniqueID': 'f2cca2a7-c327-1d76-d375-ec92cdd296cd'
        }
        response = self.make_request(url, data=data)
        success = response.get('success', False)
        if success != False:
            result = response.get('result', {})
            point = result.get('listSignInRuleData', [])[0]['point']
            print(f'{act_name}成功！✅')
            Log(f'> 获得【{point}】万象星')
            return True
        elif success == False:

            error = response.get('error', {})
            msg = error.get('message', '')
            print(f'> {act_name}失败！❌')
            print(f'> 【{msg}】')
            return False
        else:
            print(response)
            return False


    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.get_user_info():
            self.GetSignInRecordAsync()
            # self.SignInAsync()
            self.sendMsg()
            return True
        else:
            self.sendMsg()
            return False

    def sendMsg(self):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME)
            print(push_res)


def random_delay(min_delay=1, max_delay=5):
    """
    在min_delay和max_delay之间产生一个随机的延时时间，然后暂停执行。
    参数:
    min_delay (int/float): 最小延时时间（秒）
    max_delay (int/float): 最大延时时间（秒）
    """
    delay = random.uniform(min_delay, max_delay)
    print(f">本次随机延迟：【{delay:.2f}】 秒.....")
    time.sleep(delay)


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
    APP_NAME = '春茧未来荟小程序'
    ENV_NAME = 'CJWLH'
    CK_URL = 'program.springcocoon.com请求头'
    CK_NAME = 'X-XSRF-TOKEN@Cookie'
    CK_EX = 'ZMPwg2nr-kMV0HQMTNtmxxxxxxxxxxxxxxxxxxxxxxxxx@ASP.NET_SessionId=l2cxxxxxxxxxxx'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ 功能：
        积分签到
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找{CK_URL}{CK_NAME}
参数示例：{CK_EX}
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：20 8 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.06.05'
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
            run_result = RUN(infos, index).main()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
