# !/usr/bin/python3
# -- coding: utf-8 --
# cron "20 9 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('老板电器服务微商城小程序')
import hashlib
import json
import os
import random
import time
from datetime import datetime, time as times
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
        self.openid = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            print('检测到设置了UID')
            print(last_info)
            self.send_UID = last_info
        self.index = index + 1
        # print(self.access_token)
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b) XWEB/9129"

        self.headers = {
            "Host": "vip.foxech.com",
            "xweb_xhr": "1",
            "User-Agent": self.UA,
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://servicewechat.com/wxc8c90950cf4546f6/154/page-frame.html",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.s = requests.session()
        self.s.verify = False
        self.baseUrl = 'https://vip.foxech.com/index.php/api/'

    def make_request(self, url, method='post', headers={}, json_data={}, params=None, data=None):
        if headers == {}:
            headers = self.headers
        try:
            if method.lower() == 'get':
                response = self.s.get(url, headers=headers, verify=False, params=params)
            elif method.lower() == 'post':
                response = self.s.post(url, headers=headers, json=json_data, data=data, params=params, verify=False)
            else:
                raise ValueError("不支持的请求方法❌: " + method)
            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常❌：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法❌：", e)
        except Exception as e:
            print("发生了未知错误❌：", e)

    def gen_token(self):
        current_timestamp_ms = int(time.time() * 1000)
        raw_string = f'{current_timestamp_ms}wqewq{self.openid}'
        md5_hash = hashlib.md5(raw_string.encode())
        token = md5_hash.hexdigest()
        json_data = {
            "is_need_sync": 1,
            "timestamp": current_timestamp_ms,
            "token": token,
            "openid": self.openid
        }
        return json_data

    def get_user_info(self, END=False):
        act_name = '获取用户信息'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}member/get_member_info"
        json_data = self.gen_token()
        response = self.make_request(url, json_data=json_data)

        if response.get('code', -1) == "200":
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            info = data.get('info', {})
            nickname = info.get('nickname', '')
            mobile = info.get('mobile', '')
            score = info.get('score', '')
            mobile = mobile[:3] + "*" * 4 + mobile[7:]
            if END:
                Log(f"> 执行后积分：{score}")
            else:
                Log(f"> 用户名：{nickname}\n> 手机号：{mobile}\n> 当前积分：{score}")
            return True
        elif not response:
            print(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_member_score_mission_list(self):
        act_name = '获取任务列表'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}member/get_member_score_mission_list"
        json_data = self.gen_token()
        json_data['page'] = 1
        json_data['limit'] = 1000
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == "200":
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            list = data.get('list', [{}])
            for tasks in list:
                title = tasks.get('title', '')
                type = tasks.get('type', '')
                is_over = tasks.get('is_over', '')
                id = tasks.get('id', '')
                Log(f'>> 当前任务：【{title}】')
                if is_over == 1:
                    Log(f'> 已完成✅')
                    continue
                if id == 16:
                    self.user_sign()
                elif id == 7:
                    self.get_list('get_goods_list')
                # elif id == 8:
                #     self.get_list('get_ms_list')
                elif id == 12:
                    self.get_list()
                else:
                    Log('> 暂不支持，跳过❌')
            return True
        elif not response:
            print(f">账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_sign_week(self):
        act_name = '获取签到状态'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}member/get_sign_week"
        json_data = self.gen_token()

        response = self.make_request(url, json_data=json_data)

        if response.get('code', -1) == "200":
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            day = data.get('day', 0)
            Log(f'> 累计签到：【{day}】天')
            list = data.get('list', {})
            nowday = datetime.now().strftime("%Y%m%d")
            # print(f'今天是：【{nowday}】')
            for days in list:
                date = days.get('date', '')
                is_sign = days.get('is_sign', '')
                if date == nowday and is_sign == 0:
                    Log(f'> 今日未签到！❌')
                    self.user_sign()
                elif date == nowday and is_sign == 1:
                    Log(f'> 今日已签到！✅')
            if day >= 7:
                self.get_sign_prize_list()
            return True
        elif not response:
            print(f">账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def user_sign(self):
        act_name = '签到'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}member/user_sign"
        json_data = self.gen_token()
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == "200":
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            score = data.get('score', '')
            Log(f'> 获得【{score}】积分')
            return True
        elif not response:
            print(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_sign_prize(self, id, title):
        act_name = f'领取[{title}]奖励'
        Log(f'====== {act_name} ======')
        url = f"{self.baseUrl}member/get_sign_prize"
        json_data = self.gen_token()
        json_data['id'] = id
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == "200":
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            score = data.get('score', '')
            Log(f'> 获得【{score}】积分✅')
            return True
        elif not response:
            print(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_sign_prize_list(self):
        act_name = '获取连续签到状态'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}member/get_sign_prize_list"
        json_data = self.gen_token()

        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == "200":
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            list = data.get('list', [{}])
            for li in list:
                id = li.get('id', '')
                title = li.get('title', '')
                status = li.get('status', '')
                if status == 1:
                    print(f'> 【{title}】未领取❌')
                    self.get_sign_prize(id, title)
                elif status == 2:
                    print(f'> 【{title}】已领取✅')
                elif status == 0:
                    print(f'> 【{title}】未达到指定天数❌')
            return True
        elif not response:
            print(f">账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_detail(self, title, id, type='get_news_detail', ms_id=''):
        act_name = f'浏览[{title}]'
        print(f'====== {act_name} ======')
        json_data = self.gen_token()
        if 'goods' in type:
            json_data['id'] = id
            json_data['is_act'] = ''
        elif 'ms' in type:
            json_data['goods_id'] = id
            json_data['ms_id'] = ms_id
        else:
            json_data['id'] = id

        url = f"{self.baseUrl}common/{type}"
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == "200":
            data = response.get('data', {})
            info = data.get('info', False)
            if info:
                print(f'> {act_name}成功！✅')
            return True
        elif not response:
            print(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_list(self, type='get_news_list'):
        if 'news' in type:
            act_name = '获取文章列表'
        elif 'ms' in type:
            act_name = '获取秒杀列表'
        elif 'goods' in type:
            act_name = '获取商品列表'
        Log(f'====== {act_name} ======')
        url = f"{self.baseUrl}common/{type}"
        json_data = self.gen_token()
        json_data['page'] = 1
        json_data['limit'] = 20
        if 'goods' in type:
            json_data['category'] = ''
        else:
            json_data['category'] = 4

        json_data['flag'] = 1

        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == "200":
            data = response.get('data', {})
            list = data.get('list', False)
            if list == []:
                print(f'{act_name}失败！❌')
                return
            print(f'{act_name}成功！✅')
            for i in range(3):
                random_post = random.choice(list)
                postid = random_post['id']
                posttitle = random_post['title']
                ms_id = random_post.get('ms_id', '')
                print(f'> 随机选择的文章：【{posttitle}】\n> ID【{postid}】')
                if 'news' in type:
                    self.get_detail(posttitle, postid)
                elif 'ms' in type:
                    self.get_detail(posttitle, postid, 'get_ms_goods_detail', ms_id=ms_id)
                else:
                    self.get_detail(posttitle, postid, 'get_goods_detail')
                random_delay()
            return True
        elif not response:
            print(f">账号 {self.index}: ck过期 请重新抓取")
            return False
        else:
            print(response)
            return False

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.get_user_info():
            random_delay(1,30)
            self.get_sign_week()
            random_delay()
            self.get_member_score_mission_list()
            random_delay()
            self.get_user_info(True)
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
    print(f">本次随机延迟：【{delay:.2f}】 秒.....")
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
    APP_NAME = '老板电器服务微商城小程序'
    ENV_NAME = 'LBDQ'
    CK_URL = 'vip.foxech.com请求头'
    CK_NAME = 'openid'
    CK_EX = 'oZXiL5b-xxxxxxxxxxxxx'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ 功能：
        积分签到 浏览商品 浏览文章
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
✨ 推荐cron：20 9 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.06.01'
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
