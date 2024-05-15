# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "30 9 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('宽哥之家小程序')

import os
import random
import time

import requests
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
            self.send_UID = last_info
        self.index = index + 1
        Log(f"\n---------开始执行第{self.index}个账号>>>>>")
        self.s = requests.session()
        self.s.verify = False

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129',
            'Host': 'shop.sctobacco.com',
            'Connection': 'keep-alive',
            'xweb_xhr': '1',
            'gray': '0',
            'token': self.token,
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://servicewechat.com/wxb6bc0796e0f0db00/224/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.s.headers.update(self.headers)


    def do_request(self, url, method='POST',params=None, data=None, headers=None):

        try:
            response = self.s.request(method, url, params=params, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求错误: {e}")
            return None

    def personal_info(self):
        Log(f'======= 查询用户信息 =======')
        personal_info_valid = False
        try:
            # 发送GET请求
            response = self.do_request('https://shop.sctobacco.com/api/mc-server/mypage/simpleInfo',method='GET')
            # 检查请求是否成功
            if response.get('code','-1'):
                personal_info_valid = True
                data = response.get('data', {})
                mobile_phone = data.get('phone','')
                self.name = data.get('nickname','')
                unionId = data.get('unionId','')
                self.mobile_phone = mobile_phone[:3] + "*" * 4 + mobile_phone[7:]
                # 提取个人信息
                Log(f">>账号[{self.index}]登陆成功！✅\n用户名：【{self.name}】 \n手机号：【{self.mobile_phone}】")
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'>>登录失败❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)

        finally:
            # 最终返回请求是否成功的标志
            return personal_info_valid

    def myTask(self):
        print(f'======= 查询任务列表 =======')
        try:

            # 发送GET请求
            response = self.do_request('https://shop.sctobacco.com/api/mc-server/mcTask/myTask',method='GET')
            # 检查请求是否成功
            if response.get('code','-1'):
                data = response.get('data', {})
                taskList = data.get('taskList',[{}])
                skip_task =[50001,50002,30002]
                for task in taskList:
                    taskName = task.get('taskName', '')
                    taskId = task.get('taskId', '')
                    isCompleted = task.get('isCompleted', '0')
                    print(f'>>当前任务：【{taskName}】')
                    if taskId in skip_task:
                        print('>暂不支持，跳过❌')
                        continue
                    if isCompleted != '0' :
                        print('>已完成，跳过✅')
                        continue
                    if taskId == 30016:
                        self.SignSubmit()
                    elif taskId == 30004:
                        self.listForMobile()
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'查询任务列表失败❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)

    def get_score(self):
        Log(f'======= 获取积分信息 =======')
        try:
            timestamp = int(time.time() * 1000)
            # 发送GET请求
            response = self.do_request(f'https://shop.sctobacco.com/api/sc-server/log/detail?scoreTypeId=jifen001',method='GET')
            # 检查请求是否成功
            if response.get('code','-1'):
                data = response.get('data', {})
                if data:
                    scoreTypeName = data.get('scoreTypeName', '')
                    activeScore = data.get('activeScore', '')
                    Log(f'>当前{scoreTypeName}：【{activeScore}】✅')
                else:
                    Log('>获取积分信息失败❌')
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'获取积分信息失败❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)

    def SignSubmit(self):
        Log(f'======= 签到 =======')
        try:
            timestamp = int(time.time() * 1000)
            # 发送GET请求
            response = self.do_request(f'https://shop.sctobacco.com/api/ac-server/manage/acSignMemberLog/SignSubmit?t={timestamp}',method='GET')
            # 检查请求是否成功
            if response.get('code','-1'):
                data = response.get('data', '')
                if data:
                    Log(f'>签到成功✅，获得{data}积分')
                else:
                    Log('>签到失败❌')
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'签到失败❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)


    def listForMobile(self):
        Log(f'======= 获取文章列表 =======')
        try:
            timestamp = int(time.time() * 1000)
            # 发送GET请求
            response = self.do_request(f'https://shop.sctobacco.com/api/mc-server/mcMedia/listForMobile?t={timestamp}&offset=0&limit=10&isShow=1',method='GET')
            # 检查请求是否成功
            if response.get('code','-1'):
                data = response.get('data', {})
                rows = data.get('rows', [{}])
                random_element = random.choice(rows)
                if random_element:
                    Log(f'>>>获取文章列表成功✅')
                    appid = random_element['appid']
                    title = random_element['title']
                    mediaId = random_element['mediaId']
                    Log(f'>>前选择文章：【{title}】 appid:{appid} mediaId:{mediaId}')
                    self.clickMedia(mediaId,appid)
                else:
                    Log('>>获取文章列表失败❌')
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'获取文章列表失败❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)

    def clickMedia(self,mediaId,appid):
        Log(f'======= 阅读文章 =======')
        try:
            headers = self.headers.copy()
            headers['Accept'] = "application/json, text/plain, */*"
            data = {
                "mpMediaId": mediaId,
                "mediaId": mediaId,
                "appid": appid
            }
            # 发送GET请求
            response = self.do_request(f'https://shop.sctobacco.com/api/mc-server/mcMedia/clickMedia',params=data,headers=headers)
            # 检查请求是否成功
            if response.get('code','-1'):
                message = response.get('message', {})
                if message == "success":
                    Log(f'>阅读文章成功✅')
                else:
                    Log('>阅读文章失败❌')
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'阅读文章❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)


    def lottery(self):
        Log(f'======= 抽奖 =======')
        try:
            parmas={
                'activityId':'8a80895d8f15c558018f1992d33b0d97'
            }
            # 发送GET请求
            response = self.do_request(f'https://shop.sctobacco.com/api/ac-server/lottery/complete',method='GET',params=parmas)
            # 检查请求是否成功
            if response.get('code','-1'):
                message = response.get('message', {})
                if message == "success":
                    Log(f'>抽奖成功✅，{response}')
                else:
                    Log('>抽奖失败❌')
            else:
                # 如果请求不成功，则打印错误信息
                message = response.get('msg', '')
                Log(f'阅读文章❌: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)


    def main(self):
        if not self.personal_info() :
            Log("用户信息无效，请更新CK")
            self.sendMsg()
            return False
        self.myTask()
        # self.listForMobile()
        self.get_score()
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
    APP_NAME = '宽哥之家小程序'
    ENV_NAME = 'KGZJ'
    CK_NAME = 'token'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
  积分签到
✨ 抓包步骤：
  打开{APP_NAME}
  授权登陆
  打开抓包工具
  找请求头带{CK_NAME}的URl
  复制里面的{CK_NAME}参数值
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
参数示例：1790314xxxxxx@UID_xxxxx
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：5 8 * * *
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
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).main()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', f'{send_msg}\n{TIPS_HTML}')
