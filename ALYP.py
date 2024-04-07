'''
阿里云盘签到
功能：自动签到，领取签到奖品，支持多账号（使用#分割token），支持青龙
到这里获取token：http://qr.ziyuand.cn/

cron： 1 1,12 1 * * *
by：cherwin
'''
import base64
import hashlib
import json
import os
import random
import time

import requests
from os import environ, path
from sys import exit
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def load_send():
    global send, mg
    cur_path = path.abspath(path.dirname(__file__))
    if path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            print("加载通知服务成功！")
        except:
            send = False
            print("加载通知服务失败~")
    else:
        send = False
        print("加载通知服务失败~")


load_send()
send_msg = ''


def Log(cont):
    global send_msg
    print(cont)
    send_msg += f'{cont}\n'


REFRESHTOEKN_PATH = "ALYP_REFRESH_TOEKN.json"


def saveRefreeshToken(data):
    # 保存数据到文件
    if os.path.isfile(REFRESHTOEKN_PATH):
        with open(REFRESHTOEKN_PATH, 'r') as file:
            try:
                refresh_tokens = json.load(file)
            except:
                refresh_tokens = {}
    else:
        refresh_tokens = {}
    refresh_tokens.update(data)
    with open(REFRESHTOEKN_PATH, 'w') as file:
        json.dump(refresh_tokens, file)


def loadRefreshTokens():
    try:
        with open(REFRESHTOEKN_PATH, 'r') as file:
            file_content = file.read()
            # print(file_content)
            if file_content:
                refresh_tokens = json.loads(file_content)
            else:
                refresh_tokens = ''
    except FileNotFoundError:
        refresh_tokens = ''

    return refresh_tokens


def is_last_day_of_month():
    today = datetime.date.today()
    next_month = today.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)
    return today == last_day


