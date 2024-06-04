# !/usr/bin/python3
# -- coding: utf-8 --
#  （包含：甄稀冰淇淋，金典SATINE、活力伊利）
# cron "5 9 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('伊利系列小程序')
import json
import os
import random
import time
from datetime import datetime, time as times
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


class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        self.access_token = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            print('检测到设置了UID')
            print(last_info)
            self.send_UID = last_info
        self.index = index + 1
        # print(self.access_token)
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/8555'
        # if ENV_NAME == 'YL_ZXBQL':
        #     appid = "wx06af0ef532292cd3"
        #     scene = "1037"
        #     scene = "1037"
        self.headers = {
                "Host": "msmarket.msx.digitalyili.com",
                "register-source": "",
                "access-token": self.access_token,
                "forward-appid": "wx06af0ef532292cd3",
                "source-type": "",
                "Content-Type": "application/json",
                "atv-page": "",
                "scene": "1037",
                "xweb_xhr": "1",
                "User-Agent": self.UA,
                "Accept": "*/*",
                "tenant-id": "1718857849685876737",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://servicewechat.com/wxf32616183fb4511e/564/page-frame.html",
                "Accept-Language": "zh-CN,zh;q=0.9"
            }
        self.s = requests.session()
        self.s.verify = False
        self.baseUrl = 'https://msmarket.msx.digitalyili.com/gateway/api/member/'


    def make_request(self, url, method='post', headers={}, data={}, params=None):
        if headers == {}:
            headers = self.headers
        try:
            if method.lower() == 'get':
                response = self.s.get(url, headers=headers, verify=False, params=params)
            elif method.lower() == 'post':
                response = self.s.post(url, headers=headers, json=data, params=params, verify=False)
            else:
                raise ValueError("不支持的请求方法❌: " + method)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常❌：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法❌：", e)
        except Exception as e:
            print("发生了未知错误❌：", e)

    def get_user_info(self):
        act_name = '获取用户信息'
        Log(f'\n====== {act_name} ======')
        url = f"https://msmarket.msx.digitalyili.com/gateway/api/auth/account/user/info"
        response = self.make_request(url,method='get')
        if response.get('status', False):
            print(f'{act_name}成功！✅')
            site = {'1520': "活力伊利", '1577': "活力伊利", '1160': '金典SATINE', '1068': '甄稀冰淇淋','1130': '金典有机生活+'}
            registerSource = response.get('data')['registerSource']
            Log(f'当前Source：【{registerSource}】')
            siteName = site.get(registerSource,False)
            if not siteName:
                Log(f'当前小程序名称识别失败')
            Log(f'当前token所属小程序：【{siteName}】')
            nickName = response.get('data')['nickName']
            mobile = response.get('data')['mobile']
            mobile = mobile[:3] + "*" * 4 + mobile[7:]
            Log(f">用户名：{nickName}\n>手机号：{mobile}")
            return True
        elif not response:
            print(f">账号 {self.index}: ck过期 请重新抓取 access-token")
            return False
        else:
            print(response)
            return False

    def get_Point(self,END=False):
        act_name = '获取积分信息'
        if not END:Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}point"
        response = self.make_request(url,method='get')
        if response.get('status', False):
            point = response.get('data')
            print(f'{act_name}成功！✅')
            if END:
                Log(f'执行后积分:【{point}】')
            else:
                Log(f'当前积分:【{point}】')
            return True
        else:
            print(response)
            return False

    def daily_sign(self):
        act_name = '签到'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}daily/sign"
        response = self.make_request(url)
        if response.get('status', False):
            data = response.get('data',{})
            dailySign = data.get('dailySign', None)
            if dailySign != None:
                point = dailySign.get('bonusPoint', '')
                print(f'{act_name}成功！✅')
                Log(f'获得积分:【{point}】')
            return True
        else:
            print(response)
            return False

    def get_sign_status(self):
        act_name = '获取签到信息'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}sign/status"
        response = self.make_request(url,method='get')
        if response.get('status', False):
            data = response.get('data',{})
            signed = data.get('signed','')
            signedDays = data.get('signedDays','')
            monthSignDays = data.get('monthSignDays','')
            monthDays = data.get('monthDays','')
            weekSignDays = data.get('weekSignDays','')
            print(f'{act_name}成功！✅')
            Log(f'今日:【{"已签到" if signed else "未签到"}】')
            print(f'累计签到:【{signedDays}】天')
            print(f'周签:【{weekSignDays}】天')
            print(f'月签:【{monthSignDays}/{monthDays}】天')
            if not signed:
                self.daily_sign()
            return True
        else:
            print(response)
            return False


    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")

        if self.get_user_info():
            random_delay()
            self.get_Point()
            random_delay()
            self.get_sign_status()
            random_delay()
            self.get_Point(True)


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
    ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode = CHERWIN_TOOLS.main(APP_NAME, local_script_name, ENV_NAME,local_version)


if __name__ == '__main__':
    APP_NAME = '伊利系列小程序'
    ENV_NAME = 'YLXL'
    CK_URL = 'msmarket.msx.digitalyili.com请求头'
    CK_NAME = 'access-token'
    CK_EX = 'wTUhu5IlL9uQDRelKgMRbao2bxii+O8+4FffOnxxxxxxx'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ （包含：甄稀冰淇淋，金典SATINE、活力伊利）
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
✨ 推荐cron：5 9 * * *
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
