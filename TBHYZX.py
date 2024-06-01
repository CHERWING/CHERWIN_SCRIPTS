# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# ✨ 推荐cron：1 8 * * *
# ✨✨✨ @Author CHERWIN✨✨✨
# -------------------------------
# cron "0 6 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('特步会员中心小程序签到')
import json
import os
from datetime import datetime, date
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# import CHERWIN_TOOLS
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#
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
        self.token = json.loads(split_info[0])
        # print(self.token)
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            print('检测到设置了UID')
            print(last_info)
            self.send_UID = last_info
        self.index = index + 1

        self.headers = {
            "Host": "wxa-tp.ezrpro.com",
            "ezr-source": "weapp",
            "limittype": "0",
            "ezr-sp": "2",
            "uber-trace-id": "9e04a05a0c7e5df3:9e04a05a0c7e5df3:0:1",
            "ezr-brand-id": "254",
            "needloading": "[object Boolean]",
            "ezr-client-name": "EZR.FE.MultiMall.Mini",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "content-type": "application/json",
            "xweb_xhr": "1",
            "accept": "*/*",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://servicewechat.com/wx12e1cb3b09a0e6f0/121/page-frame.html",
            "accept-language": "zh-CN,zh;q=0.9"
        }
        #
        # print(self.headers)
        for key, value in self.token.items():
            self.headers[key] = value
        self.baseUrl = 'https://wxa-tp.ezrpro.com/myvip/'


    def GetVipCardInfoByVipId(self):
        Log('>>>>>>用户信息')
        url = "https://wxa-tp.ezrpro.com/myvip/FamilyCard/GetVipCardInfoByVipId"

        response = s.get(url, headers=self.headers)
        response = response.json()
        # print(response.text)
        if response.get('Success',False):
            data = response.get('Result', {})
            VipInfo=data.get('VipInfo', {})
            # 手机号
            MobileNo=VipInfo.get('MobileNo','')
            NickName=VipInfo.get('NickName','')
            BonusTotal=VipInfo.get('BonusTotal','')
            mobile=MobileNo[:3] + "*" * 4 + MobileNo[7:]
            Log(f'>>当前用户：【{NickName}】 手机号：【{mobile}】')
            Log(f'>>当前积分：【{BonusTotal}】')
            return True
        else:
            Log('可能token失效了')
            return False


    def GetSignInDtlInfo(self):
        Log('>>>>>>获取签到信息')
        url = "https://wxa-tp.ezrpro.com/myvip/Vip/SignIn/GetSignInDtlInfo"
        response = s.get(url, headers=self.headers)
        response = response.json()
        # print(response.text)
        if response.get('Success',False):
            data = response.get('Result', {})
            VipSignInDtl=data.get('VipSignInDtl', {})
            SignedDays=VipSignInDtl.get('SignedDays', '')
            IsSigInToday=VipSignInDtl.get('IsSigInToday', False)
            SignInCfg = data.get('SignInCfg', {})
            ActId = SignInCfg.get('ActId', '')
            if IsSigInToday:
                Log(f'>>今日已签到，累计签到：【{SignedDays}】天')
            else:
                Log('开始签到')
                self.SignIn(ActId)
            return True
        else:
            Log('可能token失效了')
            return False

    def SignIn(self, ActId):
        Log('====== 开始签到 ======')
        url = f"{self.baseUrl}Vip/SignIn/SignIn"
        data = {
            "ActId": ActId,
            "ActRemindStatus": True
        }
        response = s.post(url, headers=self.headers,json=data)
        response = response.json()
        # print(response)
        if response.get('Success', False):
            data = response.get('Result', {})
            BonusValue = data.get('BonusValue', '')
            Log(f'签到成功，获得：【{BonusValue}】积分')
            return True
        else:
            ErrMsg = response.get('ErrMsg', '')
            Log(f'签到失败：{ErrMsg}')
            return False


    def BonusClassify(self):
        Log('>>>>>>获取积分信息')
        url = "https://wxa-tp.ezrpro.com/myvip/Vip/Bonus/GetMyBonusLogs?pageSize=10&pageIndex=1&BonusClassify=0"
        response = s.get(url, headers=self.headers)
        response = response.json()
        # print(response)
        if response.get('Success',False):
            data = response.get('Result', {})
            BonusTotal=data.get('BonusTotal', '')
            Log(f'当前积分：【{BonusTotal}】')
            return True
        else:
            Log('可能token失效了')
            return False

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        # if self.WxAppOnLoginNew():
        if self.GetVipCardInfoByVipId():
            # self.GetVipCardInfoByVipId()
            self.GetSignInDtlInfo()
            self.BonusClassify()
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
    APP_NAME = '特步会员中心小程序'
    ENV_NAME = 'TBHYZX'
    CK_URL = 'https://wxa-tp.ezrpro.com/myvip/Base/User/WxAppOnLoginNew'
    CK_NAME = '响应body里的Fields全部内容'
    CK_EX = '{"ezr-cop-id":"888","ezr-vuid":"888888","ezr-userid":"aaaaaaa","ezr-sv":"1","ezr-st":"8888","ezr-ss":"bbbbb"}'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
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
✨ 推荐cron：0 6 * * *
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
            s = requests.session()
            s.verify = False
            run_result = RUN(infos, index).main()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
