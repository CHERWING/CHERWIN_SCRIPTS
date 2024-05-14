'''
!/usr/bin/python3
-- coding: utf-8 --
-------------------------------
✨✨✨ @Author CHERWIN✨✨✨
cron "0 9 * * *" script-path=xxx.py,tag=匹配cron用
const $ = new Env('朴朴超市APP')
'''

import json
import os
import random
import time
from sys import exit
from datetime import datetime, timedelta
from urllib.parse import urlparse

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

class RUN:
    def __init__(self, info,index,access_token=None,user_id=None):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        self.refresh_token = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        if len_split_info > 0 and "UID_" in last_info:
            self.send_UID = last_info
        self.index = index + 1

        Log(f"\n---------开始执行第{self.index}个账号>>>>>")
        self.s = requests.session()
        self.s.verify = False
        self.UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/8555'
        self.headers = {
            'Authorization': '',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.UA,
            'Origin': 'https://ma.pupumall.com',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ma.pupumall.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'pp-os': '0'
        }
        # print(self.refresh_token)
        self.team_need_help = False
        self.teamId = ''
        self.location = {}
        self.store_id = None
        self.zip = None
        self.lng = None
        self.lat = None
        self.boost_id = ''
        self.boost_id_li = []
        self.boost_name = ''
        self.boost_type = ''
        self.boost_is_enabled = ''
        self.boost_is_finished = ''
        self.boost_entity_id = ''
        self.need_newuser = False
        self.status = False
        self.params = {
            'supplement_id': '',
            'lat_y': '',
            'lng_x': '',
        }
        if access_token:
            self.access_token=access_token
            self.headers['Authorization'] = access_token
            self.headers['pp-userid'] = user_id
        self.near_location_by_city()
        self.wait_time = random.randint(1000, 3000) / 1000.0  # 转换为秒



    def make_request(self, url, method='post',headers={},params='',data={}):
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        self.headers['Host'] = host
        if headers == {}:
            headers = self.headers
        if data =={}:
            data = self.params
        try:
            if method.lower() == 'get':
                response = self.s.get(url, headers=headers, verify=False,params=params)
            elif method.lower() == 'post':
                response = self.s.post(url, headers=headers, json=data, verify=False)
            else:
                raise ValueError("不支持的请求方法: " + method)

            return response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常：", e)
        except ValueError as e:
            print("值错误或不支持的请求方法：", e)
        except Exception as e:
            print("发生了未知错误：", e)

    def near_location_by_city(self):
        print('>>>>>>开始随机选择位置')
        url = 'https://j1.pupuapi.com/client/store/place/near_location_by_city/v2'
        # 生成随机的四位数
        random_digits = ''.join(random.choices('0123456789', k=13))
        # 准备查询参数
        search_params = {
            'lng': '119.30' + random_digits,
            'lat': '26.08' + random_digits
        }
        try:
            result =self.make_request(url,method='get',params=search_params)
            errcode = result.get('errcode', -1)
            if errcode == 0:
                data = result.get('data')
                # 假设randomList是一个选择列表中随机元素的方法
                self.location = self.randomList(data)
                self.store_id = self.location['service_store_id']
                self.zip = self.location['city_zip']
                self.lng = str(self.location['lng_x'])
                self.lat = str(self.location['lat_y'])
                self.params['lat_y'] = self.lat
                self.params['lat_x'] = self.lng
                # 更新请求头部
                self.headers['pp_storeid'] = self.store_id
                self.headers['pp-cityzip'] = str(self.zip)
                print('>选取随机地点成功')
            else:
                errmsg = result.get('errmsg', '')
                print(f'>选取随机地点失败[{errcode}]: {errmsg}')
        except Exception as e:
            print(e)

    def randomList(self, lst):
        # 返回列表中的随机项
        return random.choice(lst)

    def get_AccessToken(self):
        # Log('获取access_token')
        url = "https://cauth.pupuapi.com/clientauth/user/refresh_token"
        data = {
            "refresh_token": self.refresh_token
        }
        headers = {
            "User-Agent": "Pupumall/4.7.3;Android/11;dda37894d1b4c3ed09b6272c55b37cf2",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "cauth.pupuapi.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

        try:
            response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
            response.raise_for_status()

            json_response = response.json()
            # print(json_response)
            data = json_response.get('data', {})
            access_token = data.get('access_token', '')
            if access_token:
                self.access_token = f'Bearer '+access_token
                self.user_id = data.get('user_id')
                self.name = data.get('nick_name', '')
                self.is_new_user = data.get('is_new_user', '')
                self.headers['Authorization'] = self.access_token
                self.headers['pp-userid'] = self.user_id
                append_data = {
                    'access_token':self.access_token,
                    'user_id':self.user_id
                }
                access_token_li.append(append_data)
                self.status = True
                # print(f'账号【{self.index}】access_token：{self.access_token}')
                return True
            else:
                return False
        except requests.exceptions.HTTPError as http_err:
            Log(f"HTTP请求出错: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            Log(f"网络连接出错: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            Log(f"请求超时: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            Log(f"出现了一个意外的请求错误: {req_err}")
        except json.JSONDecodeError as json_err:
            Log(f"JSON解码错误: {json_err}")
        return False


    def getUserInfo(self):
        global inviteCode
        Log(f'>>>>>>获取用户信息')
        url = "https://cauth.pupuapi.com/clientauth/user/info"

        # response = self.do_request(url, headers=headers,req_type='get')
        response = self.make_request(url,method='get')
        # print(response)
        if 'errcode' in response and response.get('errcode', '') == 0:
            data = response.get('data')
            self.user_id = data.get('user_id')
            phone_number = data['phone']
            self.phone = phone_number[:3] + '****' + phone_number[7:]
            self.invite_code = data['invite_code']
            Log(f'手机号：【{self.phone}】')
            print(f'用户ID：【{self.user_id}】\n邀请码：【{self.invite_code}】')
            # new_data = {
            #     self.user_id:
            #         {
            #             'phone': self.phone,
            #             'invite_code': self.invite_code
            #         }
            # }
            # CHERWIN_TOOLS.SAVE_INVITE_CODE("INVITE_CODE/PPCS_INVITE_CODE.json", new_data)
            return True
        else:
            Log(f'>获取用户信息失败')
            print(response)
            return False

    def signStu(self):
        Log(f'>>>>>>获取签到状态')
        url = 'https://j1.pupuapi.com/client/game/sign/v2/index'
        try:
            result = self.make_request(url, 'get')
            errcode = result.get('errcode', 1)
            if errcode == 0:
                data = result.get('data', {})
                is_signed = data.get('is_signed', 0)
                if is_signed:
                    Log('今天已签到')
                else:
                    self.sign()
            else:
                errmsg = result.get('errmsg', '')
                print('查询签到信息失败[{}]: {}'.format(errcode, errmsg))
        except Exception as e:
            print('签到索引过程中发生错误: {}'.format(e))

    def getCoinInfo(self):
        url = "https://j1.pupuapi.com/client/coin"
        # response = self.do_request(url, req_type='get')
        response = self.make_request(url,method='get')
        # print(response)
        if 'errcode' in response and response.get('errcode', '') == 0:
            data = response.get('data')
            # 当前朴分
            coin = data['balance']
            Log(f'当前朴分：【{coin}】')
        else:
            Log(f'>获取当前朴分失败')
            print(response)



    def sign(self):
        Log(f'>>>>>>开始签到')
        url = "https://j1.pupuapi.com/client/game/sign/v2?supplement_id="
        # 签到
        data = {'supplement_id': ''}
        try:
            result = self.make_request(url, 'post', data=data)
            errcode = result.get('errcode', 1)
            if errcode == 0:
                data = result.get('data', {})
                daily_sign_coin = data.get('daily_sign_coin', 0)
                coupon_list = data.get('coupon_list', [])

                rewards = [str(daily_sign_coin) + '积分']
                for coupon in coupon_list:
                    condition_amount = '{:.2f}'.format(coupon['condition_amount'] / 100)
                    discount_amount = '{:.2f}'.format(coupon['discount_amount'] / 100)
                    rewards.append('满{}减{}券'.format(condition_amount, discount_amount))
                Log('签到成功: ' + ', '.join(rewards))
            else:
                errmsg = result.get('errmsg', '')
                Log('签到失败[{}]: {}'.format(errcode, errmsg))
        except Exception as e:
            Log('签到过程中发生错误: {}'.format(e))

    # 发起组队
    def creatTeam(self):
        global inviteCode
        Log(f'>>>>>>开始发起组队')
        url = "https://j1.pupuapi.com/client/game/coin_share/team"
        response = self.make_request(url)
        # print(response)
        if 'errcode' in response and response.get('errcode', '') == 0:
            data = response.get('data')
            self.teamId = data
            Log(f'>发起组队成功，ID：【{data}】')
            return True
        elif 'errcode' in response and response.get('errcode', '') != 0:
            Log(f'>发起组队失败:【{response.get("errmsg", "")}】')
        else:
            Log(f'>发起组队失败')
            print(response)
            return False

    def get_myTeam(self):
        Log(f'>>>>>>开始查询历史组队')
        # 获取当前日期
        today = datetime.now().date()
        # 构建当天的23:59:59时间
        end_of_day = datetime.combine(today, datetime.max.time()) + timedelta(hours=23, minutes=59, seconds=59)
        # 将时间转换为时间戳（毫秒为单位）
        timestamp = int(end_of_day.timestamp() * 1000)
        # 将日期格式化为字符串
        formatted_date = today.strftime("%Y-%m-%d")
        # print(timestamp)
        # print(formatted_date)
        url = f'https://j1.pupuapi.com/client/game/coin_share/records?time_from=1704038400000&time_to={timestamp}&page=1&size=20'
        try:
            result = self.make_request(url,method='get')
            errcode = result.get('errcode', -1)
            isCreatTeam = False
            if errcode == 0:
                data = result.get('data',[{}])
                for team in data:
                    # print(team)
                    record_type = team.get('record_type','')
                    time_create = team.get('time_create','')
                    # 将时间戳转换为 datetime 对象
                    timestamp = time_create / 1000  # 将时间戳转换为秒
                    dt = datetime.fromtimestamp(timestamp)
                    # 将日期格式化为字符串
                    formatted_time_create = dt.strftime("%Y-%m-%d")
                    team_id = team.get('team_id','')
                    # print(record_type)
                    # print(formatted_time_create)
                    # print(team_id)
                    if record_type == 0 and formatted_time_create == formatted_date:
                        self.teamId = team_id
                        isCreatTeam =True
                        break
                if isCreatTeam:
                    Log(f'今日已创建ID：【{self.teamId}】队伍')
                    self.check_my_team()
                else:
                    self.creatTeam()
            else:
                errmsg = result.get('errmsg', '')
                print(f'查询组队历史信息失败[{errcode}]: {errmsg}')
        except Exception as e:
            print(str(e))

    def check_my_team(self):
        Log(f'>>>>>>开始查询组队详情')
        url = f'https://j1.pupuapi.com/client/game/coin_share/teams/{self.teamId}'
        try:
            result = self.make_request(url,method='get')
            errcode = result.get('errcode', -1)
            if errcode == 0:
                data = result.get('data')
                status = data.get('status')
                if status == 10:
                    self.team_need_help = True
                    self.team_max_help = data.get('target_team_member_num')
                    self.team_helped_count = data.get('current_team_member_num')
                    Log(f'组队未完成: {self.team_helped_count}/{self.team_max_help}')
                elif status == 30:
                    self.team_need_help = False
                    coins = data.get('current_user_reward_coin')
                    Log(f'已组队成功, 获得了{coins}积分')
                else:
                    Log(f'组队状态[{status}]')
                    print(f': {json.dumps(data)}')
            else:
                errmsg = result.get('errmsg', '')
                print(f'查询组队信息失败[{errcode}]: {errmsg}')
        except Exception as e:
            print(str(e))

    # 组队
    def joinAuthorTeam(self):
        print(f'>>>>>>第1个账号开始助力作者')
        if len(AuthorCode) > 0:
            for code in AuthorCode:
                # print(code['teamId'])
                if code.get('status',False) and code.get('phone','') != self.phone:
                    url = f"https://j1.pupuapi.com/client/game/coin_share/teams/{code['teamId']}/join"
                    response = self.make_request(url)
                    # print(response)
                    if 'errcode' in response and response.get('errcode', '') == 0:
                        print(f'>入队成功:【{code}】')
                        break
                # elif 'errcode' in response and response.get('errcode', '') != 0:
                #     print(f'>入队失败:【{response.get("errmsg", "")}】')
                # else:
                #     print(f'>入队失败')
                #     print(response)
# 组队
    def joinTeam(self):
        global inviteCode
        Log(f'>>>>>>开始本地组队')
        with open('INVITE_CODE/PPCS_INVITE_CODE.json', 'r') as file:
            data = json.load(file)
        inviteCode = list(data.values())
        for code in inviteCode:
            teamId = code.get('teamId',False)
            if not teamId:continue
            url = f"https://j1.pupuapi.com/client/game/coin_share/teams/{code['teamId']}/join"
            response = self.make_request(url)
            # print(response)
            if 'errcode' in response and response.get('errcode', '') == 0:
                Log(f">入队成功:【{code['teamId']}】")
            elif 'errcode' in response and response.get('errcode', '') != 0:
                Log(f'>入队失败:【{response.get("errmsg", "")}】')
            else:
                Log(f'>入队失败')
                print(response)

    def boost_recommend(self):
        print(f'>>>>>>开始获取助力活动列表')
        url = f'https://j1.pupuapi.com/client/boost/recommend'
        try:
            result = self.make_request(url,method='get')
            errcode = result.get('errcode', -1)
            if errcode == 0:
                data = result.get('data',[])
                for li in data:
                    self.boost_id = li.get('id','')
                    self.boost_name = li.get('name','')
                    self.boost_type = li.get('type','')
                    self.boost_is_enabled = li.get('is_enabled','')
                    self.boost_is_finished = li.get('is_finished','')
                    self.boost_entity_id = li.get('entity_id','')
                    self.boost_finish_condition_msg = li.get('boost_finish_condition_msg','')


                    if self.boost_entity_id:
                        print(f'当前项目：【{self.boost_name}】 已发起 ID：【{self.boost_entity_id}】 完成状态：{self.boost_is_finished} ')
                        li = {
                            'boost_entity_id': self.boost_entity_id,
                            'boost_type': self.boost_type,
                            'need_newuser':self.need_newuser
                        }
                        self.boost_id_li.append(li)
                        continue
                    print(f'当前项目：【{self.boost_name}】 完成状态：{self.boost_is_finished} ')
                    if '新人' in self.boost_finish_condition_msg:
                        self.need_newuser = True
                        continue
                    if not self.boost_take_in():break
                print(self.boost_id_li)

            else:
                errmsg = result.get('errmsg', '')
                print(f'查询组队信息失败[{errcode}]: {errmsg}')
        except Exception as e:
            print(str(e))

    def boost_help(self):
        print(f'>开始助力')
        if len(AuthorCode) > 0:
            for code in AuthorCode:
                # print(code['teamId'])
                if code.get('status',False) and code.get('phone','') != self.phone and code.get('boost',False) and self.is_new_user:
                    boost_li = code.get('boost',[])
                    for boost in boost_li:
                        boost_entity_id = boost.get('boost_entity_id','')
                        boost_type = boost.get('boost_type', '')
                        url = f'https://j1.pupuapi.com/client/boost/assist/{boost_entity_id}?group_type={boost_type}'
                        # try:
                        result = self.make_request(url)
                        errcode = result.get('errcode', -1)
                        if errcode == 0:
                            print('助力成功')
                            self.is_new_user = False
                            break
                        else:
                            errmsg = result.get('errmsg', '')
                            print(f'助力失败[{errcode}]: {errmsg}')
                            break
                else:
                    continue
        # except Exception as e:
        #     print(str(e))

    def boost_take_in(self):
        print(f'>开始发起助力活动')
        self.lng = str(self.location['lng_x'])
        self.lat = str(self.location['lat_y'])
        url = f'https://j1.pupuapi.com/client/boost/take_in/{self.boost_id}?lat_y={self.lat}&lng_x={self.lng}'
        # try:
        result = self.make_request(url)
        errcode = result.get('errcode', -1)
        if errcode == 0:
            self.boost_entity_id = result.get('data','')
            # print(self.boost_entity_id)
            if self.boost_entity_id:
                li = {
                        'boost_entity_id':self.boost_entity_id,
                        'boost_type':self.boost_type,
                        'need_newuser':self.need_newuser
                    }
                self.boost_id_li.append(li)
                return True
        else:
            errmsg = result.get('errmsg', '')
            print(f'发起组队失败[{errcode}]: {errmsg}')
            return False
        # except Exception as e:
        #     print(str(e))


    def main(self):
        # print(self.refresh_token)
        if self.get_AccessToken():
            print('成功获取了access token.')
            self.getUserInfo()
            self.signStu()
            self.getCoinInfo()
            self.get_myTeam()
            self.boost_recommend()
            if self.is_new_user:
                self.boost_help()
            new_data = {
                self.user_id:
                    {
                        'status': self.status,
                        'phone': self.phone,
                        'invite_code': self.invite_code,
                        'boost':self.boost_id_li
                    }
            }
            if self.teamId:new_data[self.user_id]['teamId']=self.teamId
            CHERWIN_TOOLS.SAVE_INVITE_CODE("INVITE_CODE/PPCS_INVITE_CODE.json", new_data)
            self.sendMsg()
            return True
        else:
            Log( f'账号[{self.index}] {CK_NAME}:\n【{self.refresh_token}】\n已失效请及时更新')
            self.sendMsg()
            return False


    def help(self):
        if self.get_AccessToken():
            if self.index == 1:
                print('--------签到组队--------')
                self.joinAuthorTeam()
            else:
                print('--------签到组队--------')
                self.joinTeam()
            return True
        else:
            Log(f'账号[{self.index}] {CK_NAME}:\n【{self.refresh_token}】\n已失效请及时更新')
            self.sendMsg(True)
            return False


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
    ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode = CHERWIN_TOOLS.main(APP_NAME, local_script_name, ENV_NAME,local_version,True)

if __name__ == '__main__':
    APP_NAME = '朴朴超市'
    ENV_NAME = 'PPCS'
    CK_NAME = 'refresh_token'
    print(f'''
✨✨✨ 朴朴超市脚本✨✨✨
✨ 功能：
      积分签到
      组队互助
✨ 抓包步骤：
      打开朴朴超市APP
      已登录先退出
      打开抓包
      登陆
      找https://cauth.pupuapi.com/clientauth/user/verify_login
      复制返回body中的{CK_NAME}
      多个账号可清理APP数据进行换号别点退出否则token失效
✨ 设置青龙变量：
export {ENV_NAME}= 'E0oXq3++6a4LG4xxxxxxxx'多账号#分割
export SCRIPT_UPDATE = 'False' 关闭脚本自动更新，默认开启
✨ 多账号默认第一个账号与作者组队，其余互助
✨ 推荐定时：0 9 * * *
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
    # with open('INVITE_CODE/PPCS_INVITE_CODE.json','r') as f:
    #     content = json.loads(f.read())
    #     print(content)

    # AuthorCode = list(content.values())
    # print(AuthorCode)
    # print(tokens)
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
        access_token_li=[]
        for index, infos in enumerate(tokens):
            run_result = RUN(infos, index).main()
            if not run_result: continue

        for index, infos in enumerate(tokens):
            RUN(infos, index).help()
            if not run_result: continue
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)