class AliDrive_CheckIn:
    def __init__(self, refresh_token, ali_reward):
        self.userAgent = "Mozilla/5.0 (Linux; U; Android 11; zh-CN; Mi9 Pro 5G Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 UWS/3.22.2.28 Mobile Safari/537.36 UCBS/3.22.2.28_210922181100 ChannelId(0) NebulaSDK/1.8.100112 Nebula InsidePlus/10.2.3 AliApp(AYSD/4.9.1)  AlipayDefined(nt:WIFI,ws:393|0|2.75)zh-CN useStatusBar/true isConcaveScreen/trueAriver/1.0.0"
        self.refresh_token = refresh_token
        self.ali_reward = ali_reward
        self.file_id = ''
        self.headers = {
            "Content-Type": "application/json",
            "charset": "utf-8",
            "User-Agent": self.userAgent
        }

    def getToken(self):
        url = 'https://auth.aliyundrive.com/v2/account/token'
        body = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = s.post(url, headers=self.headers, json=body, verify=False)
        try:
            resp = response.json()
            if resp.get('code') == 'InvalidParameter.RefreshToken':
                Log('\nRefreshToken 有误请检查！(可能token失效了，到这里获取http://qr.ziyuand.cn)\n')
                return False
            else:
                self.aliYunPanToken = f'Bearer {resp.get("access_token", "")}'
                self.access_token = resp.get("access_token", "")
                self.aliYunPanRefreshToken = resp.get("refresh_token", "")
                print(f'refresh_token:{self.aliYunPanRefreshToken}')
                self.user_id = resp.get("user_id", "")
                self.headers['Authorization'] = self.aliYunPanToken
                Log(f">账号ID：【{self.user_id}】\n>获取token成功")
                self.getUserInfo()
                # # 保存数据到文件
                # saveData = {self.user_id: self.aliYunPanRefreshToken}
                # saveRefreeshToken(saveData)
                return True
        except:
            print(response.text)
            return False

    def getUserInfo(self):
        url = 'https://api.aliyundrive.com/adrive/v2/user/get'
        body = {
            "addition_data": {},
            "user_id": self.user_id
        }
        response = s.post(url, headers=self.headers, json=body, verify=False)
        try:
            resp = response.json()
            self.phone = resp.get("phone", "")
            self.default_drive_id = resp.get("default_drive_id", "")
            if self.phone !='':
                self.phone = self.phone[:3] + '*' * 4 + self.phone[7:]
                Log(f">手机号：【{self.phone}】")
                # 保存数据到文件
                saveData = {self.phone: self.aliYunPanRefreshToken}
                saveRefreeshToken(saveData)
                return True
        except:
            print(response.text)

    def get_sign_in_list(self):
        Log(f'>>>>开始签到任务')
        sign_url = 'https://member.aliyundrive.com/v2/activity/sign_in_list?_rx-s=mobile}'
        sign_body = {'isReward': False}
        sign_res = s.post(sign_url, headers=self.headers, json=sign_body, verify=False)

        try:
            sign_resp = sign_res.json()
            result = sign_resp.get('result', {})
            self.sign_in_count = result.get('signInCount', 0)
            is_sign_in = result.get('isSignIn', False)

            if is_sign_in:
                Log(f'>签到成功！\n>已累计签到{self.sign_in_count}天！')
            else:
                Log(f'>今日已签到！\n>已累计签到{self.sign_in_count}天！')

            sign_in_infos = result.get('signInInfos', [])
            rewards_list = sign_in_infos[self.sign_in_count - 1].get('rewards', [])
            status = rewards_list[1].get('status', '')
            # print(status)
            remind = rewards_list[1].get('remind', '')
            complete_status_list = ["verification", "finished", "end"]

            if status not in complete_status_list:
                self.handle_task(remind)
            else:
                print(f'>任务【{remind}】已完成')
        except Exception as e:
            print(f"获取签到列表失败：{e}")

    def handle_task(self, task_name):
        Log(f'>>开始【{task_name}】任务')
        if task_name == '接3次好运瓶即可领取奖励':
            self.bottle_fish()
        elif task_name == '订阅官方账号「阿里盘盘酱」即可领取奖励':
            self.follow_user()
        elif task_name == '上传10个文件到备份盘即可领取奖励':
            self.fileName = '签到任务文件_喜欢可以赞赏一波_谢谢.jpg'
            self.upload_files_to_drive(10)
        elif task_name == '开启手机自动备份并持续至少一小时':
            self.update_device_extras()
        elif task_name == '备份10张照片到相册即可领取奖励':
            self.fileName = '签到任务文件_喜欢可以赞赏一波_谢谢.jpg'
            self.upload_files_to_drive(10, 'alibum')
        elif task_name == '播放1个视频30秒即可领取奖励':
            # pass
            self.get_videoList()
        elif task_name == '接好运瓶并转存任意1个文件':
            self.get_bottleShareId()
        else:
            Log(f'>【{task_name}】-暂不支持此任务，请手动完成！')
        time.sleep(2)

    ###############################文件上传任务开始###############################

    def upload_files_to_drive(self, num_files, drive_type='Default'):
        for i in range(num_files):
            self.get_user_drive_info(drive_type)
            time.sleep(1)

    def get_user_drive_info(self, drive_type):
        url = "https://api.aliyundrive.com/v2/drive/list_my_drives"
        response = s.post(url, headers=self.headers, json={})
        try:
            if response.status_code == 200:
                data = response.json()
                # print(data)
                drive_list = data.get("items", [])
                if drive_list != []:
                    index = None
                    for i, item in enumerate(drive_list):
                        if drive_type == 'alibum':
                            if item['drive_name'] == 'alibum':
                                index = i
                                break
                        else:
                            if item['drive_name'] == 'Default' and item['category'] == 'backup':
                                index = i
                                break
                    self.drive_id = drive_list[index]['drive_id']
                    print(f'当前drive ID:{self.drive_id}')
                if self.drive_id:
                    self.file_create(drive_type,True)
            else:
                print("获取用户云盘信息API请求失败")
        except Exception as e:
            print(f"获取用户云盘信息失败：{e}")

    def get_file_size(self, file_path):
        try:
            # 获取文件大小
            print(f'文件大小{os.path.getsize(file_path)}')
            return os.path.getsize(file_path)
        except OSError:
            return 0

    def download_file(self, url,filename):
        response = requests.get(url,verify=False)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'{filename} 下载签到视频文件完成！')
            return True
        else:
            print(f'下载签到视频文件失败：{response.status_code}')
            return False

    def get_file_pre_hash(self, file_path,HashType='content_hash'):
        if HashType =='pre_hash':
            with open(file_path, 'rb') as f:
                sha1 = hashlib.sha1()
                data = f.read(1024)  # 只读取前 1KB 的数据
                sha1.update(data)
            print(f'当前文件前1K hash值：{sha1.hexdigest().upper()}')
            return sha1.hexdigest().upper()
        else:
            with open(file_path, 'rb') as f:
                sha1 = hashlib.sha1()
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    sha1.update(data)
            print(f'当前文件完整hash值：{sha1.hexdigest().upper()}')
            return sha1.hexdigest().upper()


    def get_signTaskFileId(self):
        url = "https://api.aliyundrive.com/v2/file/search"
        json_data = {
            'drive_id': self.default_drive_id,
            'order_by': 'name ASC',
            'query': f'name = "{self.fileName}"',
        }
        response = s.post(url, headers=self.headers, json=json_data)
        data = response.json()

        try:
            if response.status_code == 200:
                fileList = data.get("items", [])
                if fileList:
                    print(f'找到签到任务文件id：{fileList[0]["file_id"]}')
                    print(f'执行覆盖上传')
                    self.file_id = fileList[0]['file_id']
                    return fileList[0]['file_id']
                else:
                    print(f'未找到签到任务文件')
            else:
                print("搜索文件API请求失败")
        except Exception as e:
            print(f"获取签到任务文件ID失败：{e}")

        return ''

    def file_create(self, type,needPreHash=True):
        self.filePath = f'./{self.fileName}'
        self.size = self.get_file_size(self.filePath)
        if self.size == 0:
            print('本地未发现签到视频文件，开始远程下载')
            if self.download_file(f'{server_base_url}签到任务文件_视频.mp4',self.fileName) and self.download_file(f'{server_base_url}签到任务文件_喜欢可以赞赏一波_谢谢.jpg', self.fileName):
                self.size = self.get_file_size(self.filePath)
        json_data = {
            'name': self.fileName,
            'type': 'file',
            'parent_file_id': 'root',
            'drive_id': self.drive_id,
            'check_name_mode': 'ignore',
            'size': self.size,
            "content_hash_name": "sha1",
        }
        if needPreHash:
            pre_hash = self.get_file_pre_hash(self.filePath,'pre_hash')
            json_data['pre_hash']=pre_hash
        else:
            content_hash = self.get_file_pre_hash(self.filePath,'content_hash')
            json_data['content_hash'] = content_hash
            json_data['proof_code'] = self._get_proof_code()
            json_data['proof_version'] = "v1"



        url = "https://api.aliyundrive.com/v2/file/create"
        if type == 'alibum':
            url = "https://api.aliyundrive.com/adrive/v2/biz/albums/file/create"
            json_data['proof_version'] = 'v1'
            json_data['proof_code'] = self._get_proof_code()
            json_data['content_type'] = 'image/jpeg'
            json_data['create_scene'] = 'album_autobackup'
            json_data['check_name_mode'] = 'auto_rename'

        if self.file_id == '':
            self.file_id = self.get_signTaskFileId()
        elif self.file_id != '':
            json_data['file_id'] = self.file_id

        response = s.post(url, headers=self.headers, json=json_data)
        data = response.json()

        try:
            if response.status_code == 201 or response.status_code == 200:
                rapid_upload = data.get('rapid_upload', False)
                self.file_id = data.get('file_id', '')
                print(rapid_upload)
                if rapid_upload:
                    Log(f"文件秒传匹配成功")
                else:
                    part_info_list = data.get('part_info_list', [])
                    upload_url = part_info_list[0]['upload_url']
                    if type != 'alibum':
                        self.upload_id = data.get('upload_id', '')
                    if upload_url:
                        with open(self.filePath, 'rb') as f:
                            part_content = f.read(self.size)
                        response = s.put(upload_url, data=part_content)
                        if response.status_code != 200:
                            raise Exception(f"文件上传失败")
                        Log(f"文件上传成功")
                        self.file_complete()
            elif response.status_code == 409:
                Log(f"文件秒传匹配成功")
                self.file_create('Default',False)
                # if rapid_upload:
                #     Log(f"文件秒传成功")
                #     return "文件秒传成功"
            else:
                print(f"上传文件API请求失败{data}")
        except Exception as e:
            print(f"上传文件失败：{e}")

        return ''

    def file_complete(self):
        url = "https://api.aliyundrive.com/v2/file/complete"
        json_data = {
            'file_id': self.file_id,
            'upload_id': self.upload_id,
            'drive_id': self.drive_id
        }
        response = s.post(url, headers=self.headers, json=json_data)

        if response.status_code == 200:
            print(f"上传状态上报成功")
            # file_delete(file_id, drive_id)
        else:
            print("上传文件API请求失败")

    def file_delete(self, file_id, drive_id):
        url = "https://api.aliyundrive.com/v2/file/delete"
        json_data = {
            'file_id': file_id,
            'drive_id': drive_id
        }
        response = s.post(url, headers=self.headers, json=json_data)
        if response.status_code == 204:
            # print(data)
            print(f"删除文件成功")
        else:
            print("删除文件API请求失败")

    def _get_proof_code(self) -> str:
        """计算proof_code"""
        md5_int = int(hashlib.md5(self.access_token.encode()).hexdigest()[:16], 16)
        # file_size = os.path.getsize(file_path)
        offset = md5_int % self.size if self.size else 0
        if self.filePath.startswith('http'):
            # noinspection PyProtectedMember
            bys = self._session.get(self.filePath, headers={
                'Range': f'bytes={offset}-{min(8 + offset, self.size) - 1}'
            }).content
        else:
            with open(self.filePath, 'rb') as file:
                file.seek(offset)
                bys = file.read(min(8, self.size - offset))
        return base64.b64encode(bys).decode()

    ###############################文件上传任务结束###############################
