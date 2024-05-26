# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "5 11 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('hotwind热风微商城小程序')
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
        self.token = split_info[0]
        # print(self.token)
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
        self.appid = 'wxe6d270a3e399ade9'
        self.headers = {
            'Host': 'xapi.weimob.com',
            'cloud-project-name': 'aidachildren',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mi9 Pro 5G Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160117 MMWEBSDK/20230701 MMWEBID/8701 MicroMessenger/8.0.40.2420(0x28002858) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'Content-Type': 'application/json',
            'X-WX-Token': self.token,
            'x-cms-sdk-request': '1.5.47',
            'xweb_xhr': '1',
            'x-biz-id': '1',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://servicewechat.com/{self.appid}/236/page-frame.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.baseUrl = 'https://xapi.weimob.com/api3/'
        self.use_power_max = False
        self.json_data = {
            'appid':'wxe6d270a3e399ade9',
            'basicInfo': {
                'vid': 6001391100130,
                'vidType': 2,
                'bosId': 4001873629130,
                'productId': 1,
                'productInstanceId': 2623574130,
                'productVersionId': '30044',
                'merchantId': 2000058543130,
                'tcode': 'weimob',
                'cid': 182682130,
            },
            'extendInfo': {
                'wxTemplateId': 7593,
                'analysis': [],
                'bosTemplateId': 1000001511,
                'childTemplateIds': [
                    {
                        'customId': 90004,
                        'version': 'crm@0.1.21',
                    },
                    {
                        'customId': 90002,
                        'version': ' ec@46.4',
                    },
                    {
                        'customId': 90006,
                        'version': 'hudong@0.0.208',
                    },
                    {
                        'customId': 90008,
                        'version': 'cms@0.0.439',
                    },
                    {
                        'customId': 90060,
                        'version': 'elearning@0.1.1',
                    },
                ],
                'quickdeliver': {
                    'enable': False,
                },
                'youshu': {
                    'enable': False,
                },
                'source': 1,
                'channelsource': 5,
                'refer': 'cms-index',
                'mpScene': 1037,
            },
            'queryParameter': None,
            'i18n': {
                'language': 'zh',
                'timezone': '8',
            },
            'pid': '100001338635',
            'storeId': '0',
            'bizType': 1,
        }
        self.wid =''

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

    def check_token(self):
        act_name = '检测token'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}passport/access/check"
        response = self.make_request(url, data=self.json_data)
        # print(response)
        if response.get('errmsg', False) == "success" and response.get('data', {}):
            Log(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            loginStatus = data.get('loginStatus', 0)
            if loginStatus:
                Log(f'> TOKEN有效！✅')
                return True
            else:
                Log(f'> TOKEN失效！❌')
                return False
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def queryUserInfo(self):
        act_name = '获取用户信息'
        Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        basicInfo= {
            "basicInfo": {
                    "vid": 4001873629130,
                    "bosId": 4001873629130,
                    "productInstanceId": 2623551130,
                    "tcode": "weimob",
                    "cid": 182682130,
                    "productId": 146
                }
        }
        json_data.update(basicInfo)

        json_data['request'] = {}
        json_data['source'] = 2
        json_data.pop('bizType', None)
        # print(json_data)
        url = f"{self.baseUrl}onecrm/user/center/usercenter/queryUserInfo"
        response = self.make_request(url, data=json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            Log(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            nickname = data.get('nickname', '')
            self.wid = data.get('wid', '')
            sourceObjectList = data.get('sourceObjectList', [])
            for app in sourceObjectList:
                sourceAppId = app['sourceAppId']
                if sourceAppId == self.appid:
                    self.OpenId = app['sourceOpenId']

            Log(f'> 用户名：【{nickname}】')
            Log(f'> OpenId：【{self.OpenId}】')
            Log(f'> wid：【{self.wid}】')

        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def signMainInfo(self):
        act_name = '获取签到状态'
        Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        json_data['basicInfo']['productId'] = 146
        json_data['customInfo'] = {
            "source": 0,
            "wid": self.wid
        }
        url = f"{self.baseUrl}onecrm/mactivity/sign/misc/sign/activity/c/signMainInfo"
        response = self.make_request(url, data=json_data)
        # print(response)
        if response.get('errmsg', False) == "成功" and response.get('data', {}) != {}:
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            hasSign = data.get('hasSign', False)
            maxActivityContinueSignDays = data.get('maxActivityContinueSignDays', False)
            activityCumulativeSignDays = data.get('activityCumulativeSignDays', False)
            monthCumulativeSignDays = data.get('monthCumulativeSignDays', False)
            yearCumulativeSignDays = data.get('yearCumulativeSignDays', False)
            Log(f'> 已连续签到：【{activityCumulativeSignDays}】天')
            Log(f'> 最长连续签到：【{maxActivityContinueSignDays}】天')
            Log(f'> 月累计签到：【{monthCumulativeSignDays}】天')
            Log(f'> 年累计签到：【{yearCumulativeSignDays}】天')

            if hasSign:
                Log(f'> 今日已签到✅')
                return True
            else:
                Log(f'> 今日未签到❌')
                self.sign()
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def sign(self):
        act_name = '签到'
        Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        json_data['customInfo'] = {
            "source": 0,
            "wid": self.wid
        }
        json_data.pop('bizType', None)
        url = f"{self.baseUrl}onecrm/mactivity/sign/misc/sign/activity/core/c/sign"
        response = self.make_request(url, data=json_data)
        # print(response)
        if response.get('errmsg', False) == "成功" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            fixedReward = data.get('fixedReward', {})
            points = fixedReward.get('points', 0)
            Log(f'> 获得积分：【{points}】')
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def getSimpleAccountInfo(self):
        act_name = '获取积分详情'
        Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        json_data['targetBasicInfo'] = {
            "productInstanceId": 2623551130
        }
        json_data['request'] = {}
        json_data.pop('bizType', None)
        url = f"{self.baseUrl}onecrm/point/myPoint/getSimpleAccountInfo"
        response = self.make_request(url, data=json_data)
        # print(response)
        if response.get('errmsg', False) == "success" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            availablePoint = data.get('availablePoint', '')
            Log(f'> 当前积分：【{availablePoint}】')
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.check_token():
            self.queryUserInfo()
            # random_delay(5,30)
            self.signMainInfo()
            random_delay()
            self.getSimpleAccountInfo()
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
    print(f">本次随机延迟： {delay:.2f} 秒.....")
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
    APP_NAME = 'hotwind热风微商城小程序'
    ENV_NAME = 'RFWSC'
    CK_URL = 'xapi.weimob.com'
    CK_NAME = '请求头X-WX-Token'
    CK_EX = '8c8ff04e4f53c213faesxxxxxxxxxxxxxxxxxxxxxxxxxx'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ 功能：
      签到
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找{CK_URL}{CK_NAME}
参数示例：{CK_EX}
邀请码：https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/6dbacc8f-1c1a-47cf-9760-327385e85a0f
✨请走作者邀请码支持开发，谢谢！✨
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：5 11 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.05.24'
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
        if send and not IS_DEV: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
