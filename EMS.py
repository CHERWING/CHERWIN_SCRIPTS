# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# ✨✨✨ @Author CHERWIN✨✨✨
# -------------------------------
# cron "0 10 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('EMS邮惠中心小程序')

import os
from datetime import date

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
        self.openId = token
        self.headers = {
            'Host': 'ump.ems.com.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6945',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh',
     }


    def do_request(self, url, method="POST",params=None, data=None, headers=None):
        if not headers:
            headers = self.headers
        try:
            response = self.s.request(method, url, params=params, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求错误: {e}")
            return None

    def findByOpenIdAppId(self):
        act_name = '获取TOKEN'
        Log(f"\n====== {act_name} ======")
        try:
            params = {
                "appId":"wx52872495fb375c4b",
                "openId":self.openId,
                "source":"JD"
            }
            response = self.do_request('https://ump.ems.com.cn/memberCenterApiV2/member/findByOpenIdAppId',data=params)
            if response and response.get('code') == '000000':
                # print(response)
                info = response.get('info', {})
                self.token = info.get('token', '')
                self.memberId = info.get('memberId', '')
                self.headers['MC-TOKEN'] = self.token
                Log(f'>>{act_name}成功✅')
                # print(f'>用户ID：【{self.memberId}】')
                return True
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False
    def details(self):
        act_name = '获取用户信息'
        Log(f"\n====== {act_name} ======")
        try:
            params = {}
            response = self.do_request('https://ump.ems.com.cn/memberCenterApiV2/member/details',data=params)
            if response and response.get('code') == '000000':
                # print(response)
                info = response.get('info', {})
                phone = info.get('phone', '')
                Log(f'>>{act_name}成功✅')
                Log(f'>用户ID：【{self.memberId}】\n手机号：【{phone}】')
                return True
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False

    def sign(self):
        act_name = '签到'
        Log(f"\n====== {act_name} ======")
        try:
            params = {
                "appId":"wx52872495fb375c4b",
                "userId":self.memberId,
                "openId":self.openId,
                "activId":'d191dce0740849b1b7377e83c00475d6'
            }
            response = self.do_request('https://ump.ems.com.cn/activCenterApi/signActivInfo/sign',data=params)
            if response and response.get('code') == '000000':
                # print(response)
                info = response.get('info', {})
                prizeSize = info[0].get('prizeSize', {})
                Log(f'>{act_name}成功✅>获得：【{prizeSize}】积分')
                return True
            elif response and response.get('code') == '600001':
                msg = response.get('msg')
                Log(f'{act_name}失败❌:【{msg}】')
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False

    def memberGoldsInfo(self):
        act_name = '获取积分信息'
        Log(f"\n====== {act_name} ======")
        try:
            params = {}
            response = self.do_request('https://ump.ems.com.cn/memberCenterApiV2/golds/memberGoldsInfo',data=params)
            if response and response.get('code') == '000000':
                # print(response)
                info = response.get('info', {})
                availableGoldsTotal = info.get('availableGoldsTotal', {})
                Log(f'>当前积分：【{availableGoldsTotal}】')
                return True
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False

    def receivePrize(self,prizeId):
        act_name = '领取连签礼包'
        Log(f"\n====== {act_name} ======")
        try:
            params = {
                "activId": "d191dce0740849b1b7377e83c00475d6",
                "appId": "wx52872495fb375c4b",
                "openId": self.openId,
                "userId": self.memberId,
                "prizeId": prizeId
            }
            response = self.do_request('https://ump.ems.com.cn/activCenterApi/signActivInfo/receivePrize',data=params)
            if response and response.get('code') == '000000':
                Log(f'{act_name}成功✅')
                return True
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False

    def queryPrizeIsReceive(self):
        act_name = '查询签到礼包领取状态'
        Log(f"\n====== {act_name} ======")
        try:
            params = {
                "activId": "d191dce0740849b1b7377e83c00475d6",
                "appId": "wx52872495fb375c4b",
                "openId": self.openId,
                "userId": self.memberId
            }
            response = self.do_request('https://ump.ems.com.cn/activCenterApi/signActivInfo/queryPrizeIsReceive',data=params)
            if response and response.get('code') == '000000':
                info = response.get('info',[{}])
                Log(f'{act_name}成功✅')
                if info != [{}]:
                    for Id in info:
                        prizeId = Id['prizeId']
                        prizeReceiveStatus = Id['prizeReceiveStatus']
                        if prizeReceiveStatus != 1:
                            Log(f'有待领取礼包')
                            self.receivePrize(prizeId)
                        else:
                            Log(f'暂无待领取礼包')
                else:
                    Log(f'暂无待领取礼包')
                return True
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False

    def querySignDetail(self):
        act_name = '获取签到详情'
        Log(f"\n====== {act_name} ======")
        try:
            params = {
                "appId": "wx52872495fb375c4b",
                "userId": self.memberId,
                "openId": self.openId,
                "activId": 'd191dce0740849b1b7377e83c00475d6'
            }
            response = self.do_request('https://ump.ems.com.cn/activCenterApi/signActivInfo/querySignDetail',data=params)
            if response and response.get('code') == '000000':
                Log(f'{act_name}成功✅')
                info = response.get('info', {})
                signDay = info.get('signDay', '')
                maxContiSignDay = info.get('maxContiSignDay', '')
                signDayList = info.get('signDayList', {})
                Log(f'>累计签到：【{signDay}】天')
                Log(f'>已连续签到：【{maxContiSignDay}】天')
                if date.today().strftime("%Y-%m-%d") not in signDayList:
                    Log(f'>今日未签到')
                    self.sign()
                else:
                    Log(f'>今日已签到✅')

                return True
            else:
                Log(f'{act_name}失败❌: {response}')
                return False
        except Exception as e:
            print(f'{act_name}异常❌: {e}')
            return False

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        # if self.login():

        if self.findByOpenIdAppId():
            self.details()
            self.querySignDetail()
            self.queryPrizeIsReceive()
            self.memberGoldsInfo()
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
    APP_NAME = 'EMS邮惠中心小程序'
    ENV_NAME = 'EMS'
    CK_NAME = 'openId'
    CK_URL = 'https://ump.ems.com.cn/memberCenterApiV2/member/findByOpenIdAppId'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找{CK_URL}请求body里面的[{CK_NAME}]
      复制里面的[{CK_NAME}]参数值
参数示例：o-7675D-prmxxxxxxxxxx
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：0 10 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.05.23'
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
