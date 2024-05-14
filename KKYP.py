# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author CHERWIN✨✨✨
# -------------------------------
# cron "0 0 2 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('夸克云盘签到')
import os
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
        self.cookie = token

    def get_growth_info(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        headers = {"content-type": "application/json", "cookie": self.cookie}
        response = self.s.get(url=url, headers=headers, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        payload = {"sign_cyclic": True}
        headers = {"content-type": "application/json", "cookie": self.cookie}
        response = self.s.post(url=url, json=payload, headers=headers, params=querystring).json()
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def get_account_info(self):
        url = "https://pan.quark.cn/account/info"
        querystring = {"fr": "pc", "platform": "pc"}
        headers = {"content-type": "application/json", "cookie": self.cookie}
        response = self.s.get(url=url, headers=headers, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        account_info = self.get_account_info()
        if not account_info:
            Log(f"\n账号[{self.index}]登录失败，cookie无效")
            return False
        else:
            Log(f"用户名: {account_info['nickname']}")
            growth_info = self.get_growth_info()
            if growth_info:
                if growth_info["cap_sign"]["sign_daily"]:
                    Log(f"今日已签到+{int(growth_info['cap_sign']['sign_daily_reward'] / 1024 / 1024)}MB，连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})")
                else:
                    sign, sign_return = self.get_growth_sign()
                    if sign:
                        Log(f"今日签到+{int(sign_return / 1024 / 1024)}MB，连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})")

                    else:
                        Log( f"签到: {sign_return}\n")


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
    APP_NAME = '夸克云盘'
    ENV_NAME = 'KKYP'
    CK_NAME = '全部ck'
    CK_URL = 'https://pan.quark.cn/'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      签到
✨ 抓包步骤：
      打开抓包工具
      打开https://pan.quark.cn/
      登陆
      找带cookies的URl
      复制里面的cookies参数值
参数示例：_UP_A4A_11_=wxxxxxxx
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ 推荐cron：0 0 2 * * *
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
