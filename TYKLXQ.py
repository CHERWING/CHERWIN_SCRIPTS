# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "5 9,18 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('统一快乐星球小程序')
import hashlib
import os
import random
import re
import time
from datetime import datetime

import requests

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


def Log(cont='',Notsend = False):
    global send_msg, one_msg
    if not cont:return
    if not Notsend:
        print(cont)
        one_msg += f'{cont}\n'
        send_msg += f'{cont}\n'
    else:
        print(cont)

AUTHOR_WID = ['10872443198', '10596344325', '10872476061', '10872406585', '10612799632']

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
        self.appid = 'wx532ecb3bdaaf92f9'
        self.headers = {
            'Host': 'xapi.weimob.com',
            'cloud-project-name': 'aidachildren',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Mi14 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160175 MMWEBSDK/20230701 MMWEBID/8701 MicroMessenger/8.0.40.2420(0x28002858) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'Content-Type': 'application/json',
            'X-WX-Token': self.token,
            'x-cms-sdk-request': '1.5.47',
            'xweb_xhr': '1',
            'x-biz-id': '1',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': f'https://servicewechat.com/{self.appid}/195/page-frame.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.baseUrl = 'https://xapi.weimob.com/api3/'
        self.use_power_max = False
        self.OpenId = ''
        self.json_data = {
            "appid": 'wx532ecb3bdaaf92f9',
            "basicInfo": {
                "vid": 6013753979957,
                "vidType": 2,
                "bosId": 4020112618957,
                "productId": 1,
                "productInstanceId": 3171023957,
                "productVersionId": "30044",
                "merchantId": 2000020692957,
                "tcode": "weimob",
                "cid": 176205957
            },
            "extendInfo": {
                "wxTemplateId": 7593,
                "analysis": [],
                "bosTemplateId": 1000001511,
                "childTemplateIds": [{
                    "customId": 90004,
                    "version": "crm@0.1.21"
                }, {
                    "customId": 90002,
                    "version": " ec@46.4"
                }, {
                    "customId": 90006,
                    "version": "hudong@0.0.208"
                }, {
                    "customId": 90008,
                    "version": "cms@0.0.439"
                }, {
                    "customId": 90060,
                    "version": "elearning@0.1.1"
                }],
                "quickdeliver": {
                    "enable": False
                },
                "youshu": {
                    "enable": False
                },
                "source": 1,
                "channelsource": 5,
                "refer": "cms-index",
                "mpScene": 1089
            },
            "queryParameter": None,
            "i18n": {
                "language": "zh",
                "timezone": "8"
            },
            "pid": "4020112618957",
            "storeId": "0",
            "bizType": 1
        }
        self.game_json_data = {}
        self.invite_wid = ''
        self.availablePoint = 0
        self.act_module = []

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
        Log(f'\n====== {act_name} ======',True)
        url = f"{self.baseUrl}passport/access/check"
        response = self.make_request(url, data=self.json_data)
        # print(response)
        if response.get('errmsg', False) == "success" and response.get('data', {}):
            Log(f'> {act_name}成功！✅',True)
            data = response.get('data', {})
            if data == {}: return False
            loginStatus = data.get('loginStatus', 0)
            if loginStatus:
                Log(f'> TOKEN有效！✅',True)
                return True
            else:
                Log(f'> TOKEN失效！❌')
                return False
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def queryUserInfo(self):
        global AUTHOR_WID
        act_name = '获取用户信息'
        Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        basicInfo = {
            "basicInfo": {
                "vid": 6013753979957,
                "bosId": 4020112618957,
                "productInstanceId": 3168798957,
                "tcode": "weimob",
                "cid": 176205957,
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
            Log(f'> {act_name}成功！✅',True)
            data = response.get('data', {})
            if data == {}: return False
            nickname = data.get('nickname', '')
            self.wid = data.get('wid', '')

            # print(f'取得的invite_wid:【{self.invite_wid}】')

            sourceObjectList = data.get('sourceObjectList', [])
            for app in sourceObjectList:
                sourceAppId = app['sourceAppId']
                if sourceAppId == self.appid:
                    self.OpenId = app['sourceOpenId']

            Log(f'> 用户名：【{nickname}】')
            Log(f'> OpenId：【{self.OpenId}】')
            Log(f'> wid：【{self.wid}】')
            self.queryCustomerInfo()

        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def queryCustomerInfo(self):
        act_name = '获取手机号'
        # Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        json_data['pid'] = '4020112618957'
        json_data['basicInfo']['productId'] = 146
        json_data['basicInfo']['productInstanceId'] = 3168798957
        json_data['basicInfo']['productVersionId'] = "12017"
        json_data['extendInfo']['refer'] = "onecrm-user-info"
        json_data['extendInfo']['mpScene'] = 1008
        json_data['storeId'] = '0'
        json_data.pop('bizType', None)
        url = f"{self.baseUrl}onecrm/user/center/usercenter/queryCustomerInfo"
        response = self.make_request(url, data=json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            # print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            userBaseInfos = data.get('userBaseInfos', [])
            phone = userBaseInfos[3].get('fieldValue', '')
            Log(f'> 手机号：【{phone}】')
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def signMainInfo(self):
        act_name = '获取签到状态'
        Log(f'\n====== {act_name} ======',True)
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
            Log(f'> 已连续签到：【{activityCumulativeSignDays}】天',True)
            Log(f'> 最长连续签到：【{maxActivityContinueSignDays}】天',True)
            Log(f'> 月累计签到：【{monthCumulativeSignDays}】天',True)
            Log(f'> 年累计签到：【{yearCumulativeSignDays}】天',True)
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

    def getSimpleAccountInfo(self,END = False):
        act_name = '获取积分详情'
        if not END:
            Log(f'\n====== {act_name} ======',True)
        else:
            Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        json_data['targetBasicInfo'] = {
            "productInstanceId": 3168798957
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
            if not END:
                self.availablePoint = availablePoint
                Log(f'> 当前积分：【{availablePoint}】',True)
            else:
                receive = availablePoint - self.availablePoint
                Log(f'> 执行后积分：【{availablePoint}】', True)
                Log(f'> 本次运行获得积分：【{receive}】', True)
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def queryPageInfo(self):
        act_name = '获取活动列表'
        Log(f'\n====== {act_name} ======')
        json_data = self.json_data.copy()
        json_data['bosId'] = 4020112618957
        json_data['requestType'] = 1
        json_data['pageSize'] = 10
        json_data['pageNum'] = 1
        json_data['exParams'] = {
            "pageId": 13906063
        }
        json_data['jsonSwitch'] = True
        json_data['pageId'] = 13906063
        json_data['$level'] = 1
        json_data.pop('bizType', None)
        url = f"{self.baseUrl}mp-decoration/web/page/queryPageInfo"
        response = self.make_request(url, data=json_data)
        # print(response)
        if response.get('errcode', False) == 0 and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            page_module_info_list = data.get("pageModuleInfoList", [])

            for index, module in enumerate(page_module_info_list):
                moduleJSON = module.get("moduleJSON", {})
                # print("找到的moduleJSON:", moduleJSON)
                content = moduleJSON.get("content", {})
                # print("找到的content:", content)
                items = content.get("items", [])
                # print("找到的items:", items)
                name = items[0].get("name")
                if name == None:continue
                if '活动页-列表' in name:
                    link = items[0].get("link",{})
                    link_name = link.get('name','').split('-')
                    act_name = link_name[2]
                    act_type = link_name[0]
                    miniUrl = link.get('miniUrl','')
                    pattern = r'activityId=(\d+)'
                    # 使用正则表达式查找匹配
                    activityId = re.search(pattern, miniUrl)
                    # 提取activityId
                    if activityId:
                        activity_id = activityId.group(1)
                        print(f'\n找到的活动：【{act_name}】 类型：【{act_type}】 ID：【{activity_id}】')
                        self.game_json_data = self.set_json_data(activity_id, act_type)
                        self.LightCard_index(act_name)
                        self.LightCard_index(act_name, True)
                        random_delay()
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def set_json_data(self, activityId, type):
        self.game_json_data = {}
        json_data = self.json_data.copy()
        common_data = {
            "pid": "4020112618957",
            "_transformBasicInfo": True,
            'storeId': "0",
            "source": 1,
            "$level": 1,
            "vidTypes": [2],
            "tcode": "weimob",
            "openid": self.OpenId
        }

        if type == '集卡':
            json_data.update({
                '_version': "2.9.2",
                'productVersionId': "16233",
                'appletVersion': 280,
                'productId': 165646,
                "productInstanceId": 3169913957,
                'operationSource': 4,
                "vid": 6013753979957,
                "bosId": 4020112618957,
                "cid": 176205957,
                "activityId": activityId,
                "vidType": 2,
                'v': "76e04a82cc9efce6e19336bfddab891410029744"
            })
            refer = "hd-card-home"
            mpScene = 1089
            productVersionId = 3169913957


        elif type == '消消乐':
            productVersionId = 3169906957
            json_data.update({
                '_version': "2.5.4",
                'templateKey': "elimination",
                'productVersionId': "12003",
                'productId': 214,
                "activityId": activityId,
            })

        elif type == '转盘':
            productVersionId = 3169919957
            json_data.update({
                '_version': "2.5.4",
                'templateKey': "bigwheel",
                'productVersionId': "12004",
                'productId': 222,
                "activityId": activityId,
            })


        if type in ['消消乐', '转盘']:
            mpScene = 1089
            refer = "hd-lego-index"
            json_data.update({
                'refer': "hd-lego-index",
                'productVersionId': json_data['productVersionId'],
                '_requrl': "/orchestration/mobile/activity/info",
                'templateId': "",
                'bussinessType': 1,
                'channel': 1,
                'channelType': 1,
                'openId': self.OpenId,
                'wid': self.wid,
                "playSourceCode": "lcode",
                'activityIdentity': 20
            })

        json_data.update(common_data)
        json_data['basicInfo']['productId'] = json_data['productId']
        json_data['merchantId'] = json_data['basicInfo']['merchantId']
        json_data['basicInfo']['productVersionId'] = productVersionId
        json_data['extendInfo']['refer'] = refer
        json_data['extendInfo']['mpScene'] = mpScene
        json_data.pop('bizType', None)

        return json_data

    def LightCard_index(self, actname,END=False):
        act_name = f'【{actname}】活动状态查询'
        if END:
            Log(f'\n====== {act_name} ======')
        else:
            Log(f'\n====== {act_name} ======',True)
        # print(json.dumps(json_data))

        url = f"{self.baseUrl}interactive/qianxi/amasscard/api/index"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            data = response.get('data', {})
            if data == {}: return False
            theme = data.get('theme', {})
            description = data.get('description', {})
            self.cards = theme.get('cards', [{}])

            startTime = data.get('startTime', "2024/05/23 10:00:00")
            endTime = data.get('endTime', "2024/05/23 10:00:00")
            act_start_time = datetime.strptime(startTime, "%Y/%m/%d %H:%M:%S")
            act_end_time = datetime.strptime(endTime, "%Y/%m/%d %H:%M:%S")
            current_time = datetime.now()


            is_within_range = act_start_time <= current_time <= act_end_time
            if is_within_range:
                if not END:
                    print(f'【{actname}】活动进行中....')
                    print(f'> {actname}查询成功！✅')
                remainCount = data.get('remainCount', 0)
                totalUse = data.get('totalUse', 0)
                Log(f'>> 剩余点亮：【{remainCount}】次',True)
                Log(f'>> 已点亮：【{totalUse}】次',True)
                theme = data.get('theme', {})
                cards = theme.get('cards', [{}])
                if END:
                    Log(f'>> 当前已收集：')
                    for card in cards:
                        cardName = card['cardName']
                        cardAmassedNum = card['cardAmassedNum']
                        Log(f'> 【{cardName}】卡【{cardAmassedNum}】张')
                    if current_time.date() == act_end_time.date() and current_time < act_end_time:
                        print("今日结束活动，进行自动兑换")
                        self.getPrizeList(True)
                    else:
                        self.getPrizeList()

                    # # 定义正则表达式
                    # pattern = r'（\d+）[^（]*（限[^）]+）'
                    #
                    # # 查找所有匹配项
                    # matches = re.findall(pattern, description)
                    # Log('兑换条件：')
                    # # 打印提取的兑奖条件
                    # for match in matches:
                    #     Log(match)

                else:
                    print(f'>> 当前已收集：')
                    for card in cards:
                        cardName = card['cardName']
                        cardAmassedNum = card['cardAmassedNum']
                        print(f'> 【{cardName}】卡【{cardAmassedNum}】张')
                    if remainCount > 0:
                        for i in range(remainCount):
                            print(f'>> 开始第【{i + 1}】次点亮')
                            self.lightCard()
                            random_delay(3, 5)
                    for wid in AUTHOR_WID:
                        if wid != str(self.wid):
                            self.invite_wid =wid
                            self.LightCard_hasHelped()
                        random_delay()
                return True
            else:
                print(f'【{act_name}】已结束')
                return False
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def LightCard_hasHelped(self):
        act_name = '查询是否助力好友'
        Log(f'\n====== {act_name} ======',True)
        # print(self.invite_wid)
        self.game_json_data['ownerWid'] = self.invite_wid
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}interactive/qianxi/amasscard/api/hasHelped"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            data = response.get('data', {})
            if data == {}: return False
            hasHelped = data.get('hasHelped', 0)
            Log(f'>> 已助力【{hasHelped}】次',True)
            if hasHelped == 0:
                self.LightCard_helpLightCard()
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def LightCard_helpLightCard(self):
        act_name = '助力'
        Log(f'====== {act_name} ======',True)
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}interactive/qianxi/amasscard/api/helpLightCard"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0":
            data = response.get('data', {})
            if data == {}: return False
            ownerNick = data.get('ownerNick', '')
            cardName = data.get('cardName', '')
            Log(f'>> 帮助【{ownerNick}】点亮【{cardName}】卡',True)

        if response.get('errcode', False) == "364" :
            print('好友助力已满')
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def lightCard(self):
        act_name = '点亮'
        Log(f'====== {act_name} ======',True)
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}interactive/qianxi/amasscard/api/lightCard"
        response = self.make_request(url, data=self.game_json_data)

        if response.get('errcode', False) == "0" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            cardId = data.get('cardId', 0)
            for card in self.cards:
                if card["cardId"] == cardId:
                    cardName =card["cardName"]
            Log(f'>> 获得：【{cardName}】卡',True)

        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    # 获取所需卡片的数量
    def get_card_amassed_num(self,card_id):
        for card in self.cards:
            if card["cardId"] == card_id:
                return card["cardAmassedNum"]
        return 0

    # 计算最多可以兑换多少次
    def calculate_max_exchanges(self,required_cards):
        min_exchanges = float('inf')
        for card_id, required_num in required_cards.items():
            available_num = self.get_card_amassed_num(card_id)
            max_exchanges_for_card = available_num // required_num
            if max_exchanges_for_card < min_exchanges:
                min_exchanges = max_exchanges_for_card
        return min_exchanges

    def getPrizeList(self,change=False):
        act_name = '获取可兑换列表'
        Log(f'\n====== {act_name} ======',True)
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}interactive/qianxi/amasscard/api/getPrizeList"
        response = self.make_request(url, data=self.game_json_data)

        if response.get('errcode', False) == "0" and response.get('data', {}):
            print(f'>>> {act_name}成功！✅')
            data = response.get('data', {})
            prizes =data.get('prizes', [{}])
            for prize in prizes:
                prizeId =prize.get('prizeId', '')
                prizeName =prize.get('prizeName', '')
                cardsNeeded =prize.get('cardsNeeded', '')
                Log(f'>> 当前可兑换：【{prizeName}】')
                Log(f'>> ID：【{prizeId}】')
                # 需要消耗的卡片ID
                cards_needed_list = cardsNeeded.split(",")

                # 将所需的卡片ID转换为字典，假设每种卡片只需要1张
                required_cards = {int(card_id): 1 for card_id in cards_needed_list}
                # 计算并输出结果
                max_exchanges = self.calculate_max_exchanges(required_cards)
                Log(f">> 最多可以兑换 {max_exchanges} 次")
                # self.consumerCards(prizeId)
                if change:
                    for i in range(max_exchanges+1):
                        print(f'开始第【{i+1}】次兑换')
                        self.consumerCards(prizeId)
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def consumerCards(self,prizeId):
        act_name = '兑换'
        Log(f'====== {act_name} ======',True)
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}interactive/qianxi/amasscard/api/consumerCards"
        self.game_json_data['prizeId'] = prizeId

        response = self.make_request(url, data=self.game_json_data)

        if response.get('errcode', False) == "0" and response.get('data', {}):
            if response.get('errmsg', '') == '操作成功':
                print(f'> {act_name}成功！✅')
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def LightCard_receiveBefore(self):
        act_name = '轮询卡片'
        Log(f'\n====== {act_name} ======',True)
        # print(json.dumps(json_data))
        cardId_li = ["30034868", "30034869", "30034870", "30034871", "30034872", "30034873"]
        for i in range(10872440286, 10872443198):
            self.xm_json_data['ownerWid'] = i
            for card in cardId_li:
                self.xm_json_data['cardId'] = card
                url = f"{self.baseUrl}interactive/qianxi/amasscard/api/receiveBefore"
                response = self.make_request(url, data=self.xm_json_data)
                # print(response)
                if response.get('errcode', False) == "0" and response.get('data', {}):
                    print(f'> {act_name}成功！✅')
                    data = response.get('data', {})
                    if data == {}: return False
                    ownerNick = data.get('ownerNick', 0)
                    cardName = data.get('cardName', 0)
                    isHaveReceive = data.get('isHaveReceive', 0)
                    if isHaveReceive:
                        print(f'>> 【{cardName}】卡,可领取用户：【{ownerNick}】，账号：【{i}】')
                    else:
                        print(f'账号【{i}】【{cardName}】卡不可领取')
                else:
                    print(f'> {act_name}失败❌：{response}')
                    return False
                time.sleep(2)
            time.sleep(2)

    def Check_act_info(self, actname):
        act_name = f'【{actname}】活动状态查询'
        Log(f'\n====== {act_name} ======',True)
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}orchestration/mobile/activity/info"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            activityTime = data.get('activityTime', {})
            start_time = activityTime[0]
            end_time = activityTime[1]
            print(f'活动结束时间：【{end_time}】')
            act_start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            act_end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            is_within_range = act_start_time <= current_time <= act_end_time
            if is_within_range:
                print(f'活动进行中....')
                return True
            else:
                Log(f'【{actname}】已结束')
                return False
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def game_chance(self, actname, act_type):
        act_name = f'【{actname}】抽奖机会查询'
        Log(f'\n====== {act_name} ======',True)
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}orchestration/mobile/prize/getRemainingAssets"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            assets = data.get('assets', {})
            chance = assets.get('chance', {})
            assetUseNum = chance.get('assetUseNum', 0)
            assetNum = chance.get('assetNum', 0)
            Log(f'>> 剩余次数：【{assetNum}】次',True)
            Log(f'>> 已玩：【{assetUseNum}】次',True)
            for i in range(assetNum):
                Log(f'>> 开始第：【{i + 1}】次游戏',True)
                if act_type == '转盘':
                    self.ZP_play(actname)
                elif act_type == '消消乐':
                    if '柠檬茶' in actname:
                        socre = random.randint(60, 100)
                    else:
                        socre = random.randint(30, 90)
                    self.XXL_game_play(actname,socre)
                random_delay(3, 5)
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def XXL_game_play(self, actname,socre):
        act_name = f'【{actname}】提交分数'
        Log(f'\n====== {act_name} ======',True)
        self.game_json_data['_requrl'] = "/orchestration/mobile/activity/draw/play"
        self.game_json_data['score'] = socre
        actid = self.game_json_data['activityId']
        str = f'{actid}elimination{socre}'
        scoreSign = hashlib.md5(str.encode()).hexdigest()
        self.game_json_data['scoreSign'] = scoreSign
        # print(json.dumps(json_data))
        url = f"{self.baseUrl}orchestration/mobile/activity/draw/play"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            prizes = data.get('prizes', [{}])
            name = prizes[0].get('name', '')
            Log(f'>> 获得：【{name}】',True)
        else:
            print(f'> {act_name}失败❌：{response}')
            return False

    def ZP_play(self, actname):
        act_name = f'【{actname}】抽奖'
        Log(f'\n====== {act_name} ======')
        self.game_json_data['_requrl'] = "/orchestration/mobile/activity/draw/play"
        url = f"{self.baseUrl}orchestration/mobile/activity/draw/play"
        response = self.make_request(url, data=self.game_json_data)
        # print(response)
        if response.get('errcode', False) == "0" and response.get('data', {}):
            print(f'> {act_name}成功！✅')
            data = response.get('data', {})
            if data == {}: return False
            prizes = data.get('prizes', [{}])
            name = prizes[0].get('name', '')
            Log(f'>> 获得：【{name}】')
        else:
            print(f'> {act_name}失败❌：{response}')
            return False




    def main(self):
        Log(f"\n开始执行第{self.index}个账号--------------->>>>>")
        if self.check_token():
            # random_delay(5,30)
            self.queryUserInfo()
            random_delay()
            self.getSimpleAccountInfo()
            random_delay()
            self.signMainInfo()
            random_delay()
            self.queryPageInfo()
            random_delay()
            # self.Play_game()

            random_delay()
            self.getSimpleAccountInfo(True)
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
    APP_NAME = '统一快乐星球小程序'
    ENV_NAME = 'TYKLXQ'
    CK_URL = 'xapi.weimob.com'
    CK_NAME = '请求头X-WX-Token'
    CK_EX = '8c8ff04e4f53c213faesxxxxxxxxxxxxxxxxxxxxxxxxxx'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ 功能：
      签到 转盘、集卡、消消乐游戏
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
✨ 推荐cron：5 9,18 * * *
✨✨✨ @Author CHERWIN✨✨✨
''')
    local_script_name = os.path.basename(__file__)
    local_version = '2024.06.02'
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
