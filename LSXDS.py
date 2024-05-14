# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# ✨✨✨ @Author CHERWIN✨✨✨
# -------------------------------
# cron "1 8 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('乐事心动社小程序')

import os
import random
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
            "Host": "campuscrm.pepsico.com.cn",
            "xweb_xhr": "1",
            "Authorization": self.token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/8555",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wxf0cab11391f02ba7/90/page-frame.html",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.default_data={"memberId": ''}
        self.baseUrl = 'https://wxa-tp.ezrpro.com/myvip/'

    def make_request(self, url, method='post', headers={}, params={}):
        if headers == {}:
            headers = self.headers
        if params == {}:
            params = self.default_data
        try:
            if method.lower() == 'get':
                response = requests.get(url, headers=headers, verify=False)

            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, json=params, verify=False)
            else:
                raise ValueError("不支持的请求方法: " + method)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法：", e)
        except Exception as e:
            print("发生了未知错误：", e)

    def access_refresh(self):
        Log('>>>>>>刷新用户信息')
        url = "https://campuscrm.pepsico.com.cn/web/user/member/access-refresh"

        response = self.make_request(url)
        if response.get('success',False):
            Log('登录刷新成功！')
            return True
        else:
            Log('可能token失效了')
            return False

    def getInfo(self):
        Log('>>>>>>获取用户信息')
        url = "https://campuscrm.pepsico.com.cn/web/user/member/getInfo"

        response = self.make_request(url)
        if response.get('success',False):
            data = response.get('data', {})
            self.memberId = data.get('memberId', '')
            self.default_data['memberId']=self.memberId
            memberNo = data.get('memberNo', '')
            phone = data.get('phone', '')
            openId = data.get('openId', '')
            unionId = data.get('unionId', '')
            nickname = data.get('nickname', '')
            Log(f'用户名：【{nickname}】,手机号：【{phone}】')
            # print(f'unionId：【{unionId}】,openId：【{openId}】')
            # print(f'memberNo：【{memberNo}】')
            # print(f'memberId：【{self.memberId}】')
            return True
        else:
            Log('可能token失效了')
            return False

    def whetherSignIn(self):
        Log('>>>>>>查询签到')
        url ="https://campuscrm.pepsico.com.cn/web/user/member/whetherSignIn"

        response = self.make_request(url)
        if response.get('success',False):
            data = response.get('data', {})
            whetherSignIn = data.get('whetherSignIn', False)
            signInDay = data.get('signInDay', 0)
            todaySignInGrowth = data.get('todaySignInGrowth', 0)
            todaySignInPoints = data.get('todaySignInPoints', 0)
            if whetherSignIn:
                Log('今日未签到')
                self.signIn()
            else:
                Log(f'今日已签到，累计签到【{signInDay}】天，获得成长值【{todaySignInGrowth}】，获得积分【{todaySignInPoints}】')
            return True
        else:
            Log('可能token失效了')
            return False

    def signIn(self):
        Log('>>>>>>用户信息')
        url ="https://campuscrm.pepsico.com.cn/web/user/member/signIn"

        response = self.make_request(url)
        if response.get('success',False):
            data = response.get('data', {})
            if data:
                Log('签到成功！')
            return True
        else:
            Log('可能token失效了')
            return False


    def getArticleList(self):
        Log('>>>>>>获取文章')
        url ="https://campuscrm.pepsico.com.cn/web/user/original/getArticleList"
        data = self.default_data.copy()
        datas = {
            "categoryId": 0,
            "sort": 0,
            "pageNum": 10,
            "pageSize": 1
        }
        data.update(datas)
        # print(data)
        response = self.make_request(url,params=data)
        if response.get('success',False):
            data = response.get('data', {})
            if data:
                Log('获取文章成功！')
                list = data.get('list', [{}])
                # 随机选择一个帖子
                random_post = random.choice(list)
                self.shark(random_post)
            return True
        else:
            Log('可能token失效了')
            return False

    def shark(self,random_post):
        Log('>>>>>>分享文章')
        url ="https://campuscrm.pepsico.com.cn/web/user/original/shark"
        data = self.default_data.copy()
        if random_post:
            random_post_id=random_post.get('id','')
            datad = {
                "id":random_post_id
            }
        data.update(datad)
        # print(data)
        response = self.make_request(url, params=data)
        if response.get('success',False):
            data = response.get('data', {})
            if data == 'success':
                Log(f'文章【{random_post_id}】分享成功！')
            return True
        else:
            Log('可能token失效了')
            return False

    def userAddInfo(self):
        Log('>>>>>>发帖')
        url ="https://campuscrm.pepsico.com.cn/web/user/original/userAddInfo"
        data = self.default_data.copy()
        datad = {
            "categoryId": 76,
            "title": "我的乐事搭子，我的乐事范儿",
            "text": "我的乐事搭子当然是代言人范丞丞啦~",
            "coverImg": "https://pepsicocampuscrmstgblob.blob.core.chinacloudapi.cn/pepsicocampuscrmstgblob/FAQ_202405081630107224.jpeg",
            "imgs": "https://pepsicocampuscrmstgblob.blob.core.chinacloudapi.cn/pepsicocampuscrmstgblob/FAQ_202405081630107224.jpeg"
        }
        data.update(datad)
        # print(data)
        response = self.make_request(url, params=data)
        if response.get('success',False):
            data = response.get('data', {})
            if data:
                Log('发帖成功！')
                self.getUserList()
                return True
        else:
            Log('可能token失效了')
            return False

    def getUserList(self):
        Log('>>>>>>获取已发布帖子')
        url = "https://campuscrm.pepsico.com.cn/web/user/original/getUserList"
        data = self.default_data.copy()
        datad = {
            "pageNum": 1,
            "pageSize": 10
        }
        data.update(datad)
        # print(data)
        response = self.make_request(url, params=data)
        if response.get('success',False):
            data = response.get('data', {})
            post_list = data.get('list', [{}])
            for post in post_list:
                post_id = post["id"]
                title = post["title"]
                print("ID:", post_id)
                print("Title:", title)
                self.deleteUserInfo(post_id)
            return True
        else:
            Log('可能token失效了')
            return False

    def deleteUserInfo(self,originalInfoId):
        Log('>>>>>>删帖')
        url = "https://campuscrm.pepsico.com.cn/web/user/original/deleteUserInfo"
        data = self.default_data.copy()
        datad = {
            "originalInfoId": originalInfoId
        }
        data.update(datad)
        # print(data)
        response = self.make_request(url, params=data)
        if response.get('success',False):
            data = response.get('data', {})
            if data:
                Log(f'删帖[{originalInfoId}]成功！')
            return True
        else:
            Log('可能token失效了')
            return False

    def getMemberPoint(self):
        Log('>>>>>>获取积分信息')
        url = "https://campuscrm.pepsico.com.cn/web/user/point/getMemberPoint"
        # print(data)
        response = self.make_request(url)
        if response.get('success',False):
            data = response.get('data', {})
            Log(f'当前积分：【{data}】')
            return True
        else:
            Log('可能token失效了')
            return False


    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.access_refresh():
            self.getInfo()
            self.whetherSignIn()
            self.getArticleList()
            # 发帖无积分待修复
            # self.userAddInfo()
            self.getMemberPoint()
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
    APP_NAME = '乐事心动社小程序'
    ENV_NAME = 'LSXDS'
    CK_URL = 'https://campuscrm.pepsico.com.cn/web/user/member/access-refresh'
    CK_NAME = 'Authorization'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
      分享任务
✨ 抓包步骤：
      打开{APP_NAME}
      授权登陆
      打开抓包工具
      找{CK_URL}返回值[{CK_NAME}]
邀请码：
https://private-user-images.githubusercontent.com/160421895/328828056-75d87630-867f-41fe-8367-d28ce6bf3bd8.png
https://private-user-images.githubusercontent.com/160421895/328828354-528864ed-bde4-490e-bcd9-edb775035129.png
https://private-user-images.githubusercontent.com/160421895/328828400-b1e5866b-f201-4636-b0f3-c97e61efbf44.png
参数示例：eyJhbGciOiJxxxxxxxxx@8888888
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：抓完CK没事儿别打开小程序，重新打开小程序请重新抓包
✨ 推荐cron：1 8 * * *
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
            s = requests.session()
            s.verify = False
            run_result = RUN(infos, index).main()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)