#接好运瓶
    def bottle_fish(self):
        json_data = {}
        for i in range(3):
            response = s.post('https://api.aliyundrive.com/adrive/v1/bottle/fish', headers=self.headers,
                                     json=json_data, verify=False)
            if response.status_code == 200:
                Log('接好运瓶成功！')
            else:
                print(response.text)

#######################接好运瓶并转存1个文件任务

    # 接好运瓶获取分享ID
    def get_bottleShareId(self):
        json_data = {}
        response = s.post('https://api.aliyundrive.com/adrive/v1/bottle/fish', headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200:
            resp = response.json()
            self.shareid = resp.get('shareId','')
            print(f'获取到好运瓶分享ID：【{self.shareid}】')
            self.get_shareFileId()
        else:
            print(response.text)

    #根据shareid获取分享文件file_id
    def get_shareFileId(self):
        json_data = {"share_id":self.shareid}
        response = s.post('https://api.aliyundrive.com/adrive/v2/share_link/get_share_by_anonymous', headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200:
            resp = response.json()
            file_infos = resp.get('file_infos',[])
            self.share_file_id = file_infos[0]['file_id']
            print(f'获取到文件ID：【{self.share_file_id}】')
            self.get_shareToken()

        else:
            print(response.text)

    #保存文件
    def get_shareToken(self):
        json_data ={"share_id":self.shareid}
        response = s.post('https://api.aliyundrive.com/v2/share_link/get_share_token', headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200:
            resp = response.json()
            share_token=resp.get('share_token','')
            self.headers['x-share-token'] = share_token
            self.save_shareFile()
        else:
            print(response.text)
    #保存文件
    def save_shareFile(self):
        json_data ={"requests":[{
            "body":{
                "share_id":self.shareid,
                "to_drive_id":self.default_drive_id,
                "addition_data":{"umidtoken":""},
                "auto_rename":True,"file_id":self.share_file_id,
                "to_parent_file_id":"root"},
            "headers":{"Content-Type":"application/json"},
            "id":"0","method":"POST",
            "url":"/file/copy"}],
        "resource":"file"
        }
        response = s.post('https://api.aliyundrive.com/adrive/v2/batch', headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200:
            res = response.json()
            status = res["responses"][0]["status"]
            file_id = res["responses"][0]["body"]["file_id"]
            if status == 201:
                Log('文件保存成功')
                self.file_delete(file_id, self.default_drive_id)
            else:
                print('文件保存失败')
        else:
            print(response.text)

#接好运瓶并转存1个文件任务#######################

    #领取版本升级奖励
    def version_reward(self):
        json_data = {"code":"newVersion490Reward","rule":"all"}
        response = s.post('https://member.aliyundrive.com/v1/users/space_goods_reward?_rx-s=mobile', headers=self.headers,
                                 json=json_data, verify=False)
        if response.status_code == 200:
            Log('领取版本升级奖励成功！')
        else:
            print(response.text)
    #领取奖励
    def reward_sign(self, type,sign_in_count=None):
        if sign_in_count == None:sign_in_count = self.sign_in_count
        json_data = {"signInDay": str(sign_in_count)}
        if type == 'sign_in_reward':
            url = f'https://member.aliyundrive.com/v1/activity/{type}?_rx-s=mobile'
        else:
            url = f'https://member.aliyundrive.com/v2/activity/{type}?_rx-s=mobile'
        response = s.post(url, headers=self.headers, json=json_data, verify=False)
        try:
            resp = response.json()
            if 'result' in resp and resp.get("result",None) != None:
                Log(f">{resp['result']['notice']}")
            elif 'success' in resp and resp.get("success",None) != None:
                Log(f">已领奖")
            else:
                Log(f">{resp['message']}")
        except:
            print(response.text)

    # 订阅阿里官方账号
    def follow_user(self):
        data = {"user_id": 'ec11691148db442aa7aa374ca707543c'}
        response = s.post('https://api.aliyundrive.com/adrive/v1/member/follow_user', headers=self.headers, json=data,
                          verify=False)
        if response.status_code == 200:
            Log('订阅成功！')
        else:
            print(response.text)

    # 获取最近视频列表
    def get_videoList(self):
        self.fileName = '签到任务文件_视频.mp4'
        res = self.get_signTaskFileId()
        if res:
        # data = {}
        # response = s.post('https://api.aliyundrive.com/adrive/v2/video/list', headers=self.headers, json=data,
        #                   verify=False)
        # if response.status_code == 200:
        #     data = response.json()
        #     Video_list = data.get("items",False)
        #     if Video_list:
        #         Video_list_len = len(Video_list)
        #         for i in range(Video_list_len):
        #             Video_info = Video_list[random.randint(0,Video_list_len-1)]
        #             # print(f'当前Video_info:\n{Video_info}')
        #             if Video_info.get("type", "") == 'file':
        #                 self.file_id = Video_info['file_id']
        #                 self.drive_id = Video_info['drive_id']
        #                 self.videoUpdate()
        #                 duration = Video_info['duration']
        #                 play_cursor = str(float(Video_info['play_cursor']) + 31)
        #                 print(f'待上传时间：{play_cursor}')
        #                 self.videoUpdate(duration,play_cursor)
        #                 break
            self.videoUpdate()
            radomNum = round(random.uniform(200.000, 255.000), 3)
            self.videoUpdate(radomNum, radomNum)
        elif res == '未找到签到任务文件':
            print('放映室没有视频文件，尝试转存任务视频，重新获取视频信息')
            self.shareid = 't2j7bMBYAS5'
            self.get_shareFileId()
            # self.upload_files_to_drive(1)
            self.videoUpdate()
            radomNum = round(random.uniform(200.000, 255.000), 3)
            self.videoUpdate(radomNum,radomNum)


        else:
            print(res)

    # 获取最近视频列表
    def videoUpdate(self,duration="0",play_cursor="0"):
        data = {
            "drive_id": self.default_drive_id,
            "duration": duration,
            "file_extension": 'mp4',
            "file_id": self.file_id,
            "play_cursor": play_cursor
        }
        response = s.post('https://api.aliyundrive.com/adrive/v2/video/update', headers=self.headers, json=data,
                          verify=False)
        if response.status_code == 200:
            print('>上传观看时间成功！')
        else:
            print(response.text)

    #弃用补签卡任务
    def join_team(self):
        check_team_data = {}
        check_team_res = s.post('https://member.aliyundrive.com/v1/activity/sign_in_team?_rx-s=mobile',
                                headers=self.headers, json=check_team_data, verify=False)
        try:
            resp = check_team_res.json()
            if resp['result'] != 'null':
                act_id = resp['result']['id']
                join_team_data = {"id": act_id, "team": "blue"}
                join_team_res = requests.post('https://member.aliyundrive.com/v1/activity/sign_in_team_pk?_rx-s=mobile',
                                              headers=self.headers, json=join_team_data, verify=False)
                try:
                    join_team_res = join_team_res.json()
                    if join_team_res['success']:
                        Log('>加入蓝色战队成功!')
                except:
                    print(join_team_res.text)
        except:
            print(check_team_res.text)

    #补签卡随机翻任务牌3次
    def get_cardTask(self):
        for i in range(3):
            json_data = {"position":random.randint(1,9)}
            response = s.post('https://member.aliyundrive.com/v2/activity/complement_task?_rx-s=mobile', headers=self.headers,
                                     json=json_data, verify=False)
            if response.status_code == 200:
                Log('翻卡成功')
            else:
                print(response.text)

    # 获取period
    def get_period(self):
        print(f'>>>>>开始获取补签卡任务')
        json_data = {}
        response = s.post('https://member.aliyundrive.com/v2/activity/complement_task_detail?_rx-s=mobile',headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200:
            resp = response.json()
            self.period = resp['result']['period']
            Tasks = resp['result']['tasks']
            # 在这里执行相应的操作
            if len(Tasks) < 3:
                self.get_cardTask()
                self.get_period()
            for task in Tasks:
                self.card_taskName = task['taskName']
                self.card_taskId = task['taskId']
                Log(f'>>当前任务：【{self.card_taskName}】')
                if task["status"] == "finished" or task["status"] == "verification":
                    self.reward_cardTask()
                    # Log('>本周补签卡已领取')
                    return
                if self.card_taskName == '当周使用好运瓶翻3次':
                    self.bottle_fish()
                    break
                elif self.card_taskName == '当周观看任意一个电影时间满3分钟':
                    self.get_videoList()
                    break
                elif self.card_taskName == '当周备份照片满20张':
                    Log(f'>任务：【{self.card_taskName}】暂不支持')
                    continue
                elif self.card_taskName == '当周使用快传发送文件给好友':
                    Log(f'>任务：【{self.card_taskName}】暂不支持')
                    continue
                else:
                    Log(f'>任务：【{self.card_taskName}】暂不支持')
                    continue
            self.reward_cardTask()
        else:
            print(response.text)

    # 获取历史设备ID
    def get_listDevice(self):
        json_data = {}
        response = s.post('https://user.aliyundrive.com/v1/deviceRoom/listDevice',headers=self.headers, json=json_data, verify=False)
        if response.status_code == 200 or response.status_code == 400:
            resp = response.json()
            # 检查响应是否包含'items'
            if 'items' in resp:
                items = response.json()['items']

                # 检查'items'列表是否不为空
                if items:
                    last_item = items[-1]  # 获取最后一个元素
                    self.x_device_id = last_item['id']
                    print("x_device_id :", self.x_device_id )
                    return True

                else:
                    print("items列表为空")
                    return False
            else:
                print("响应中没有'items'字段")
                return False
        else:
            print(response.text)
    #上传备份设置,
    def update_device_extras(self):
        # 生成随机的totalSize和useSize（示例范围为256GB到1TB）
        total_size = random.randint(256 * 1024 * 1024 * 1024, 1024 * 1024 * 1024 * 1024)  # 256GB到1TB
        use_size = random.randint(total_size, total_size)  # useSize小于或等于totalSize，范围也是256GB到1TB
        if self.get_listDevice():
            self.headers['x-device-id'] = self.x_device_id
        json_data = {
            "albumAccessAuthority": True,
            "albumBackupLeftFileTotal": 0,
            "albumBackupLeftFileTotalSize": 0,
            "albumFile": random.randint(1,20),
            "autoBackupStatus": True,
            "brand": "xiaomi",
            "systemVersion": "Android 11",
            "totalSize": total_size,
            "umid": "",
            "useSize": use_size,
            "utdid": ""
        }
        response = s.post('https://api.aliyundrive.com/users/v1/users/update_device_extras', headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200 or response.status_code == 400:
            resp = response.json()
            if 'success' in resp:
                print(f">{resp}")
            else:
                print(f">{resp['message']}")
        else:
            print(response.text)
    #领取补签卡
    def reward_cardTask(self):
        json_data = {"period":self.period,'taskId':self.card_taskId}
        response = s.post('https://member.aliyundrive.com/v2/activity/complement_task_reward?_rx-s=mobile', headers=self.headers,json=json_data, verify=False)
        if response.status_code == 200 or response.status_code == 400:
            resp = response.json()
            if 'success' in resp:
                print(f">补签卡领取成功")
            else:
                print(f">{resp['message']}")
        else:
            print(response.text)


    #使用补签卡
    def use_signCard(self):
        use_signCard_data = {}
        use_signCard_res = s.post('https://member.aliyundrive.com/v1/activity/complement_sign_in?_rx-s=mobile',
                                  headers=self.headers, json=use_signCard_data, verify=False)
        try:
            resp = use_signCard_res.json()
            if resp['code'] != 'BadRequest':
                Log('>补签成功！')
            else:
                Log(f">补签失败！原因：{resp['message']}")
        except:
            print(use_signCard_res.text)

    def main(self, indx):
        log_message = f"\n开始执行第【{indx + 1}】个账号--------------->>>>>"
        Log(log_message)
        current_day = datetime.datetime.now().day
        if self.getToken():
            self.get_sign_in_list()

            #新增领取版本奖励
            # self.version_reward()
            if self.ali_reward:
                Log('>>>>开始领取签到奖励')
                self.reward_sign('sign_in_reward')
                time.sleep(2)
                self.reward_sign('sign_in_task_reward')
            else:
                if not is_last_day_of_month():
                    Log(f'>今天是【{current_day}】日，您设置了不自动领取奖品，不自动领取')
                else:
                    Log('>今日为本月最后一天，默认领取所有奖品')
                    for day in range(1, current_day + 1):
                        Log(f'开始领取【第{day}天】奖品')
                        self.reward_sign('sign_in_reward', day)
                        self.reward_sign('sign_in_task_reward', day)
                        time.sleep(1)
            self.get_period()
            self.use_signCard()
        else:
            return False
#删除缓存
def del_cash(file_path):
    try:
        # 删除文件
        os.remove(file_path)
        print(">缓存文件删除成功")
        return True
    except FileNotFoundError:
        print(">缓存文件不存在")
        return "缓存文件不存在"
    except Exception as e:
        print(f">缓存文件删除失败：{e}")
        return f"缓存文件删除失败：{e}"

# 对比缓存与环境变量 token 长度
def len_comp(cached_tokens, env_token):
    global refresh_tokens, LEN
    if cached_tokens != '':
        cached_tokens = '#'.join(cached_tokens.values())
        cached_token_list = cached_tokens.split("#")
        cached_token_len = len(cached_token_list)
    else:
        cached_token_len = 0

    env_token_list = env_token.split("&")
    env_token_len = len(env_token_list)

    if env_token_len != cached_token_len:
        print("***缓存 freshToken 长度与环境变量长度不一致，使用【环境变量】")
        del_cash(REFRESHTOEKN_PATH)
        refresh_tokens = env_token_list
        LEN = env_token_len
    else:
        print("***缓存 freshToken 长度与环境变量长度一致，使用【缓存】")
        refresh_tokens = cached_token_list
        LEN = cached_token_len

def compare_versions(local_version, server_version):
    local_parts = local_version.split('.')  # 将本地版本号拆分成数字部分
    server_parts = server_version.split('.')  # 将服务器版本号拆分成数字部分

    for l, s in zip(local_parts, server_parts):
        if int(l) < int(s):
            return True  # 当前版本低于服务器版本
        elif int(l) > int(s):
            return False  # 当前版本高于服务器版本

    # 如果上述循环没有返回结果，则表示当前版本与服务器版本的数字部分完全相同
    if len(local_parts) < len(server_parts):
        return True  # 当前版本位数较短，即版本号形如 x.y 比 x.y.z 低
    else:
        return False  # 当前版本与服务器版本相同或更高

def check_update(local_version, server_version_url, server_script_url, script_filename):
    """
    检查版本并更新

    Args:
        local_version (str): 本地版本号
        server_version_url (str): 服务器版本文件地址
        server_script_url (str): 服务器脚本地址
        script_filename (str): 要保存的脚本文件名

    Returns:
        bool: 是否进行了更新操作
    """
    # 获取服务器版本号
    response = requests.get(server_version_url,verify=False)
    if response.status_code == 200:
        server_version = response.text.strip()  # 去除首尾空格
        print(f'当前版本：【{local_version}】')
        print(f'服务器版本：【{server_version}】')

        if compare_versions(local_version, server_version):
            # 需要更新，下载服务器脚本
            AUTO_UPDATE =os.getenv("ALYP_UPDATE", "True").lower() != "false"
            # print(AUTO_UPDATE)
            if AUTO_UPDATE:
                print(">>>>>>>发现新版本的脚本，默认自动更新，准备更新...")
                print(">>>>>>>禁用更新请定义变量export ALYP_UPDATE = 'False'")
                response = requests.get(server_script_url,verify=False,timeout=10)
                if response.status_code == 200:
                    with open(script_filename, 'wb') as f:
                        f.write(response.content)
                    print(f'{script_filename} 下载完成！')
                    return True
                else:
                    print(f'下载失败：{response.status_code}')
            else:
                print(">>>>>>>发现新版本的脚本，您禁用了自动更新，如需启用请删除变量ALYP_UPDATE")
        else:
            print(f'当前版本高于或等于服务器版本')
    else:
        print(f'获取服务器版本失败：{response.status_code}')

    return False

if __name__ == '__main__':
    print('''
✨✨✨ 阿里云盘任务脚本✨✨✨
✨脚本更新地址：https://pan.ziyuand.cn/%E8%BD%AF%E4%BB%B6%E8%B5%84%E6%BA%90%E7%B1%BB/%E8%84%9A%E6%9C%AC/%E9%98%BF%E9%87%8C%E4%BA%91%E7%9B%98
✨获取refresh_token：
    https://alist.nn.ci/zh/guide/drivers/aliyundrive.html
    http://qr.ziyuand.cn/
✨自动签到
✨自动补签
✨自动完成签到任务（部分）
✨自动完成补签卡任务（部分）
✨自动领取任务奖品（如无需自动领取请定义变量：export ali_reward="False"，默认每月最后一天自动领取所有任务奖品）
✨支持青龙（变量：export ALYP="xxxx"）
✨支持多账号（使用&分割refresh_token）
✨脚本自动更新（禁用更新，变量：ALYP_UPDATE = "False"）
✨强制使用变量不使用缓存Token（变量：USE_ENV= "True"）
✨✨✨ @Author CHERWIN✨✨✨
    ''')
    # 检查更新
    local_version = '2023.11.05'  # 本地版本
    server_base_url="http://pan.ziyuand.cn/d/软件资源类/脚本/阿里云盘/"
    server_script_url = f"{server_base_url}ALYP.py"
    server_version_url = f'{server_base_url}version.txt'  # 服务器版本文件地址
    check_update(local_version, server_version_url, server_script_url, 'ALYP.py')

    refresh_tokens = ''
    LEN = 0
    ENV = os.environ.get("ALYP")
    #强制使用环境变量，首次或增加账号后建议开启，跑一次删除变量，青龙变量 export USE_ENV = True
    USE_ENV = os.environ.get("USE_ENV") if environ.get("USE_ENV") else False
    if USE_ENV:
        print('当前强制使用变量')
        del_cash(REFRESHTOEKN_PATH)
    refresh_token = ENV if ENV else refresh_tokens
    Cach_Tokens = loadRefreshTokens()
    if refresh_token:
        len_comp(Cach_Tokens, refresh_token)
    else:
        print("******未填写 ALYP 变量。青龙可在环境变量设置 ALYP 或者在本脚本文件上方将获取到的 refresh_token 填入refresh_token后面的''中")
        exit(0)

    #自动领取开关
    ali_reward = environ.get("ali_reward") if environ.get("ali_reward") else True
    if ali_reward:
        print('******默认自动领取奖品,如需关闭自动领取请定义变量：export ali_reward="False"\n******默认自动补签')
    else:
        print('******设置了不自动领取奖品')
    print(f'******当前使用token：\n{refresh_tokens}')
    if LEN > 0:
        print(f"\n>>>>>>>>>>共获取到{LEN}个账号<<<<<<<<<<")
        for indx, ck in enumerate(refresh_tokens):
            s = requests.session()
            s.verify = False
            # print(ck)
            Sign = AliDrive_CheckIn(ck, ali_reward).main(indx)
            if not Sign: continue


        send('阿里云盘签到通知', send_msg)
