# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author CHERWIN✨✨✨
# -------------------------------
# cron "30 1 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('奈雪小程序签到')
import datetime
import json
import os
import random
import requests
import hashlib
import hmac
import base64
import time
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

        self.token =  f'Bearer {token}'
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6945'
        self.openId = 'QL6ZOftGzbziPlZwfiXM'

    def random_string(self,length=6, chars='123456789'):
        return ''.join(random.choice(chars) for _ in range(length))

    def get_body(self):
        nonce = int(self.random_string())
        timestamp = int(time.time())
        url_path = f'nonce={nonce}&openId={self.openId}&timestamp={timestamp}'
        signature = base64.b64encode(
            hmac.new('sArMTldQ9tqU19XIRDMWz7BO5WaeBnrezA'.encode(), url_path.encode(), hashlib.sha1).digest()).decode()
        common = {
            'platform': 'wxapp',
            'version': '5.1.8',
            'imei': '',
            'osn': 'microsoft',
            'sv': 'Windows 10 x64',
            'lang': 'zh_CN',
            'currency': 'CNY',
            'timeZone': '',
            'nonce': nonce,
            'openId': self.openId,
            'timestamp': timestamp,
            'signature': signature
        }
        params = {
            'businessType': 1,
            'brand': 26000252,
            'tenantId': 1,
            'channel': 2,
            'stallType': None,
            'storeId': None
        }

        requestData = {
            'common': common,
            'params': params
        }
        return requestData

    def task_api(self,api_options=None):
        if api_options is None:
            api_options = {}
        try:
            # 首先解析URL，获得主机名
            host_name = api_options['url'].replace('//', '/').split('/')[1]
            full_url = api_options['url']
            if 'queryParam' in api_options:
                # 如果存在查询参数，将其附加到URL
                query_str = "&".join(f"{k}={v}" for k, v in api_options['queryParam'].items())
                full_url += '?' + query_str
            # 定义请求头
            headers = {
                'Host': host_name,
                'Connection': 'keep-alive',
                'User-Agent': self.UA,
                'Authorization': self.token,
                'Referer': 'https://tm-web.pin-dao.cn/',
                'Origin': 'https://tm-web.pin-dao.cn'
            }
            # 准备请求体
            data = None
            if 'body' in api_options:
                body = self.get_body()
                body['params'].update(api_options['body'])
                content_type = api_options.get('Content-Type', 'application/json')
                headers['Content-Type'] = content_type
                if 'json' in content_type:
                    data = json.dumps(body)
                else:
                    data = "&".join(f"{k}={json.dumps(v) if isinstance(v, dict) else v}" for k, v in body.items())
                headers['Content-Length'] = str(len(data))
            # 如果有额外的URL参数或头部参数，合并到请求中
            if 'urlObjectParam' in api_options:
                # 这里根据需要处理urlObjectParam
                pass
            if 'headerParam' in api_options:
                headers.update(api_options['headerParam'])
            # 发出请求
            response = requests.request(method=api_options.get('method', 'GET'), url=full_url, headers=headers,
                                        data=data, timeout=20,verify=False)
            # 打印状态码
            if response.status_code != 200:
                print(f"[{api_options.get('fn', 'unknown function')}]返回[{response.status_code}]")

            # 解析结果
            try:
                result = response.json()
            except ValueError:
                result = response.text
            return result

        except Exception as e:
            print(str(e))
            return {}

    def base_userinfo(self):
        try:
            api_options = {
                'fn': 'baseUserinfo',
                'method': 'post',
                'url': 'https://tm-web.pin-dao.cn/user/base-userinfo',
                'body': {}
            }
            response = self.task_api(api_options)
            if response['code'] == 0:
                # 登录成功的逻辑处理
                phone = response['data']['phone']
                self.phone = phone[:3] + "*" * 4 + phone[7:]
                self.userId = response['data']['userId']
                self.nickName = response['data']['nickName']
                Log(f'账号[{self.index}]登录成功！\n手机号：[{self.phone}] ID[{self.userId}]')
                # print(one_msg)
                return True
            else:
                # 登录失败的逻辑处理
                Log(f"账号登录失败: {response['message']}")
        except Exception as e:
            print(e)

    def user_account(self):
        try:
            api_options = {
                'fn': 'userAccount',
                'method': 'post',
                'url': 'https://tm-web.pin-dao.cn/user/account/user-account',
                'body': {}
            }
            response = self.task_api(api_options)
            if response['code'] == 0:
                # 查询成功的逻辑处理
                coin = response['data']['coin']
                Log(f'账号[{self.index}]当前奈雪币: {coin}')
            else:
                # 查询失败的逻辑处理
                Log(f'账号[{self.index}]查询失败')
        except Exception as e:
            print(e)

    def sign_record(self):
        try:
            sign_date = datetime.datetime.now().replace(day=1).strftime('%Y-%m-%d')
            today_date = datetime.datetime.now().strftime('%Y-%m-%d')
            api_options = {
                'fn': 'signRecord',
                'method': 'post',
                'url': 'https://tm-web.pin-dao.cn/user/sign/records',
                'body': {
                    'signDate': sign_date,
                    'startDate': today_date
                }
            }
            response = self.task_api(api_options)
            if response['code'] == 0:
                Log(f"今天{'已' if response['data']['status'] else '未'}签到，已签到{response['data']['signCount']}天")
                if not response['data']['status']:
                    self.sign_save()
            else:
                Log(f"查询签到失败: {response['message']}")
        except Exception as e:
            print(e)

    def sign_save(self):
        try:
            sign_date = datetime.datetime.now().strftime('%Y-%m-%d')
            api_options = {
                'fn': 'signSave',
                'method': 'post',
                'url': 'https://tm-web.pin-dao.cn/user/sign/save',
                'body': {
                    'signDate': sign_date
                }
            }
            response = self.task_api(api_options)
            if response['code'] == 0:
                if response['data']['flag']:
                    Log('签到成功')
                else:
                    Log('今天已经签到过了')
            else:
                print(f"签到失败: {response['message']}")
        except Exception as e:
            print(e)

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        base_userinfo_result = self.base_userinfo()
        if not base_userinfo_result:
            Log("用户信息无效，请更新CK")
            return False
        self.sign_record()
        self.user_account()
        self.sendMsg()
        return True

    def sendMsg(self, help=False):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME, help)
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
    APP_NAME = '奈雪点单小程序'
    ENV_NAME = 'NXDD'
    CK_NAME = 'Authorization'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找请求头带{CK_NAME}的URl
      复制里面的{CK_NAME}参数值【不要】前面的Bearer 【不要】前面的Bearer 【不要】前面的Bearer 
参数示例：eyJhbGciOiJxxxxxxxxxxxx
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值【不要】前面的Bearer'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：30 1 * * *
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
