# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# ✨ 推荐cron：0 6 * * *
# ✨✨✨ @Author CHERWIN✨✨✨
# -------------------------------
# cron "0 6 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('中通快递小程序签到')

import os
from os import path
import requests
import hashlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# import CHERWIN_TOOLS
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
        self.openId = split_info[0]
        self.uid = split_info[1]
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

        self.UA = 'Mozilla/5.0 (Linux; Android 14; Mi14 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230701 MMWEBID/8701 MicroMessenger/8.0.40.2420(0x28002858) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wx1ddeb67115f30d1a'
        self.headers = {
            'Host': 'superapp-public.kiwa-tech.com',
            'User-Agent': self.UA ,
            "_haidilao_app_token": "",
            "content-type": "application/json",
            "xweb_xhr": "1",
            "appid": "15",
            "appversion": "3.67.0",
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://servicewechat.com/wx1ddeb67115f30d1a/121/page-frame.html",
            "accept-language": "zh-CN,zh;q=0.9"
        }
    def do_request(self,  url , method='POST', params=None, data=None, headers=None):
        if not headers:
            headers = self.headers
        try:
            response = self.s.request(method, url, params=params, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求错误: {e}")
            return None

    def wechatLogin(self):
        print('>>>>>>登陆获取token')
        try:
            data = {
                "type": 1,
                "country": "CN",
                "codeType": 1,
                "business": "登录",
                "terminal": "会员小程序",
                "openId": self.openId,
                "uid": self.uid
            }
            response = self.do_request( 'https://superapp-public.kiwa-tech.com/api/gateway/login/center/login/wechatLogin',data =data)
            if response and response.get('success') == True:
                data = response.get('data',{})
                id = data.get('id','')
                token = data.get('token','')
                self.haidilao_app_token=token
                self.headers['_haidilao_app_token'] = token
                Log(f'ID：【{id}】')
                return True
            else:
                print(f"登陆获取token失败: {response}")
                return False
        except Exception as e:
            print(f"登陆获取token异常: {e}")
            return False


    def queryMemberCacheInfo(self):
        Log('>>>>>>获取用户信息')
        try:
            data = {"type":1}
            response = self.do_request( 'https://superapp-public.kiwa-tech.com/activity/wxapp/applet/queryMemberCacheInfo',data =data)
            if response and response.get('success') == True:
                data = response.get('data',{})
                customerName = data.get('customerName','')
                mobile = data.get('mobile','')
                mobile = mobile[:3] + "*" * 4 + mobile[7:]
                coinNum = data.get('coinNum','')

                Log(f'用户名：【{customerName}】\n手机号：【{mobile}】\n捞币：【{coinNum}】')
                return True
            else:
                print(f"登陆获取token失败: {response}")
                return False
        except Exception as e:
            print(f"登陆获取token异常: {e}")
            return False


    def daily_sign_getAct(self):
        Log('>>>>>>获取签到信息')
        try:
            data = {"source":1}
            response = self.do_request( 'https://superapp-public.kiwa-tech.com/activity/daily/sign/getAct',data =data)
            if response and response.get('success') == True:
                data = response.get('data',{})
                memberSignFlag = data.get('memberSignFlag',False)
                if memberSignFlag:
                    print('已签到')
                else:
                    print('未签到')
                    self.signIn()

                return True
            else:
                print(f"登陆获取token失败: {response}")
                return False
        except Exception as e:
            print(f"登陆获取token异常: {e}")
            return False


    def queryFragment(self):
        try:
            self.headers['referer'] =f"https://superapp-public.kiwa-tech.com/app-sign-in/?SignInToken={self.haidilao_app_token}&source=MiniApp"

            response = self.do_request( 'https://superapp-public.kiwa-tech.com/activity/wxapp/signin/queryFragment')
            if response and response.get('success') == True:
                data = response.get('data',{})
                total = data.get('total','')
                expireDate = data.get('expireDate','').split()[0]
                today = data.get('today','').split()[0]

                Log(f'当前拥有：【{total}】拼图碎片')
                if expireDate == today:
                    Log('碎片今日到期，请及时兑换!!!!!')
                    Log('碎片今日到期，请及时兑换!!!!!')
                    Log('碎片今日到期，请及时兑换!!!!!')
                else:
                    Log(f'本期碎片失效时间：{expireDate}')
                return True
            else:
                print(f"获取拼图失败: {response}")
                return False
        except Exception as e:
            print(f"获取拼图异常: {e}")
            return False


    def signIn(self):
        try:
            data = {"signinSource": "MiniApp"}
            self.headers['referer'] =f"https://superapp-public.kiwa-tech.com/app-sign-in/?SignInToken={self.haidilao_app_token}&source=MiniApp"

            response = self.do_request( 'https://superapp-public.kiwa-tech.com/activity/wxapp/signin/signin',data = data)
            if response and response.get('success') == True:
                # data = response.get('data',{})
                # total = data.get('total','')
                Log(f'签到成功！')
                return True
            else:
                Log(f"签到失败: {response}")
                return False
        except Exception as e:
            print(f"签到异常: {e}")
            return False




    def signin_query(self):
        print('>>>>>>开始签到')
        try:
            self.headers['referer'] =f"https://superapp-public.kiwa-tech.com/app-sign-in/?SignInToken={self.haidilao_app_token}&source=MiniApp"

            response = self.do_request( 'https://superapp-public.kiwa-tech.com/activity/wxapp/signin/query')
            if response and response.get('success') == True:
                data = response.get('data',{})
                signinOr = data.get('signinOr',0)
                activityName = data.get('activityName',0)
                signinQueryDetailList = data.get('signinQueryDetailList',[{}])
                daycount = 0
                for day in signinQueryDetailList:
                    days = day.get('dailySigninStatus',1)
                    if days == 2:
                        daycount+=1
                if signinOr != 0 :
                    Log(f'已签到,本期累计签到【{daycount}】天')
                else:
                    Log(f'未签到,本期累计签到【{daycount}】天')
                    self.signIn()
                return True
            else:
                print(f"签到失败: {response}")
                return False
        except Exception as e:
            print(f"签到异常: {e}")
            return False


    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.wechatLogin():
            self.queryMemberCacheInfo()
            self.signin_query()
            self.queryFragment()
            self.sendMsg()
            return True
        else:
            self.sendMsg()
            return False
    def sendMsg(self):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME)
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
    APP_NAME = '海底捞小程序'
    ENV_NAME = 'HDL'
    CK_NAME = 'openId@uid'
    CK_URL= 'https://superapp-public.kiwa-tech.com/api/gateway/login/center/login/wechatLogin'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      签到
✨ 抓包步骤：
      打开抓包工具
      打开{APP_NAME}
      授权登陆
      找{CK_URL}的URl复制请求里面的body[{CK_NAME}]
      复制里面的[{CK_NAME}]参数值
参数示例：o4YwF5LIxxxxx@oF_Z5jh0Bwg_uZrODxxxxxxx
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
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)