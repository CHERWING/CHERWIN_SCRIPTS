# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 6 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('口味王小程序签到')

import os
import random
import time

import requests
import hashlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# import CHERWIN_TOOLS
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
if os.path.isfile('DEV_ENV.py'):
    import DEV_ENV
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
        self.memberId = split_info[0]
        self.unionId = split_info[1]
        self.openId = split_info[2]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            print('检测到设置了UID')
            print(last_info)
            self.send_UID = last_info
        self.index = index + 1


        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/9079"

        self.headers = {
            "Host": "member.kwwblcj.com",
            "xweb_xhr": "1",
            "User-Agent": self.UA,
            "user-paramname": "memberId",
            "Content-Type": "application/json",
            "Accept": "/",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wxfb0905b0787971ad/101/page-frame.html",
            "Accept-Language": "zh-CN,zh;q=0.9"
            }

    def wxHeards(self):
        timestamp = int(time.time() * 1000)
        random_num = random.randint(0, 31)
        u = [
            "A", "Z", "B", "Y", "C", "X", "D", "T", "E", "S", "F", "R", "G", "Q", "H", "P", "I", "O", "J", "N", "k",
            "M", "L", "a", "c", "d", "f", "h", "k", "p", "y", "n"]
        r = f"{timestamp}{self.memberId}{u[random_num]}"
        sign = hashlib.md5(r.encode()).hexdigest()
        update_headers = {
            "user-sign": sign,
            "user-paramname": "memberId",
            "user-timestamp": str(timestamp),
            "user-random": str(random_num)
        }
        self.headers.update(update_headers)

        return
    def do_request(self,  url , method='POST', params=None, data=None, headers=None):
        self.wxHeards()
        if not headers:
            headers = self.headers
        try:
            response = s.request(method, url, params=params, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"请求错误: {e}")
            return None

    def memberInfo(self):
        print('>>>>>>获取用户信息')
        try:
            url = f"https://member.kwwblcj.com/member/api/info/?userKeys=v1.0&pageName=member-info-index-search&formName=searchForm&kwwMember.memberId={self.memberId}&kwwMember.unionid={self.unionId}&memberId={self.memberId}"
            response = self.do_request(url,'GET')
            if response and response.get('msg') == "查询成功":
                result = response.get('result',{})
                memberInfo = result.get('memberInfo',{})
                self.userCname = memberInfo.get('userCname','')
                Log(f'当前用户：【{self.userCname}】')
                return True
            else:
                print(f"登陆获取token失败: {response}")
                return False
        except Exception as e:
            print(f"登陆获取token异常: {e}")
            return False



    def get_task_list(self):
        print('>>>>>>获取任务列表')
        # try:
        url = f"https://member.kwwblcj.com/member/api/list/?userKeys=v1.0&pageName=select-task-list&formName=searchForm&page=1&rows=20&memberId={self.memberId}"
        response = self.do_request(url,'GET')
        if response and response.get('msg') == "查询成功":
            rows = response.get('rows',[{}])
            for task in rows:
                self.taskLimit = task.get('taskLimit','')
                self.taskTitle = task.get('taskTitle','')
                self.subTitle = task.get('subTitle','')
                self.complete = task.get('complete','')
                self.rewardScore = task.get('rewardScore','')
                self.ruleType = task.get('ruleType','')
                self.infoId = task.get('infoId','')
                # print(f'\n当前任务:【{self.taskTitle}】\n任务要求:【{self.subTitle}】\n任务奖励:【{self.rewardScore}】\ninfoId：【{self.infoId}】\nruleType：【{self.ruleType}】')
                print(f'当前任务:【{self.taskTitle}】')
                if self.complete == '1':
                    print('任务已完成！')
                    continue
                if self.taskTitle == '每日阅读':
                    self.ReadTask()

                elif self.taskTitle == "收青果":
                    self.activity()

                # elif self.taskTitle == "每日答题":
                #     pass
                    # self.loginFreePlugin()
                else:
                    print('暂不支持此任务')
            wait_time = random.randint(2, 4)  # 转换为秒
            time.sleep(wait_time)  # 等待
            return True
        else:
            print(f"获取任务列表失败: {response}")
            return False
        # except Exception as e:
        #     print(f"获取任务列表异常: {e}")
        #     return False

    def activity(self):
        print(f'>>>>>>{self.taskTitle}')
        try:
            url = f"https://member.kwwblcj.com/member/api/list/?userKeys=v1.0&pageName=activeTaskFlag&formName=editForm&memberId={self.memberId}&userCname={self.userCname}&page=1&rows=2"

            response = self.do_request(url,'GET')

            # url2 = f"https://member.kwwblcj.com/member/api/list/?userKeys=v1.0&pageName=memberTaskInfo&formName=searchForm&page=1&rows=2&memberId={self.memberId}"
            # response = self.do_request(url2, 'GET')
            #
            if response and response.get('flag') == "T":
                print(f'访问：【{self.taskTitle}】成功！')
                return True
            else:
                print(f"{self.taskTitle}失败: {response}")
                return False
        except Exception as e:
            print(f"{self.taskTitle}异常: {e}")
            return False


    def ReadTask(self):
        print(f'>>>>>>{self.taskTitle}')
        try:
            url = f"https://member.kwwblcj.com/member/api/list/?userKeys=v1.0&pageName=setNewsReadTaskFlag&formName=addForm&memberId={self.memberId}&userCname={self.userCname}&articleTitle=3.15&actionType=articleRead&actionDesc=3.15https%3A%2F%2Fmp.weixin.qq.com%2Fs%2F_2N3AQ12lbXfBSSPja-Q0Q&memberName={self.userCname}&objId=C01&page=1&rows=2"

            response = self.do_request(url,'GET')

            if response and response.get('flag') == "T":

                print(f'阅读成功！')
                return True
            else:
                print(f"{self.taskTitle}失败: {response}")
                return False
        except Exception as e:
            print(f"{self.taskTitle}异常: {e}")
            return False

    def getPoint(self):
        try:
            url = f"https://member.kwwblcj.com/member/api/list/?userKeys=v1.0&pageName=me-funds&formName=searchForm&userId={self.memberId}&page=1&rows=2&memberId={self.memberId}"

            response = self.do_request(url,'GET')
            if response and response.get('flag') == "T":
                rows = response.get('rows',{})
                balance = rows.get('balance','')
                # print(response)
                Log(f'当前积分：【{balance}】\n')
                return True
            else:
                print(f"获取积分信息失败: {response}")
                return False
        except Exception as e:
            print(f"获取积分信息异常: {e}")
            return False

    def loginFreePlugin(self):
        print(f'>>>>>>{self.taskTitle}')
        try:
            url = f"https://member.kwwblcj.com/member/api/info/?userKeys=v1.0&pageName=loginFreePlugin&formName=searchForm&uid={self.memberId}&levelCode=K1&redirect=https%3A%2F%2F89420.activity-20.m.duiba.com.cn%2Fprojectx%2Fp129446ea%2Findex.html%3FappID%3D89420&memberId={self.memberId}"
            response = self.do_request(url,'GET')
            if response and response.get('msg') == "信息获取成功！":
                result = response.get('result',{})
                self.autologin(result)
                return True
            else:
                print(f"{self.taskTitle}失败: {response}")
                return False
        except Exception as e:
            print(f"{self.taskTitle}异常: {e}")
            return False

    def autologin(self,url):
        try:
            headers = {
                "Host": "89420.activity-20.m.duiba.com.cn",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/9079",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "navigate",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "accept-language": "zh-CN,zh;q=0.9"
            }

            response = s.get(url, headers=headers,allow_redirects=True)
            print(response.text)
            url = 'https://89420.activity-20.m.duiba.com.cn/projectx/p129446ea/coop_frontVariable.query?user_type=0&is_from_share=1&_t=1710789863411'

            response = s.get(url, headers=headers)
            print(response.text)
            # if response and response.get('msg') == "信息获取成功！":
            #     result = response.get('result',{})
            #
            #     return True
            # else:
            #     print(f"{self.taskTitle}失败: {response}")
            #     return False
        except Exception as e:
            print(f"{self.taskTitle}异常: {e}")
            return False



    def main(self):
        print(f"\n开始执行第{self.index}个账号--------------->>>>>")
        # self.memberInfo()
        if self.memberInfo():
            self.get_task_list()
            self.getPoint()
            self.sendMsg()
            return True
        else:
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
    APP_NAME = '口味王会员中心小程序'
    ENV_NAME = 'KWW'
    CK_NAME = 'memberId@unionid@openid'
    CK_URL= '/member/api/info/'
    print(f'''
✨✨✨ {APP_NAME}签到✨✨✨
✨ 功能：
      积分签到
      部分积分任务
✨ 抓包步骤：
      打开抓包工具
      打开{APP_NAME}
      授权登陆
      找{CK_URL}的URl提取请求[{CK_NAME}]（@符号连接）
参数示例：4249095xxxxxx@oWmTE6IqrlDFRzxxxxx@o_V6_5btlEBzxxxxxx
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ 推荐cron：0 9 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.04.06'
    if os.path.isfile('CHERWIN_TOOLS.py'):
        import_Tools()
    else:
        if down_file('CHERWIN_TOOLS.py', 'https://py.cherwin.cn/CHERWIN_TOOLS.py'):
            print('脚本依赖下载完成请重新运行脚本')
            import_Tools()
        else:
            print('脚本依赖下载失败，请到https://py.cherwin.cn/CHERWIN_TOOLS.py下载最新版本依赖')
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



