# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# 邀请码：https://github.com/CHERWING/CHERWIN_SCRIPTS/assets/160421895/6dbacc8f-1c1a-47cf-9760-327385e85a0f
# ✨请走作者邀请码支持开发，谢谢！✨
# 定时至少4次
# cron "5 7,11,15,20 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('999会员中心小程序')
import base64
import json
import os
import random
import time
from datetime import datetime
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

        CF_PROXY_URL = os.environ.get('CF_PROXY_URL', False)
        if CF_PROXY_URL:
            print(f'【已设置反代】：{CF_PROXY_URL}✅')
            self.baseUrl = CF_PROXY_URL
        else:
            print(
                f'【未设置反代，使用官方域名】❌ 脚本如果报错（unsafe legacy renegotiation）请自行搭建反代，搭建方法见：https://github.com/CHERWING/CHERWIN_SCRIPTS/tree/main/Cloudflare%20Workers%20Proxy')
            self.baseUrl = 'https://mc.999.com.cn/'

        self.headers = {
            'Host': self.baseUrl.split('/')[2],
            'xweb_xhr': '1',
            'locale': 'zh_CN',
            'Authorization': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wx58ff7065f6d3dffe/69/page-frame.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }


        self.use_power_max = False

    def make_request(self, url, method='post', headers={}, data={}, params=None):
        if headers == {}:
            headers = self.headers
        try:
            if method.lower() == 'get':
                response = self.s.get(url, headers=headers,  params=params)
            elif method.lower() == 'post':
                response = self.s.post(url, headers=headers, json=data, params=params)
            else:
                raise ValueError("不支持的请求方法❌: " + method)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常❌：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法❌：", e)
        except Exception as e:
            print("发生了未知错误❌：", e)

    def get_userinfo(self):
        act_name = '用户信息'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}zanmall_diy/ma/personal/user/info"
        response = self.make_request(url,'get')
        # print(response)
        if response.get('success', False):
            data = response.get('data', {})
            self.userId = data.get('userId', '')
            self.phone = data.get('phone', '')
            self.nickName = data.get('nickName', '')
            Log(f'{act_name}成功！✅')
            Log(f'> 当前用户ID：【{self.userId}】\n> 手机号：【{self.nickName}】')
            return True
        else:
            print(f'{act_name}失败❌：{response}')
            return False

    def invited(self):
        act_name = '助力作者'
        # print(f'\n====== {act_name} ======')
        json_data = {
            "inviterMobile": base64.b64decode(b'MTc1MjE1NzE5MDU=').decode('utf-8'),
            "activityId": "2",
            "tempUid": "6fff1cb519924645926a7de2fad44722"
        }
        url = f"{self.baseUrl}zanmall_diy/ma/invitation/invitee/invited"
        response = self.make_request(url,data=json_data)
        if response.get('success', False):
            # print(f'> {act_name}成功！✅')
            return True
        else:
            # print(f'> {act_name}失败❌：{response}')
            return False

    def get_Checkinlist(self):
        act_name = '获取打卡状态'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}zanmall_diy/ma/client/dailyHealthCheckIn/list"
        response = self.make_request(url,'get')
        if response.get('success', False):
            data = response.get('data', {})
            for task in data:
                type = task['type']
                name = task['name']
                status = task['status']
                if not status:
                    self.do_finishTask(type,name)
                    self.do_signTask(type,name)
                    break
                else:
                    Log(f'> {name}已打卡！✅')
            return True
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def do_signTask(self,type,name):
        act_name = f'{name}打卡上报'
        Log(f'\n====== {act_name} ======')
        url = f'{self.baseUrl}zanmall_diy/ma/client/dailyHealthCheckIn/signTask'
        json_data = f'type={type}'
        response = self.make_request(url,'post',params=json_data)
        if response.get('success', False):
            data = response.get('data', {})
            status = data.get('status', False)
            if status:
                Log(f'> {act_name}成功！✅')
                return True
            else:
                print(f'> {act_name}失败❌')
                return False
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def do_finishTask(self,type,name):
        act_name = f'{name}打卡'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}zanmall_diy/ma/client/pointTaskClient/finishTask"
        checkInTime = datetime.now().strftime("%Y-%m-%d")
        json_data = {
            "type": "daily_health_check_in",
            "params": {
                "checkInCode": type,
                "checkInTime": checkInTime
            }
        }
        response = self.make_request(url,'post',data=json_data)
        if response.get('success', False):
            data = response.get('data', {})
            point = data.get('point', '')
            success = data.get('success', False)
            if success:
                Log(f'> {act_name}成功！✅')
                Log(f'> 获得积分：【{point}】')
            else:
                print(f'> {act_name}失败❌')
            return True
        else:
            print(f'> {act_name}失败❌：{response}')
            return False
    def get_pointInfo(self):
        act_name = '获取积分信息'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}zanmall_diy/ma/personal/point/pointInfo"
        response = self.make_request(url,'get')
        if response.get('success', False):
            data = response.get('data', {})
            Log(f'> {act_name}成功！✅')
            Log(f'> 当前积分：【{data}】')
            return True
        else:
            print(f'> {act_name}失败❌：{response}')
            return False
    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.get_userinfo():
            # random_delay(5,30)
            self.invited()
            self.get_Checkinlist()
            random_delay()
            self.get_pointInfo()
            self.sendMsg()
            return True
        else:
            self.sendMsg()
            return False

    def sendMsg(self):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME)
            print(push_res)

def get_ip():
    response = requests.get('https://cdn.jsdelivr.net/gh/parserpp/ip_ports/proxyinfo.json',verify=False)
    # 使用正则表达式提取 IP 地址和端口号
    data = response.text
    lines = data.strip().split('\n')
    # json_objects = [json.loads(line) for line in lines]
    json_objects = [json.loads(line) for line in lines if json.loads(line)["country"] == "CN"]
    # json_array = json.dumps(json_objects, indent=4)
    if json_objects:
        selected = random.choice(json_objects)
        result = f"{selected['type']}://{selected['host']}:{selected['port']}"

        proxies = {
            selected['type']: result,
        }
        print(f"当前代理：{result}")
        return proxies
    else:
        print("没匹配到CN的ip")
        return None


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
    ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode = CHERWIN_TOOLS.main(APP_NAME, local_script_name, ENV_NAME,
                                                                    local_version)


if __name__ == '__main__':
    APP_NAME = '999会员中心小程序'
    ENV_NAME = 'JJJHYZX'
    CK_URL = 'mc.999.com.cn'
    CK_NAME = '请求头Authorization值'
    CK_EX = 'xxxxx-xxxxx-xxxx-xxx-xxxxxxxx'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      早起打卡 每天8杯水 运动15分钟 早睡打卡
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
✨ 推荐cron：5 7,11,15,20 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.05.27'
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
