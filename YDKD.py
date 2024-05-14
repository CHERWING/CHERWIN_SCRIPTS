# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : cherwin
# ✨✨✨ 韵达快递小程序签到✨✨✨
# ✨ 功能：
#       积分签到
# ✨ 抓包步骤：
#       打开韵达快递小程序
#       授权登陆
#       打开抓包工具
#       找URl请求头带openID
#       复制里面的openID参数值
# 参数示例：at965eoakumxxxxxxxx
# ✨ 设置青龙变量：
# export YDKD='openID参数值'多账号#或&分割
# export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
# ✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
# ✨ 推荐cron：0 6 * * *
# ✨✨✨ @Author CHERWIN✨✨✨
# -------------------------------
# cron "30 6 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('韵达快递小程序签到')
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
        self.headers = {
            'Host': 'op.yundasys.com',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6945',
            'Content-Type': 'application/json; charset=UTF-8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://op.yundasys.com/mb-ext-channel/index.html',
            'Accept-Language': 'zh-CN,zh'
        }

        self.baseUrl = 'https://op.yundasys.com/gateway/ydmb-integral/ydintegral/'
        self.news_List = []
        self.list_index = 0
        self.isFirstTask = True

    def get_point(self):
        Log('>>>>>>获取积分信息')
        json_data = {
            "channelId": "wxapp",
            "reqTime": int(time.time()),
            "accountSrc": "wxapp",
            "accountId": self.token
        }
        response = s.post(f'{self.baseUrl}member/integral/info', headers=self.headers,json=json_data)
        point_info = response.json()
        # print(point_info)
        if point_info['code']== 200:
            point=point_info['data']['total']
            userId=point_info['data']['userId']
            Log(f'>>当前用户：【{userId}】')
            Log(f'>>当前积分：【{point}】')
            return True
        else:
            Log('可能token失效了')
            return False

    def sign(self):
        Log('>>>>>>签到')
        json_data = {
            'channelId': 'wxapp',
            'itgType': 'sign',
            'reqTime': int(time.time()),
            'accountSrc': 'wxapp',
            'accountId': self.token
        }
        response = s.post(f'{self.baseUrl}obtain/event/integral', headers=self.headers,json=json_data)
        point_info = response.json()
        # print(point_info)
        if point_info['code']== 200:
            msg=point_info['message']
            Log(f'>>签到成功,,{msg}')
        else:
            print(f">>{point_info['message']}")
            # print(response.text)
    def get_TaskList(self):
        Log('>>>>>>获取任务列表')
        json_data ={
            "channelId": "wxapp",
            "pageNum": 1,
            "pageSize": 100,
            "businessType": "goldBetter",
            "reqTime": int(time.time()),
            "accountSrc": "wxapp",
            "accountId": self.token
        }
        response = s.post(f'{self.baseUrl}integral/event/list', headers=self.headers,json=json_data)
        # try:
        json_data = response.json()
        # print(json_data)
        skip_type=['关注公众号','实名认证','完善个人信息','累计消耗积分','寄快递','购买超级会员','兑换商品']
        complete = {}
        if json_data['message'] == '请求成功':
            data=json_data['data']
            list = data['items']
            for i in list:
                eventStatus = i['eventStatus']
                eventCode = i['eventCode']
                #可完成次数
                surplusCount = i['surplusCount']
                title = i['eventName']
                if title == '本月寄满3件': surplusCount = 1
                if title in skip_type:continue
                stu = {"0":"已完成","1":"未完成"}
                Log(f'当前任务【{title}】,{stu[eventStatus]}')
                for t in range(surplusCount):
                    if eventStatus != "1" :
                        self.doTask(eventCode,title)
                        if title == '观看精彩视频':
                            self.watchAd(title)
                    else:
                        complete[title] = 0
                    time.sleep(2)
            time.sleep(2)

        if all(value == 0 for value in complete.values()):
            Log(">>>任务已全部完成")
            return True
            # print(f'>>当前积分：【{point}】')
        # except:
        #     print(response.text)
    def watchAd(self,title):
        json_data = {
            "action":"ydmbintegral.ydintegral.obtain.event.integral",
            "appid":"wjvxmno358lze827",
            "req_time":int(time.time()),
            "options":"false",
            "data":{
                "accountId":self.token,
                "accountSrc":"wxapp",
                "reqTime":int(time.time()),"itgType":"wechat_viewadv"
                    },
            "version":"V1.0"}
        response = s.post(f'{self.baseUrl}obtain/event/integral', headers=self.headers, json=json_data)
        point_info = response.json()
        # print(point_info)
        if point_info['code'] == 200:
            msg = point_info['message']
            print(f'>>{title},{msg}')
        else:
            print(f">>{title},{point_info['message']}")

    def doTask(self,eventCode,title):
        json_data = {
            'channelId': 'wxapp',
            'itgType': f'{eventCode}',
            'reqTime': int(time.time()),
            'accountSrc': 'wxapp',
            'accountId': self.token
        }
        response = s.post(f'{self.baseUrl}obtain/event/integral', headers=self.headers, json=json_data)
        point_info = response.json()
        # print(point_info)
        if point_info['code'] == 200:
            msg = point_info['message']
            print(f'>>{title},{msg}')
        else:
            print(f">>{title},{point_info['message']}")

    def getDrawInfo(self):
        self.DrawHeaders = {
            'Host': 'op.yundasys.com',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8259',
            'Content-Type': 'application/json; charset=UTF-8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://op.yundasys.com/mb-ext-channel/index.html',
            'Accept-Language': 'zh-CN,zh',
        }
        json_data = {
            "reqTime": int(time.time()),
            "accountId": self.token,
            "accountSrc": "wxapp"
        }
        response = s.post(f'https://op.yundasys.com/gateway/ydmbaccount/ydaccount/mc/Itg/store/token', headers=self.DrawHeaders, json=json_data)
        point_info = response.json()
        # print(point_info)
        if point_info['code'] == 200:
            data = point_info['data']
            if data:
                self.getDrawNumber(data)
        else:
            print(f">>{point_info['message']}")

    def getDrawNumber(self,data):
        json_data = {
            'activityId': 16,
            'plum_session_applet': data,
            'suid': 'gmrtxvrye6',
            'mwl_client_flag': 'wxapp',
        }
        resp = s.post(f'https://op.yundasys.com/itgstoresys/api/lottery/drawNumber', headers=self.DrawHeaders, json=json_data)
        res_info = resp.json()
        if res_info['code'] == 200:
            freeDrawNumber = res_info['data']['freeDrawNumber']
            print(f'>>剩余免费抽奖次数：【{freeDrawNumber}】')
            if freeDrawNumber == 1:
                self.doDraw(data)

        else:
            print(f">>{res_info['message']}")

    def doDraw(self,data):
        res_data = {
            'activityId': 16,
            'plum_session_applet': data,
            'suid': 'gmrtxvrye6',
            'mwl_client_flag': 'wxapp',
        }
        resp = s.post(f'https://op.yundasys.com/itgstoresys/api/lottery/draw', headers=self.DrawHeaders, json=res_data)
        res_info = resp.json()
        if res_info['code'] == "200":
            msg = res_info['message']
            prizeName = res_info['data']['prizeName']
            Log(f'>>{msg},获得{prizeName}')
        else:
            Log(f">>{res_info['message']}")


    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if not self.get_point():
            return False
        self.sign()
        self.get_TaskList()
        self.getDrawInfo()
        self.sendMsg()
        return True

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
    APP_NAME = '韵达快递小程序'
    ENV_NAME = 'YDKD'
    CK_NAME = 'Authorization'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
      积分抽奖
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找URl请求头带{CK_NAME}
      复制里面的{CK_NAME}参数值
参数示例：oPJUI0eZ5cm8BpR7xxxx
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
            s = requests.session()
            s.verify = False
            run_result = RUN(infos, index).main()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)