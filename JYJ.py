# !/usr/bin/python3
# -- coding: utf-8 --
# cron "5 10 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('劲友家小程序')
import base64
import json
import os
import random
import time
import urllib

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
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


# 请保留作者邀请，谢谢
Author_inviteCustId = ['1797269977598922752', '1797253239272509440', '1797354681178132480', '787259516457639936',
                       '1797356377962844160']


class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        self.token = split_info[0]
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
            'Host': 'jjw.jingjiu.com',
            'accept': 'application/json, text/plain, */*',
            'xweb_xhr': '1',
            'appid': 'wx10bc773e0851aedd',
            'authorization': self.token,
            'user-agent': self.UA,
            'content-type': 'application/x-www-form-urlencoded',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://servicewechat.com/wx10bc773e0851aedd/618/page-frame.html',
            'accept-language': 'zh-CN,zh;q=0.9',
        }
        self.s = requests.session()
        self.s.verify = False
        self.baseUrl = 'https://jjw.jingjiu.com/app-jingyoujia/app/'

    def make_request(self, url, method='post', headers={}, json_data={}, params=None, data=None):
        if headers == {}:
            headers = self.headers
        try:
            if method.lower() == 'get':
                response = self.s.get(url, headers=headers, verify=False, params=params)
            elif method.lower() == 'post':
                headers = self.headers.copy()
                headers['accept'] = 'application/json, text/plain, */*'
                headers['content-type'] = 'application/json'
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

    def encrypt(self, data):
        data = json.dumps(data)
        key = "Z0J7M480h6kppf67"
        # 将密钥和数据转换为字节
        key_bytes = key.encode('utf-8')
        data_bytes = data.encode('utf-8')

        # 使用AES进行加密（ECB模式，PKCS7填充）
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted_bytes = cipher.encrypt(pad(data_bytes, AES.block_size))

        # 将加密后的数据转换为base64编码的字符串
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_base64

    def random_city_coordinates(self):
        print('\n====== 随机选择定位 ======')
        # 定义各个地区的经纬度边界（大致范围）
        regions = {
            "北京": {"min_lat": 39.26, "max_lat": 41.03, "min_lon": 115.25, "max_lon": 117.30},
            "上海": {"min_lat": 30.40, "max_lat": 31.53, "min_lon": 120.51, "max_lon": 122.12},
            "浙江": {"min_lat": 27.10, "max_lat": 31.53, "min_lon": 118.00, "max_lon": 123.00},
            "深圳": {"min_lat": 22.45, "max_lat": 22.75, "min_lon": 113.75, "max_lon": 114.63},
            "广州": {"min_lat": 22.26, "max_lat": 23.92, "min_lon": 112.57, "max_lon": 114.03},
            "江苏": {"min_lat": 30.75, "max_lat": 35.20, "min_lon": 116.18, "max_lon": 121.56},
            "福建": {"min_lat": 23.50, "max_lat": 28.22, "min_lon": 116.40, "max_lon": 120.43}
        }

        # 随机选择一个地区
        selected_region = random.choice(list(regions.keys()))
        region = regions[selected_region]

        # 随机生成该地区的经纬度，并保留15位小数
        latitude = round(random.uniform(region["min_lat"], region["max_lat"]), 15)
        longitude = round(random.uniform(region["min_lon"], region["max_lon"]), 15)
        print(f"随机生成的【{selected_region}】境内经纬度坐标：\n纬度={latitude:.15f}\n经度={longitude:.15f}")

        return selected_region, latitude, longitude

    def generate_positive_comment(self):
        subjects = [
            "今天", "这一天", "现在", "此刻", "每一天", "每一刻", "每时每刻", "未来"
        ]

        verbs = [
            "充满希望", "充满阳光", "美好", "令人期待", "值得期待", "光辉灿烂", "充满可能", "无限美好"
        ]

        adjectives = [
            "积极", "快乐", "充满活力", "动力满满", "能量满满", "振奋", "鼓舞人心", "激动人心"
        ]

        encouragements = [
            "你真的很棒", "继续加油", "保持积极的心态", "相信自己", "不要放弃", "你的努力会有回报", "你能行", "你是最棒的"
        ]

        actions = [
            "继续前行", "努力奋斗", "坚持不懈", "勇敢追梦", "微笑面对生活", "不断进步", "追求卓越", "克服困难"
        ]

        endings = [
            "加油！", "你会成功的！", "相信自己！", "美好的事情正在发生！", "未来属于你！", "你一定能做到！", "前途一片光明！",
            "今天会很棒！"
        ]

        emojis = [
            "💪", "👍", "🌟", "😊", "🚀", "💖", "🌈", "☀️", "😁", "🏆", "✨", "👏", "🔥", "🎉", "🌻"
        ]

        subject = random.choice(subjects)
        verb = random.choice(verbs)
        adjective = random.choice(adjectives)
        encouragement = random.choice(encouragements)
        action = random.choice(actions)
        ending = random.choice(endings)
        emoji = random.choice(emojis)

        comment = f"{subject} {verb}且{adjective}！{encouragement}，{action}。{ending} {emoji}"

        return comment

    def get_user_info(self):
        act_name = '获取用户信息'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/customer/detail"
        response = self.make_request(url, method='get')
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            nickName = data.get('nickName', '')
            mobile = data.get('mobile', '')
            self.custId = data.get('custId', '')

            mobile = mobile[:3] + "*" * 4 + mobile[7:]
            Log(f"> 用户名：{nickName}\n> 手机号：{mobile}\n> ID：{self.custId}")
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_user_point(self, END=False):
        act_name = '获取积分信息'
        # 使用 Log 或 print 打印操作名
        log_or_print = Log if END else print
        log_or_print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/customer/queryIntegralLog?changeDirection=1&dateType=0"
        response = self.make_request(url, method='get')
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            totalIncIntegral = data.get('totalIncIntegral', '')
            log_or_print(f"> 执行{'后' if END else '前'}积分：{totalIncIntegral}")
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def get_TopicList(self):
        act_name = '获取文章列表'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}ugcExcellent/queryUgcExcellentTopicList?pageNum=1&pageSize=20&topicType=35&themeId="
        response = self.make_request(url, method='get')
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            rows = response.get('rows', {})
            random_topic = random.choice(rows)
            topicId = random_topic.get('topicId', '')
            topic = random_topic.get('topic', '')
            imgList = random_topic.get('imgList', '')
            if len(imgList) > 0:
                imgurl = imgList[0]

            print(f"> 随机文章【{topic}】 id：【{topicId}】")
            self.sendTopicLike(topicId, '点赞')
            random_delay(3, 5)
            self.sendTopicLike(topicId, '取消点赞')
            random_delay()
            self.addComment(topicId)
            random_delay()
            self.queryVoteInfo(imgurl)
            random_delay()

            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def queryVoteInfo(self, imgurl):
        act_name = '获取投票话题状态'
        # 使用 Log 或 print 打印操作名
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/ugcVote/queryVoteInfo/35"
        response = self.make_request(url, method='get')
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            alreadyVote = data.get('alreadyVote', '')
            voteInfoList = data.get('voteInfoList', [])
            quizId = voteInfoList[0].get('quizId', '')
            print(f"> 获取到话题id：{quizId}")
            if alreadyVote:
                self.hotTopic(imgurl)
                return True
            if quizId:
                if self.vote(quizId):
                    self.hotTopic(imgurl)
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def vote(self, quizId):
        act_name = '话题投票'
        # 使用 Log 或 print 打印操作名
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/ugcVote/vote"
        data = {
            "topicType": 35,
            "voteInfoList": [{
                "quizId": quizId,
                "optionMarkList": ["B"]
            }]
        }
        response = self.make_request(url, json_data=data)
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            data = response.get('data', False)
            return data
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def sendTopicLike(self, topicId, type='点赞'):
        act_name = type
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/ugc/sendTopicLike"
        json_data = {
            "invokeType": 1,
            "topicId": topicId
        }
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == 200:
            print(f'>> {act_name}成功！✅')
            data = response.get('data', {})
            rewardResult = data.get('rewardResult', '')
            rewardNum = data.get('rewardNum', '')
            if rewardResult:
                print(f"> 获得【{rewardNum}】积分")
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def addComment(self, topicId):
        act_name = '评论'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/ugc/addComment"
        content = self.generate_positive_comment()
        print(f'> 随机评论：【{content}】')
        json_data = {
            "invokeType": 1,
            "topicId": topicId,
            "content": content
        }
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == 200:
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            rewardResult = data.get('rewardResult', '')
            rewardNum = data.get('rewardNum', '')
            if rewardResult:
                print(f"> 获得【{rewardNum}】积分")
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def hotTopic(self, imgurl):
        act_name = '发帖'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/ugc/hotTopic"
        content = self.generate_positive_comment()
        print(f'随机帖子：【{content}】')
        json_data = {
            "content": content,
            "imgList": [imgurl],
            "topicType": 35,
            "themeId": 62
        }
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == 200:
            print(f'> {act_name}成功！✅')
            self.finish_task()
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def finish_task(self):
        act_name = '完成任务'
        print(f'====== {act_name} ======')
        url = f"https://jjw.jingjiu.com/app-jingyoujia/business/member/task/finish"
        json_data = {
            "taskType": self.taskType,
            "lat": self.lat,
            "lon": self.lon
        }
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == 200:
            print(f'> {act_name}成功！✅')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def currentGrowMedicine(self):
        act_name = '获取药材成长信息'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/currentGrowMedicine"
        MedicineLi = {
            1: "枸杞",
            2: "淮山药",
            3: "肉苁蓉",
            4: "仙茅",
            5: "肉桂",
            6: "当归 ",
            7: "丁香",
            8: "淫羊藿",
            9: "黄芪"
        }
        response = self.make_request(url, method='get')
        if response.get('code', -1) == 200:
            data = response.get('data', {})
            print(f'{act_name}成功！✅')
            # 药材类型
            medicineType = data.get('medicineType', '')
            Log(f'> 当前药材：【{MedicineLi[medicineType]}】')
            # 总需水量
            totalWaterNum = data.get('totalWaterNum', '')
            # 剩余总需水量
            totalSurplusWaterNum = data.get('totalSurplusWaterNum', '')
            # 当前阶段剩余需水量
            surplusWaterNum = data.get('surplusWaterNum', '')
            # 当前阶段总需水量
            currentStageWaterNum = data.get('currentStageWaterNum', '')
            # 当前已浇水量
            totalDoneWaterNum = data.get('totalDoneWaterNum', '')
            Log(f'> 当前阶段进度：{(currentStageWaterNum - surplusWaterNum)}/{currentStageWaterNum}')
            Log(f'> 当前阶段剩余需水量：{surplusWaterNum}')
            Log(f'> 总进度：{totalDoneWaterNum}/{totalWaterNum}')
            Log(f'> 剩余总需水量：{totalSurplusWaterNum}')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def taskList(self):
        act_name = '获取任务列表'
        Log(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/task/taskList"

        response = self.make_request(url, method='get')
        if response.get('code', -1) == 200:
            data = response.get('data', '')
            print(f'{act_name}成功！✅')
            for task in data:
                self.taskType = task.get('taskType', '')
                finish = task.get('finish', '')
                name = task.get('name', '')
                Log(f'>> 当前任务【{name}】')
                skip_task = [1, 2, 5, 9]
                if self.taskType in skip_task:
                    print('暂不支持，跳过')
                    continue
                if finish:
                    Log(f'> 已完成✅')
                    continue
                if name == '生活圈互动领水滴':
                    self.get_TopicList()
                elif name == '每日浇水领水滴':
                    for i in range(3):
                        self.water(i + 1)
                        random_delay(3, 5)
                elif name == '订阅提醒领水滴':
                    self.subscribe()
                elif name == '【翻倍】健康打卡领水滴':
                    self.photoPunch()
                random_delay()
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def subscribe(self):
        act_name = f'订阅通知'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/task/subscribe"
        json_data = {
            "lat": self.lat,
            "lon": self.lon
        }
        data = {
            "v1": self.encrypt(json_data)
        }

        response = self.make_request(url, json_data=data)
        if response.get('code', -1) == 200:
            print(f'> {act_name}成功！✅')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def photoPunch(self):
        act_name = f'拍照打卡'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/activityCommon/photoPunch"
        json_data = {
            "activityType": "MOUNTAIN_CLIMBING_2024",
            "recordUrl": "https://jjw-oos.jingjiu.com/jingyoujia/images/pages/online-punch/example.png",
            "code": "",
            "lat": self.lat,
            "lon": self.lon
        }
        response = self.make_request(url, json_data=json_data)
        if response.get('code', -1) == 200:
            data = response.get('data', {})
            print(f'{act_name}成功！✅')
            water = data.get('water', False)
            if water:
                waterNum = data.get('waterNum', 0)
                print(f'> 获得【{waterNum}】水滴')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def water(self, i):
        act_name = f'第【{i}】次浇水'
        print(f'====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/water"
        json_data = {
            "lat": self.lat,
            "lon": self.lon
        }
        data = {
            "v1": self.encrypt(json_data)
        }
        response = self.make_request(url, json_data=data)
        if response.get('code', -1) == 200:
            print(f'> {act_name}成功！✅')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def everyDayWaterStatus(self):
        act_name = f'获取每日水滴状态'
        print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/user/everyDayWaterStatus"

        params = {
            'lat': self.lat,
            'lon': self.lon,
        }

        response = self.make_request(url, method='get', params=params)
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            data = response.get('data', False)
            if data:
                print('> 可领取')
                self.everyDayWater()
            else:
                print('> 已领取')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def game_userInfo(self, END=False):
        act_name = f'获取水滴数量'
        # 使用 Log 或 print 打印操作名
        log_or_print = Log if END else print
        log_or_print(f'\n====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/user/userInfo"

        params = {
            'lat': self.lat,
            'lon': self.lon,
        }

        response = self.make_request(url, method='get', params=params)
        if response.get('code', -1) == 200:
            print(f'{act_name}成功！✅')
            data = response.get('data', {})
            waterNum = data.get('waterNum', 0)
            log_or_print(f'> 当前剩余水滴【{waterNum}】')
            log_or_print(f'> 可浇水【{waterNum // 10}】次')
            if waterNum > 0:
                for i in range(waterNum // 10):
                    self.water(i + 1)
                    random_delay(2, 5)
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def everyDayWater(self):
        act_name = f'领取每日水滴'
        print(f'====== {act_name} ======')
        url = f"{self.baseUrl}jingyoujia/game/user/everyDayWater"
        json_data = {
            "lat": self.lat,
            "lon": self.lon
        }
        data = {
            "v1": self.encrypt(json_data)
        }
        response = self.make_request(url, json_data=data)
        if response.get('code', -1) == 200:
            data = response.get('data', 0)
            print(f'> {act_name}成功！✅')
            print(f'> 获得：【{data}】水滴')
            return True
        elif not response:
            Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
            return False
        else:
            print(response)
            return False

    def invite(self):
        act_name = f'助力'
        print(f'====== {act_name} ======')
        max_help = 3
        url = f"{self.baseUrl}jingyoujia/game/user/invite"
        for code in Author_inviteCustId:
            if max_help < 1: break
            if code == self.custId:
                print('> 跳过助力自己')
                continue
            json_data = {
                "inviteCustId": code,
                "lat": self.lat,
                "lon": self.lon
            }
            data = {
                "v1": self.encrypt(json_data)
            }
            response = self.make_request(url, json_data=data)
            if response.get('code', -1) == 200:
                data = response.get('data', 0)
                success = data.get('success', False)
                if success:
                    print(f'> 助力成功！剩余可助力【{max_help}】次✅')
                    max_help -= 1
                elif data.get('msg', '') == '今日己为他助力过啦~明天再来':
                    print(f'> 助力失败：已助力过！❌')
                    max_help -= 1
                else:
                    msg = data.get('msg', '')
                    print(f'> 助力失败：{msg}❌')

            elif not response:
                Log(f"> 账号 {self.index}: ck过期 请重新抓取❌")
                continue
            else:
                print(response)
                continue
        random_delay(2, 5)

    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.get_user_info():
            self.region, self.lat, self.lon = self.random_city_coordinates()
            self.everyDayWaterStatus()
            self.invite()
            self.taskList()
            self.game_userInfo()
            self.game_userInfo(True)
            self.currentGrowMedicine()
            self.get_user_point(True)
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
    APP_NAME = '劲友家小程序'
    ENV_NAME = 'JYJ'
    CK_URL = 'jjw.jingjiu.com请求头'
    CK_NAME = 'authorization'
    CK_EX = 'JYJwx eyJ0eXAiOxxxxx'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ 功能：
    互动：发帖、点赞、收藏、分享 劲酒庄园：部分日常任务
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
✨ 推荐cron：5 10 * * *
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
        # if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)
