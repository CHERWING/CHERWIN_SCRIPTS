# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "0 0,8 * * " script-path=xxx.py,tag=匹配cron用
# const $ = new Env('微信公众号：卡夫亨氏新厨艺')

import os
import random
import time
from datetime import date, datetime,time as times

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
            'Host': 'kraftheinzcrm-uat.kraftheinz.net.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090719) XWEB/8447 Flue',
            'token': self.token,
            'Accept': '*/*',
            'Origin': 'https://fscrm.kraftheinz.net.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://fscrm.kraftheinz.net.cn/?code=031NdLkl2SD8ac4BUKll2x4iqC2NdLkO&state=fid%3DN8d3E4AyKCBiu7DuBRNPlw&appid=wx65da983ae179e97b',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.baseUrl = 'https://kraftheinzcrm-uat.kraftheinz.net.cn/crm/public/index.php/api/v1/'

    def getUserInfo(self,End=False):
        global userid_list, username_list
        response = self.s.get(
            f'{self.baseUrl}getUserInfo',
            headers=self.headers
        )
        if response.status_code == 200:
            try:
                resp = response.json()
                data = resp.get('data',{})
                nickname = data.get('nickname','')
                openId = data.get('openId','')
                signTimes = data.get('signTimes',0)
                memberInfo = data.get('memberInfo', {})
                self.phone = memberInfo.get('phone', '')
                score = memberInfo.get('score', '')
                if End :
                    Log(f'执行后积分：【{score}】')
                    return True
                self.member_id = data.get('member_id','')
                # add = {"nickname":nickname,"member_id":member_id}
                userid_list.append(self.member_id)
                username_list.append(nickname)
                serialSign = data.get('serialSign', [{}])
                signTimes = data.get('signTimes', 0)
                Log(f'>>>当前用户：【{nickname}】\nID：【{self.member_id}】 \nOpenID:【{openId}】 \n已连续签到【{signTimes}】天')

                if serialSign:
                    current_date = date.today()
                    date_string = serialSign[0].get('createdAt',current_date)
                    memberBalance = serialSign[0].get('memberBalance', 0)
                    parsed_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').date()
                    if parsed_date == current_date:
                        print(f"今日已签到，当前积分：【{memberBalance}】")
                else:
                    print("今日未签到")
                    wait_time = random.randint(1000, 10000) / 1000.0  # 转换为秒
                    time.sleep(wait_time)
                    print('随机延时1-10秒执行签到')
                    self.dailySign()
                return True
            except:
                print(response.text)
                return False
        else:
            print("API访问失败！")
            return False


    def dailySign(self):
        print('执行签到')
        response = self.s.post(
            f'{self.baseUrl}dailySign',
            headers=self.headers
        )
        if response.status_code == 200:
            try:
                resp = response.json()
                msg = resp['msg']
                Log(f'>{msg}')
            except:
                print(response.text)
        else:
            print("API访问失败！")

    def getCookbookIndex(self):
        global Cookid_list
        data = {
            'page': '1',
            'pagesize': '30'
        }
        response = self.s.post(
            f'{self.baseUrl}getCookbookIndex',
            headers=self.headers, data=data
        )
        if response.status_code == 200:
            try:
                resp = response.json()
                id_list = resp['data']['chineseCookbook']['data']
                for i in id_list:
                    Cookid_list.append(i['id'])
                    # self.creatCookbookCode(i['id'])
                print(f'>获取到菜谱ID:【{Cookid_list}】')
            except:
                print(response.text)
        else:
            print("API访问失败！")

    def creatCookbookCode(self,cookbook_id):

        data = {
            'cookbook_id':cookbook_id
        }
        response = self.s.post(
            f'{self.baseUrl}createCookbookCode',
            headers=self.headers, data=data
        )
        if response.status_code == 200:
            try:
                resp = response.json()
                data = resp.get('data',{})
                code_url = data.get('code_url','')
                print(f'创建分享链接成功：[{code_url}]')
            except:
                print(response.text)
        else:
            print("API访问失败！")

    def recordScoreShare(self, cookbook_id, now_id):
        # print('')
        # self.getUserInfo()
        Log('开始互助')
        for id in userid_list:
            if now_id == id: continue
            # Log(f'>>>开始为【{id}】分享的菜谱【{cookbook_id}】助力')
            data = {
                'cookbook_id': cookbook_id,
                'invite_id': id,
            }
            response = self.s.post(
                f'{self.baseUrl}recordScoreShare',
                headers=self.headers, data=data
            )
            if response.status_code == 200:
                try:
                    resp = response.json()
                    msg = resp['msg']
                    Log(f'>为【{id}】助力结果：【{msg}】')
                except:
                    print(response.text)
            else:
                print("API访问失败！")

    def helpAuthor(self, authorid, cookbook_id, now_id):
        Log('开始助力作者')
        if now_id != authorid:
            data = {
                'cookbook_id': cookbook_id,
                'invite_id': authorid,
            }
            response = self.s.post(
                f'{self.baseUrl}recordScoreShare',
                headers=self.headers, data=data
            )
            if response.status_code == 200:
                try:
                    resp = response.json()
                    msg = resp['msg']
                    Log(f'>为【作者】助力结果：【{msg}】')
                except:
                    print(response.text)
            else:
                print("API访问失败！")
        else:
            Log('助力对象为自身，跳过')

    def exchange(self):
        data = {
            'phone': self.phone
        }
        huafei_li = ['全网10元话费', '全网20元话费']
        videoCard_li = ['爱奇艺', '腾讯', '优酷']
        cardType = ['年卡', '季卡', '月卡', '周卡']
        for card in huafei_li:
            data['value'] = card
            data['type'] = '话费'
            data['memberId'] = self.member_id
            self.exchangeIntegralNew(data)

        for card in cardType:
            for video in videoCard_li:
                cardname = video + card
                data['value'] = cardname
                data['type'] = '视频卡'
                self.exchangeIntegralNew(data)
                print(cardname)


    # 预留兑换函数
    def exchangeIntegralNew(self,data):
        print(f'正在尝试兑换【{data["value"]}】')
        response = self.s.post(
            f'{self.baseUrl}exchangeIntegralNew',
            headers=self.headers,
            data=data
        )
        if response.status_code == 200:
            try:
                resp = response.json()
                msg = resp['msg']
                Log(f'>{msg}')
            except:
                print(response.text)
        else:
            print("API访问失败！")

    def main(self):
        if self.getUserInfo():
            now = datetime.now().time()
            start_time = times(23, 59, 59)
            end_time = times(0, 5)
            if start_time <= now <= end_time:
                self.exchange()
            self.getCookbookIndex()
            self.getUserInfo(True)
            self.sendMsg()
            return True
        else:
            self.sendMsg()
            return False

    def help(self):
        # print(Cookid_list)
        # print(username_list)
        # print(userid_list)
        if Cookid_list and username_list and userid_list:
            cookbook_id = random.choice(Cookid_list)
            username = username_list[self.index-1]
            now_id = userid_list[self.index-1]
            Log(f'\n当前用于助力用户:【{username}】 ID:【{now_id}】')
            self.helpAuthor(659402, cookbook_id, now_id)
            self.helpAuthor(659403, cookbook_id, now_id)
            self.helpAuthor(659404, cookbook_id, now_id)
            self.helpAuthor(659405, cookbook_id, now_id)
            self.helpAuthor(659406, cookbook_id, now_id)
            self.recordScoreShare(cookbook_id, now_id)
            self.sendMsg(True)
            return True
        else:
            return False


    def sendMsg(self,help=False):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME,help)
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
    # print(APP_NAME, local_script_name, ENV_NAME,local_version)
    ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode = CHERWIN_TOOLS.main(APP_NAME, local_script_name, ENV_NAME,local_version)




if __name__ == '__main__':
    APP_NAME = '卡夫亨氏新厨艺'
    ENV_NAME = 'KFHS'
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
✨ 注册链接（复制微信打开）：
https://fscrm.kraftheinz.net.cn/?from=N8d3E4AyKCBiu7DuBRNPlw==#/

https://kraftheinzcrm-uat.kraftheinz.net.cn/?from=FoAgXkwvgZl6SOyJ2ekGrg==
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
参数示例：Fks8FqmiTksnmZSj2fDvxxxxxxxxx@UID_xxxxx
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}参数值'多账号#或&分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ ✨ 注意：token有效期7天，7天后重新抓
✨ 推荐cron：0 0,8 * * 
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.06.03'
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
    # print(token)
    if not token:
        print(f"未填写{ENV_NAME}变量\n青龙可在环境变量设置 {ENV_NAME} 或者在本脚本文件上方将{CK_NAME}填入token =''")
        exit()
    tokens = CHERWIN_TOOLS.ENV_SPLIT(token)
    # print(tokens)
    Cookid_list = []
    userid_list = []
    username_list = []
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).main()
            if not run_result: continue
        print(f"\n>>>>>>>>>>开始互助<<<<<<<<<<")
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).help()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
