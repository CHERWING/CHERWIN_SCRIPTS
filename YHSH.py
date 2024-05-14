'''
!/usr/bin/python3
-- coding: utf-8 --
-------------------------------
✨✨✨ @Author CHERWIN✨✨✨
cron "51 8,21 * * *" script-path=xxx.py,tag=匹配cron用
const $ = new Env('永辉生活')
'''
import hashlib
import json
import os
import random
import time
import urllib
from os import environ, path
from sys import exit
from urllib.parse import quote, urlparse, parse_qs

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

inviteCode = {}
GameCode=[]
PRIZEID = ''


class RUN:
    def __init__(self, info,index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        token = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID =None
        if len_split_info > 0 and "UID_" in last_info:
            self.send_UID = last_info
        self.index = index + 1
        self.s = requests.session()
        self.s.verify = False
        self.UA = 'Mozilla/5.0 (Linux; Android 11; Mi9 Pro 5G Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.162 Mobile Safari/537.36YhStore/9.6.0.14 cn.yonghui.hyd/2022946000 (client/phone; Android 30; Xiaomi/Mi9 Pro 5G)'
        self.headers = {
            'Host': 'api.yonghuivip.com',
            'Connection': 'keep-alive',
            'User-Agent': self.UA,
            'X-YH-Context': 'origin=h5&morse=1',
            'Accept': '*/*',
            'Origin': 'https://m.yonghuivip.com',
            'X-Requested-With': 'cn.yonghui.hyd',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://m.yonghuivip.com/',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        # 创建一个字典来存储参数
        data = {}
        # 解析第一个URL并提取参数
        parsed_url1 = urlparse(token)
        # print(parsed_url1)
        self.data_dict = parse_qs(parsed_url1.query)
        # print(self.data_dict)
        self.url_add = token.split('?')[1]
        # print(self.data_dict)
        self.fruit_is_ripe = False
        self.gameCode =''
        if self.data_dict.get('memberid') :
            self.memberId = self.data_dict.get('memberid',[])[0]
        else:
            self.memberId = self.data_dict.get('memberId', [])[0]
        if self.data_dict.get('shopid') :
            self.shopid = self.data_dict.get('shopid',[])[0]
        else:
            self.shopid = '9M7M'
            self.url_add =f'{self.url_add}&shopid={self.shopid}'
        print(self.shopid)
        self.gamecode_li = []
        self.canJoinTeam = True
        self.canhelp_coup = True
        self.teamCode = ''


    # 将参数转换为字典
    def create_dict_from_string(self, data_string):
        params = {}
        key_value_pairs = data_string.split(',')
        for pair in key_value_pairs:
            key, value = pair.split('=')
            params[key] = value
        return params

    # 发送请求函数
    def do_request(self, url, data={}, req_type='post', headers={}):
        if headers == {}:
            headers = self.headers
        try:
            if req_type.lower() == 'get':
                response = self.s.get(url, headers=headers)
            elif req_type.lower() == 'post':
                response = self.s.post(url, headers=headers, json=data)
            else:
                raise ValueError('Invalid req_type: %s' % req_type)
            res = response.json()
            return res
        except requests.exceptions.RequestException as e:
            print('Request failed:', e)
            return None
        except json.JSONDecodeError as e:
            print('JSON decoding failed:', e)
            return None

    def getCredit(self):
        Log(f'\n>>>>>>获取积分信息')
        headers = {
            'Accept': '*/*'
        }
        url = f'https://api.yonghuivip.com/web/coupon/credit/details/?page=0&{self.url_add}'
        response = self.do_request(url, req_type='get', headers=headers)
        # print(response)

        if 'code' in response and response.get('code','') == 0:
            credit = response.get('data')['credit']
            self.sign_count = response.get('data')['count']

            Log(f'>当前用户：{self.memberId}\n>当前积分：{credit}')
            # Log(f'>>>累计签到：{self.sign_count}天')
            return True
        elif response.get("message", "") == '登录状态已失效，请重新登录':
            if send:send('永辉生活账号失效通知', f'账号：{self.index} ID:{self.memberId}已失效，请重新抓包')
        else:
            Log(f'>获取积分信息失败')
            # print(response)
            return False

    def sign(self):
        Log(f'\n>>>>>>开始执行签到')
        headers = {
            'Accept': 'application/json'
        }

        data = {
            "memberId": self.memberId,
            "shopid": self.shopid,
            "missionid": "39"
        }
        url = f'https://api.yonghuivip.com/web/coupon/signreward/sign?{self.url_add}'
        response = self.do_request(url, headers=headers,data=data)
        # print(response)

        if 'code' in response and response.get('code') == 0:
            Log(f'>签到成功')
            Log(f'>累计签到：{int(self.sign_count) + 1}天')
            self.getCredit()
            return True
        elif '任务已完成，请勿重复点击' in response:
            Log(f'>今日已签到')
        else:
            Log(f'>签到失败，{response.get("message")}')
            return False

    def teamDetail(self):
        Log(f'\n>>>>>>开始获取组队详情')
        headers = {
            'Accept': 'application/json'
        }
        data = {
            "createTeamFlag": True,
            "shopId": self.shopid,
        }

        url = f'https://api.yonghuivip.com/web/coupon/credit/dividePoint/teamDetail?{self.url_add}'
        response = self.do_request(url, headers=headers,data=data)
        # print(response)
        if 'code' in response and response.get('code') == 0:
            data = response.get('data',{})
            if data != {}:
                self.teamCode = data.get('teamCode','')
                subTitle = data.get('subTitle','')
                print(f'战队ID：【{self.teamCode}】 状态：【{subTitle}】')
                new_data={
                    self.memberId:{
                        'teamCode':self.teamCode
                    }
                }
                inviteCode.update(new_data)
                print(inviteCode)
            else:
                print('未查询到战队,开始创建')
                self.creatTeam()
        else:
            print(f'>创建战队失败，{response.get("message")}')

    def creatTeam(self):
        Log(f'\n>>>>>>开始组队任务')
        headers = {
            'Accept': 'application/json'
        }
        data = {
            "shopId": self.shopid,
        }

        url = f'https://api.yonghuivip.com/web/coupon/credit/dividePoint/createTeam?{self.url_add}'
        response = self.do_request(url, headers=headers,data=data)
        # print(response)
        if 'code' in response and response.get('code') == 0:
            data = response.get('data',{})
            self.teamCode = data.get('teamCode', '')
            subTitle = data.get('subTitle', '')
            Log(f'创建战队成功,ID：【{self.teamCode}】 状态：【{subTitle}】')
            new_data = {
                self.memberId: {
                    'teamCode': self.teamCode
                }
            }
            inviteCode.update(new_data)
        else:
            print(f'>创建战队失败，{response.get("message")}')

    def joinAuthorTeam(self):
        print(f'>>>开始加入作者队伍')
        headers = {
            'Accept': 'application/json'
        }
        if len(AuthorCode) >0 :
            for code in AuthorCode:
                if not self.canJoinTeam:break
                data = {
                    "teamCode": code.get('teamCode'),
                    "shopId": self.shopid
                }
                url = f'https://api.yonghuivip.com/web/coupon/credit/dividePoint/joinTheParty?{self.url_add}'
                response = self.do_request(url, headers=headers, data=data)
                if 'code' in response and response.get('code') == 0:
                    print(f'加入战队成功')
                    break
                elif response.get('message') == '达到1天内组队上限':
                    self.canJoinTeam = False

    def joinTeam(self):
        Log(f'>>>开始本地账号组队')
        headers = {
            'Accept': 'application/json'
        }
        inviteCode_li = list(inviteCode.values())
        # print(inviteCode_li)
        for code in inviteCode_li:
            if not self.canJoinTeam:
                print('达到1天内组队上限')
                break
            data = {
                "teamCode": code.get('teamCode'),
                "shopId": self.shopid
            }
            url = f'https://api.yonghuivip.com/web/coupon/credit/dividePoint/joinTheParty?{self.url_add}'
            response = self.do_request(url, headers=headers, data=data)

            if 'code' in response and response.get('code') == 0:
                Log(f'组队成功')
                break
            elif response.get("message","") == '会员专享功能，请先登录':
                break
            elif response.get('message') == '达到1天内组队上限':
                self.canJoinTeam = False
            else:
                Log(f'>组队失败，{response.get("message")}')

    def farmInfo(self):
        headers = {
            'Accept': '*/*'
        }
        url = f'https://activity.yonghuivip.com/api/web/flow/farm/info?{self.url_add}'
        response = self.do_request(url, headers=headers, req_type='get')
        # print(response)

        if 'code' in response and response.get('code') == 0:
            self.parentId = response.get('data',[])['parentId']
            self.memberAmount = response.get('data',[])['memberAmount']
            self.ladderText = response.get('data',[]).get('ladderText','')
            Log(f'>>>当前水滴：{self.memberAmount}')
            Log(f'>>>当前水果进度：{self.ladderText}')
            if self.ladderText == '再浇水0%，果树就要成熟了':
                self.fruit_is_ripe = True
                inviteCode[self.memberId]['fruit_is_ripe'] = self.fruit_is_ripe

            return True
        else:
            Log(f'>>>获取果园信息失败\n{response}')
            return False

    def plantFruit_sign(self):
        Log(f'>>>开始果园签到')
        headers = {
            'Accept': 'application/json'
        }
        data = {
            "taskType": "sign",
            "activityCode": "HXNC-QG",
            "shopId": "",
            "channel": ""
        }
        url = f'https://activity.yonghuivip.com/api/web/flow/farm/doTask?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)
        # print(response)

        if 'code' in response and response.get('code') == 0:
            signText = response.get('data')['signText']
            Log(f'>>>{signText}')
            return True
        else:
            Log(f'>>>果园签到失败\n{response}')
            return False

    def plantFruit_getTaskList(self):
        print(f'>>>获取任务列表')
        headers = {
            'Accept': '*/*'
        }
        url = f'https://activity.yonghuivip.com/api/web/flow/farm/task/list?activityCode=HXNC-QG&&parentId={self.parentId}&{self.url_add}'
        response = self.do_request(url, headers=headers, req_type='get')
        # print(response)

        if 'code' in response and response.get('code') == 0:
            data = response.get('data')
            for i in data:
                subType = i['subType']
                title = i['title']
                finished = i['finished']
                self.taskId = i['taskId']
                self.rewardid = i.get('rewardId', '')
                # print(self.rewardid)
                if subType == 'activityPage' and finished != 1:
                    actionUrl = i['actionUrl']
                    # 解码URL
                    decoded_url = urllib.parse.unquote(actionUrl)
                    decoded_url = decoded_url.replace('pid=null', f'pid={self.parentId}')
                    # print(decoded_url)
                    parsed_url = urllib.parse.urlparse(decoded_url)
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    self.aid = query_params.get("aid", [None])[0]
                    self.taskid = query_params.get("taskid", [None])[0]
                    # print(self.aid)
                    # 提取aid后面的字符串
                    index = decoded_url.find("&aid=")
                    if index != -1:
                        toUrl = f'?aid={decoded_url[index + 5:]}'
                    else:
                        toUrl = ""
                    self.doFruitTask(title, toUrl)
                if self.rewardid != '':
                    print('检测到有可收取任务')
                    self.receive_water()
            return True
        else:
            print(response)
            return False

    def doFruitTask(self, title, toUrl):
        print(f'>>>开始做任务{title}')
        params = {"platform": "android",
                  "v": "9.6.0.14",
                  "channel": "2",
                  "distinctId": "",
                  "proportion": 2.75,
                  "screen": "1080.75*2340.25",
                  "pagesize": 6,
                  "networkType": "wifi",
                  "aid": self.aid,
                  "versionpro": "2",
                  "appType": "h5",
                  "model": "Mi9 Pro 5G",
                  "os": "android",
                  "osVersion": "android30",
                  "channelSub": "",
                  "brand": "Xiaomi",
                  "productLine": "YhStore",
                  "salesChannel": "",
                  "deviceid": "",
                  "sellerid": "7",
                  "shopid": "90B3",
                  "uid": "",
                  "access_token": "",
                  "showmultiseller": "",
                  "shopName": "",
                  "isOldEdition": False,
                  "userid": "",
                  "pageid": self.aid,
                  "pid": self.parentId,
                  "taskid": self.taskid,
                  "sceneValue": "4",
                  "memberId": ""
                  }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive",
            "Connection": "keep-alive"
        }
        url = f'https://api.yonghuivip.com/web/coupon/dailyreward/browse{toUrl}&{self.url_add}'
        response = self.do_request(url, headers=headers, data=params)
        # print(response)

        if 'code' in response and response.get('code') == 0:
            data = response.get('data')['title']
            Log(f'>{data}')
            return True
        else:
            return False

    def receive_inviteWater(self):
        headers = {
            'Accept': '*/*'
        }
        url = f'https://activity.yonghuivip.com/api/web/flow/farm/invitation/bubble?activityCode=HXNC-QG&{self.url_add}'
        # print(url)
        response =self.do_request(url, headers=headers,req_type='get')
        # print(response)
        if 'code' in response and response.get('code') == 0:
            data = response['data']['inviteWaterBubble']
            if data != []:
                Log(f'>>>开始领取邀请奖励')
                for task in data:
                    url = f'https://activity.yonghuivip.com/api/web/flow/farm/receiveWater?{self.url_add}'
                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    }
                    data = {"taskId": task['taskId'], "id": task['rewardId'], "activityCode": "HXNC-QG"}
                    response = requests.post(url, headers=headers, json=data,verify=False).json()
                    if 'code' in response and response.get('code') == 0:
                        receiveAmount = response['data']['receiveAmount']
                        print(f'>成功收取【{receiveAmount}】水滴')
                    else:
                        print(f'>收取失败，{response}')
            else:
                print('>没有可领取的邀请奖励')
        else:
            print(f'>领取邀请奖励失败，{response}')

    def receive_water(self,taskType=None):
        print(f'>>>开始领取奖励')
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "taskId": self.taskId,
            "id": self.rewardid,
            "activityCode": "HXNC-QG"}
        if taskType != None:
            data['taskType'] = "activityPage"
        url = f'https://activity.yonghuivip.com/api/web/flow/farm/receiveWater?{self.url_add}'
        # print(url)

        response =self.do_request(url, headers=headers, data=data)
        # response =requests.post(url, headers=headers, json=data)
        # if response:
        #     response = response.json()
        if 'code' in response and response.get('code') == 0:
            receiveAmount = response['data']['receiveAmount']
            print(f'>成功收取【{receiveAmount}】水滴')
        else:
            print(f'>收取失败，{response}')

    def watering(self):
        self.farmInfo()
        if int(self.memberAmount / 10) > 1 :
            print(f'>>>开始浇水')
            headers = {
                'Accept': 'application/json'
            }
            data = {"activityCode": "HXNC-QG", "shopId": "", "channel": "", "inviteTicket": "", "inviteShopId": ""}
            url = f'https://activity.yonghuivip.com/api/web/flow/farm/watering?{self.url_add}'
            for i in range(int(self.memberAmount / 10)):

                response = self.do_request(url, headers=headers, data=data)
                # print(response.text)
                if 'code' in response and response.get('code') == 0:
                    print(f'>第{i + 1}次浇水成功')
                elif response.get('message') == '果树已经成熟啦，快去领取奖励吧':
                    print(f'>果树已经成熟啦')
                    self.fruit_is_ripe = True

                    inviteCode[self.memberId]['fruit_is_ripe'] = self.fruit_is_ripe

                    break
                else:
                    print(f'>浇水失败,{response}')
        else:
            print('>水滴不足，停止浇水')

    def get_inviteTicket(self):
        print(f'>>>开始获取果园邀请码')
        headers = {
            'Accept': 'application/json'
        }
        data = {"inviteAction": "802"}
        url = f'https://activity.yonghuivip.com/api/web/flow/farm/invite/ticket?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)
        # print(response)
        if 'code' in response and response.get('code','') == 0:
            self.inviteTicket = response.get('data')
            print(f'果园邀请码：{self.inviteTicket}')
            inviteCode[self.memberId]['inviteCode']=self.inviteTicket
            inviteCode[self.memberId]['shopId']=self.shopid

        else:
            print(f'>获取果园邀请码失败,{response}')

    def helpAuthor(self):
        print(f'>>>开始助力作者')
        headers = {
            'Accept': 'application/json'
        }
        for code in AuthorCode:
            if code.get('memberId', '') == self.memberId: continue
            if code.get('fruit_is_ripe',False):break
            data={
                "activityCode":"HXNC-QG",
                  "shopId":self.shopid,
                  "channel":"512",
                  "inviteTicket":code.get('inviteCode',''),"inviteAction":"watering","inviteShopId":code.get('shopId','')
                  }
            url = f'https://activity.yonghuivip.com/api/web/flow/farm/watering?inviteTicket={code}&{self.url_add}'
            response = self.do_request(url, headers=headers,data=data)
            # print(response)
            if 'code' in response and response.get('code') == 0:
                Log(f'>助力作者成功')
                break
            elif response.get("message","") == '会员专享功能，请先登录':
                break
            else:
                pass
                # Log(f'>助力作者失败,{response.get("message","")}')

    def helpOther(self):
        Log(f'>>>开始本地账号互助')
        headers = {
             'Accept': 'application/json'
        }
        inviteCode_li = list(inviteCode.values())
        # print(inviteCode_li)
        for code in inviteCode_li:
            if code.get('memberId', '') == self.memberId:continue
            if code.get('fruit_is_ripe', False): break
            data = {"activityCode": "HXNC-QG",
                    "shopId": self.shopid,
                    "channel": "512",
                    "inviteTicket": code.get('inviteCode', ''), "inviteAction": "watering",
                    "inviteShopId": code.get('shopId', '')
                    }
            url = f'https://activity.yonghuivip.com/api/web/flow/farm/watering?inviteTicket={code}&{self.url_add}'
            response = self.do_request(url, headers=headers, data=data)
            # print(response.text)
            if 'code' in response and response.get('code') == 0:
                Log(f'>助力成功')
            elif response.get("message","") == '会员专享功能，请先登录':
                break
            else:
                Log(f'>助力失败,{response.get("message","")}')

    ######################成长值任务
    def get_GrowthValue(self):
        Log(f'\n>>>>>>开始成长任务')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "businessCode": "membershipSystem"
        }
        url = f'https://api.yonghuivip.com/web/member/level/benefit/queryMemberGrowthValueProcess?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)

        if 'code' in response and response.get('code') == 0:
            # print(response['data'])
            data = response.get('data',[])
            self.levelNeedGrowthValues = data.get('levelNeedGrowthValues',[])
            if self.levelNeedGrowthValues != None:
                for li in self.levelNeedGrowthValues:
                    isCurrentLevel = li.get('isCurrentLevel','')
                    # print(isCurrentLevel)
                    if isCurrentLevel == True:
                        self.levelName = li.get('levelName', '')
                        # print(self.levelName)
                        currentTotalGrowthValue = li.get('currentTotalGrowthValue', '')
                        nextLevelMinGrowthValue = li.get('nextLevelMinGrowthValue', '')
                        count = int(nextLevelMinGrowthValue)-int(currentTotalGrowthValue)
                        print(f'当前等级:【{self.levelName}】 积分：【{currentTotalGrowthValue}】 升级需要【{count}】')
                        break
            else:
                print('--------------')

        else:
            Log(f'>获取失败，{response}')

    def get_GrowthtaskList(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "businessCode": "membershipSystem",
            "shopId": self.shopid,
            "isOpenPublishNotice": True
        }
        url = f'https://api.yonghuivip.com/web/member/task/listTasks?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)

        if 'code' in response and response.get('code') == 0:
            # print(response['data'])
            data = response.get('data',[])
            self.taskCode = data.get('taskCode','')
            # Log(f'>获取到当前签到任务ID：【{self.taskID}】 编码：【{self.taskCode}】')
            if data.get("subTasks",[]) != None:
                for li in data.get("subTasks",[]):
                    self.taskID = li.get('taskId','')
                    self.taskTitle = li.get('taskTitle','')
                    self.doSignTask()
            else:
                print('>>未发现成长值任务')

        else:
            Log(f'>获取失败，{response}')

    ######################签到任务
    def get_taskList(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "shopId": self.shopid
        }
        url = f'https://api.yonghuivip.com/web/coupon/credit/task/queryTaskInfo?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)

        if 'code' in response and response.get('code') == 0:
            # print(response['data'])
            data = response.get('data',[])
            if data:
                self.taskStatus = data.get('taskStatus','')
                self.taskID = data.get('taskId','')
                self.taskTitle = data.get('taskTitle','')
                if self.taskID and self.taskStatus ==0:
                    self.doTask()
            else:
                print('>>未发现任务')

        else:
            Log(f'>获取失败，{response}')

    def doTask(self):
        Log(f'>>>执行{self.taskTitle}')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "taskId": self.taskID,
            "shopId": self.shopid
        }
        url = f'https://api.yonghuivip.com/web/coupon/credit/task/completeTask?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)

        if 'code' in response and response.get('code') == 0:
            data = response['data']
            success = data['success']
            sendNum = data['sendNum']
            if success:
                Log(f'>获取到【{sendNum}】积分')

        elif response.get('message','')=='任务已完成，请勿重复点击':
            Log(f'>今日已签到')
        else:

            Log(f'>签到失败，{response}')

    def doSignTask(self):
        Log(f'>>>执行{self.taskTitle}')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "taskId": self.taskID,
            "shopId": self.shopid,
            "taskCode": self.taskCode
        }
        url = f'https://api.yonghuivip.com/web/member/task/doTask?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)

        if 'code' in response and response.get('code') == 0:
            recive_data = response['data']
            Log(f'>签到成功获取到【{recive_data}】成长值')
        elif response.get('message','')=='任务已完成，请勿重复点击':
            Log(f'>今日已签到')
        else:

            Log(f'>签到失败，{response}')

    #########助力券任务
    #获取助力券列表
    def listBoostCouponByPage(self):
        global PRIZEID
        print(f'>>>>>>开始获取助力券列表>>>>>>')
        print('默认发起普通用户助力券')
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "current": 1,
            "size": 20
        }
        url = f'https://api.yonghuivip.com/web/marketing/boostcoupon/listBoostCouponByPage?{self.url_add}'

        response = self.do_request(url, headers=headers, data=data)
        # print(response)
        if 'code' in response and response.get('code') == 0:
            # print(response)

            coupList = response.get('data')['records']
            for li in coupList:
                #助力券ID
                self.prizeId = li['prizeGameDTO']['prizeId']
                self.needBoostNum = li['prizeGameDTO']['needBoostNum']
                self.remainBoostNum = li['prizeGameDTO']['remainBoostNum']
                self.gameCode = li['prizeGameDTO']['gameCode']

                # boosterType  2 新人助力  1普通助力
                self.boosterType = li['prizeGameDTO']['boosterType']
                self.boosterType ="新人" if self.boosterType  == 2 else "普通用户"
                self.amount = li['boostCouponVO']['amount']
                self.coupName = li['boostCouponVO']['name']
                # 剩余张数
                self.availableCount = li['boostCouponVO']['availableCount']
                # 使用限制
                self.couponDescription = li['boostCouponVO']['couponDescription']
                self.applicationScope = li['boostCouponVO']['applicationScope']
                self.canApply = li['boostCouponVO']['canApply']
                copuname = f'{self.amount}元{self.coupName}'
                # if COPU_NAME == copuname:
                #     PRIZEID = self.prizeId
                self.canApply = "可发起" if self.canApply != -1 else "不可发起"
                if self.canApply != -1 and self.boosterType == '普通用户':
                    self.getGameCode()
                if self.gameCode:
                    gamecode_data = {
                        'name': f'{self.amount}元{self.coupName}',
                        'prizeId': self.prizeId,
                        'gameCode': self.gameCode
                    }
                    self.gamecode_li.append(gamecode_data)
                    if self.index == 1:
                        GameCode.append(gamecode_data)
                        print(f'-----【{self.amount}元{self.coupName}】----')
                        print(f'prizeId：【{self.prizeId}】\n需要【{self.needBoostNum}】个[{self.boosterType}]助力，仍需：【{self.remainBoostNum}】 {self.canApply}】 \n使用限制：【{self.couponDescription} {self.applicationScope}】\ngameCode:【{self.gameCode}】')

            # print('第一个账号gamecodeli：',GameCode)
            # print(self.gamecode_li)
            print(f'>>>>>>获取助力券列表结束>>>>>>')

    #根据prizeId获取gameCode
    def getGameCode(self):
        global GameCode
        # print(f'>>开始获取prizeID：【{self.prizeId}】gameCode')
        headers = {
            "Accept": "*/*"
        }

        url = f'https://api.yonghuivip.com/web/marketing/boostcoupon/getGameCode?prizeId={self.prizeId}&gameCode=&{self.url_add}'

        response = self.do_request(url, headers=headers, req_type='get')
        # print(response)
        if 'code' in response and response.get('code') == 0:
            # print(response)
            self.gameCode = response.get('data')
            #保存到json
            if self.gameCode:
                gamecode_data ={
                    'name':f'{self.amount}元{self.coupName}',
                    'prizeId':self.prizeId,
                    'gameCode':self.gameCode
                }
                if self.index == 1:
                    GameCode.append(gamecode_data)
                print(f'>>获取到gameCode:【{self.gameCode}】')
            else:
                print('>>未获取到gameCode')
        elif response.get('message','') =='您今日发起活动次数已达上限，请明日再来':
            self.canDoApply = False
        else:
            print(response.get('message'))

    #助力助力券
    def Boostcoupon(self,gameCodeLi=None):
        global AuthorCode

        print(f'>>>开始领券助力')
        # print('GameCode:',GameCode)
        # print('AuthorCode:',inviteCode)
        if gameCodeLi==None:
            print('>>第一个账号开始为作者助力')
            for codeli in AuthorCode:
                if not self.canhelp_coup:
                    print(f'>>>助力次数上限')
                    return
                # print(codeli)
                gameCode = codeli.get('gameCode', [{}])
                memberId = codeli.get('memberId', '')
                if memberId == self.memberId: continue
                for Codes in gameCode:
                    code = Codes.get('gameCode', '')
                    self.copuHelp(code)
        else:
            code_list = list(inviteCode.values())
            print('>>开始为第一个账号助力')
            if not self.canhelp_coup:
                print(f'>>>助力次数上限')
                return
            gameCode = code_list[0].get('gameCode', [{}])
            for Codes in gameCode:
                code = Codes.get('gameCode', '')
                self.copuHelp(code)
        #     for codeli in GameCode:
        #         if not self.canhelp_coup: return
        #         print(codeli)
        #         code = codeli.get('gameCode', [{}])
        #         self.copuHelp(code)


    def copuHelp(self,code):
        headers = {
            "Accept": "*/*"
        }
        url = f'https://api.yonghuivip.com/web/marketing/boostcoupon/boost?gameCode={code}&{self.url_add}'
        response = self.do_request(url, headers=headers, req_type='get')
        if 'code' in response and response.get('code') == 0:
            # print(response)
            Log(f'>{code},助力成功！')
            return True
        elif response.get('message') == '每日助力次数超过限制':
            self.canhelp_coup = False
            return False
        else:
            # print(f">{code},助力失败{response.get('message')}！")
            return False


    #########试用任务
    def tryList(self,levelName=None):
        if not levelName:
            self.levelName = '黄金'
        if self.levelName == '普通':
            Log(f'当前等级【{self.levelName}】不达标，停止试用申请')
        else:
            Log(f'>>>开始试用申请')
            headers = {
                'Accept': '*/*'
            }
            url = f'https://api.yonghuivip.com/web/marketing/free/trial/issue/prize/landing/page?{self.url_add}'
            response = self.do_request(url, headers=headers, req_type='get')

            if 'code' in response and response.get('code') == 0:
                # print(response)
                if response['data']['tip'] == '本期活动报名已结束，敬请期待下期活动':
                    Log('>>本期活动报名已结束，敬请期待下期活动')
                    return False
                goodsList = response['data']['currTab']['landingPagePrizeVOList']
                for liId in goodsList:
                    buttonStateName = liId['buttonStateName']
                    self.skuTitle = liId['skuTitle']
                    self.prizeId = liId['prizeId']
                    if buttonStateName != '已报名':
                        print(f'>>产品：【{self.skuTitle}】 ID：【{self.prizeId}】【可申请】')
                        self.doTry()
                    else:
                        print(f'>>产品：【{self.skuTitle}】【已申请,跳过】')

            else:
                Log(f'>获取失败，{response}')

    def doTry(self):
        print(f'>>开始申请【{self.skuTitle}】')
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "prizeId": self.prizeId
        }
        url = f'https://api.yonghuivip.com/web/marketing/free/trial/sign/up/fire?{self.url_add}'
        response = self.do_request(url, headers=headers, data=data)

        if 'code' in response and response.get('code') == 0:
            # print(response)
            Log(f'>{self.skuTitle},申请成功！')
        else:
            Log(f'>{self.skuTitle},申请失败，{response}')

    def get_WinTryList(self):
        print(f'>>>>>>获取已中奖列表>>>>>>')
        headers = {
            'Accept': '*/*',
        }
        url = f'https://api.yonghuivip.com/web/marketing/free/trial/issue/participated/detail?fromType=1&pageNum=1&{self.url_add}'
        response = self.do_request(url, headers=headers,req_type='get')
        if 'code' in response and response.get('code') == 0:
            data = response.get('data')
            participatedVOList = data.get('participatedVOList')
            for li in participatedVOList:
                skuTitle = li['skuTitle']
                skuPrice = li['skuPrice']
                status = li['status']
                #1已报名 2待领券 3未中奖 4待兑换
                if status == 2:
                    Log(f'商品：【{skuTitle}】 价格：【{skuPrice}】 【待领券】')
                elif status == 4:
                    Log(f'商品：【{skuTitle}】 价格：【{skuPrice}】 【待兑换】')
                elif status == 6:
                    print(f'商品：【{skuTitle}】 价格：【{skuPrice}】 【已过期】')
                elif status == 5:
                    print(f'商品：【{skuTitle}】 价格：【{skuPrice}】 【已兑换】')
                else:
                    print(f'商品：【{skuTitle}】 价格：【{skuPrice}】')
            # print(response)
        else:
            print(f'>申请失败，{response}')


    def sixYears_getTask(self):
        print(f'>>开始获取6周年任务列表')
        headers = {
            'Accept': '*/*'
        }

        url = f'https://api.yonghuivip.com/web/marketing/quick/task/loadTask?activityId=3572&{self.url_add}'
        response = self.do_request(url, headers=headers, req_type='get')

        if 'code' in response and response.get('code') == 0:
            data = response.get('data',[{}])
            for task in data:
                taskId = task.get('taskId','')
                taskType = task.get('taskType','')
                taskStatus = task.get('taskStatus','')
                taskTitle = task.get('taskTitle','')
                if taskStatus == 0:
                    print(f'任务[{taskTitle}]已完成')
                    continue
                self.sixYears_doTask(taskId,taskType,taskTitle)
        else:
            Log(f'获取6周年任务列表，{response}')

    def sixYears_doTask(self,taskId,taskType,taskTitle):
        print(f'>>开始执行{taskTitle}任务')
        headers= self.headers.copy()

        headers_new = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        headers.update(headers_new)

        data = {
            "activityId": '3572',
            "activityCode": "FJ-MD-05",
            "taskId": taskId,
            "taskType": taskType
        }

        url = f'https://api.yonghuivip.com/web/marketing/quick/task/doTask?{self.url_add}'
        response = self.do_request(url, headers=headers,data=data)

        if 'code' in response and response.get('code') == 0:
            data = response.get('data',{})
            count = data.get('count',0)
            print(f'获得【{count}】次抽奖机会')
        else:
            Log(f'>执行{taskTitle}任务失败，{response}')

    def help_fun(self):
        print(f"\n>>>>>>>>>>开始互助<<<<<<<<<<")
        one_msg = ''
        if not self.getCredit():
            return False
        # # pass
        # Log(f"\n********账号【{self.index}】果园互助********")
        # self.helpAuthor()
        # self.helpOther()
        Log(f"\n********账号【{self.index}】组队互助********")
        self.joinAuthorTeam()
        self.joinTeam()
        self.sendMsg(True)
        return True
    def main(self):
        global one_msg
        wait_time = random.randint(1000, 3000) / 1000.0  # 转换为秒
        one_msg = ''
        Log(f"\n---------开始执行第{self.index}个账号>>>>>")
        if not self.getCredit():
            return False
        self.sign()
        self.teamDetail()
        self.get_taskList()
        self.creatTeam()
        self.get_GrowthValue()
        self.get_GrowthtaskList()
        Log(f'\n>>>>>>开始试用任务')
        self.get_WinTryList()
        self.tryList()
        Log('\n>>>>>>开始助力券任务')
        self.listBoostCouponByPage()
        if self.index == 1:
            self.Boostcoupon()
        else:
            self.Boostcoupon(GameCode)
        self.sixYears_getTask()
        new_data = {
            self.memberId:
                {
                 'memberId': self.memberId,
                 'gameCode': self.gamecode_li,
                 'fruit_is_ripe': self.fruit_is_ripe,
                 # 'inviteCode': self.inviteTicket,
                 'teamCode': self.teamCode,
                 'shopId': self.shopid
                 }
        }
        # print(new_data)
        inviteCode.update(new_data)
        # print(f'当前inviteCode：\n{inviteCode}')
        CHERWIN_TOOLS.SAVE_INVITE_CODE("INVITE_CODE/YHSH_INVITE_CODE.json", new_data)
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
    APP_NAME='永辉生活'
    ENV_NAME = 'YHSH'
    CK_NAME = 'url'
    print(f'''
✨✨✨ {APP_NAME}脚本✨✨✨
✨ 功能：
      积分签到
      种树
      种树任务
      成长值任务
      试用申请
      果园互助
      组队互助
      助力券助力
✨ 抓包步骤：
      打开永辉生活APP或小程序
      点击“我的”
      打开抓包工具
      点击“积分签到”，找到带以下参数的链接复制：
        -deviceid
        -jysessionid
        -shopid
        -memberid 
        -access_token
        -sign
链接示例：https://api.yonghuivip.com/web/coupon/credit/coupon/getcreditcouponpageinfo/v2?xxxxx
✨ ✨✨wxpusher一对一推送功能，
  ✨需要定义变量export WXPUSHER=wxpusher的app_token，不设置则不启用wxpusher一对一推送
  ✨需要在{ENV_NAME}变量最后添加@wxpusher的UID
✨ 设置青龙变量：
export {ENV_NAME}='{CK_NAME}'多账号#分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ 默认每个账号随机助力作者一次，其余互助，后续考虑加上邀请池
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
                print(
                    '脚本依赖下载失败，请到https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/CHERWIN_TOOLS.py下载最新版本依赖')
                exit()
    print(TIPS)
    token = ''
    token = ENV if ENV else token
    if not token:
        print(f"未填写{ENV_NAME}变量\n青龙可在环境变量设置 {ENV_NAME} 或者在本脚本文件上方将{CK_NAME}填入token =''")
        exit()
    tokens = token.split('#')
    # print(tokens)
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).main()
            if not run_result:continue
        # for index, infos in enumerate(tokens):
        #     RUN(infos, index).help_fun()
        #     if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)

