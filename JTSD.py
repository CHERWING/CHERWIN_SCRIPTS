# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# -------------------------------
# cron "0 5 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('极兔速递小程序签到')
import json
import os
import random
import time
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
        self.token = split_info[0]
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

        self.headers =  {
            "Host": "applets.jtexpress.com.cn",
            "authtoken": self.token,
            "xweb_xhr": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/8555",
            "content-type": "application/json;charset=UTF-8",
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://servicewechat.com/wxe37801988179d0a5/316/page-frame.html",
            "accept-language": "zh-CN,zh;q=0.9"
        }

        self.baseUrl = 'https://applets.jtexpress.com.cn/'
        self.news_List = []
        self.list_index = 0
        self.isFirstTask = True

    def qureyMyselfGrow(self):
        Log('>>>>>>获取用户信息')
        response = self.s.get(f'{self.baseUrl}/applets/user/qureyMyselfGrow?', headers=self.headers)
        data_info = response.json()
        # print(point_info)
        if data_info.get('succ','') == True:
            data = data_info.get('data', {})
            mobile = data.get('mobile', '')
            mobile = mobile[:3] + "*" * 4 + mobile[7:]
            id = data.get('id', '')
            memberId = data.get('memberId', '')
            growValue = data.get('growValue', '')
            nextStartGrow = data.get('nextStartGrow', '')
            Log(f'获取用户[{self.index}]信息成功！\n手机号：【{mobile}】\n用户ID：【{memberId}】\n成长值：【{growValue}/{nextStartGrow}】')
            return True
        else:
            print('获取用户信息失败！可能token失效了')
            return False

    def addActionRecord(self):
        print('>>>>>>进入签到详情')
        json_data =  {
            "eventTimestamp": int(time.time() * 1000),
            "pagePath": "packageA/signIn/index",
            "reportAddress": "",
            "reportLocation": "",
            "phoneModel": "microsoft",
            "eventType": "enter_signIn",
            "elementContent": "",
            "elementEventName": "进入签到详情",
            "elementCode": 2
        }
        response = self.s.post(f'{self.baseUrl}/applets/user/addActionRecord', headers=self.headers,json=json_data)
        data_info = response.json()
        # print(point_info)
        if data_info.get('succ','') == True:
            msg=data_info.get('msg','')
            print(f'{msg}')
            return True
        else:
            print('进入签到详情失败！可能token失效了')
            return False
    def sign(self):
        print('>>>>>>开始签到')
        json_data =  {}
        response = self.s.post(f'{self.baseUrl}/applets/user/sign', headers=self.headers,json=json_data)
        data_info = response.json()
        # print(point_info)
        if data_info.get('succ','') == True:
            msg=data_info.get('msg','')
            day=data_info.get('data', {}).get('day', {})
            Log(f'累计签到【{day}】天')
            return True
        else:
            Log('签到失败')
            return False

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.qureyMyselfGrow():
            self.addActionRecord()
            self.sign()
            self.sendMsg()
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
    APP_NAME = '极兔速递小程序'
    ENV_NAME = 'JTSD'
    CK_NAME = 'authtoken'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找URl请求头带[{CK_NAME}]
      复制里面的[{CK_NAME}]参数值
参数示例：eyJhbGciOiJIUzUxMiJ9.eyJnZW5lcmF0ZVRpbWUixxxxxx
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