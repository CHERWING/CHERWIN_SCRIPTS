# !/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# cron "30 1 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('霸王茶姬小程序')

import os
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f) XWEB/8555',
            'work-wechat-userid': '',
            'multi-store-id': '',
            'gdt-vid': '',
            'qz-gtd': '',
            'scene': '1006',
            'Qm-From': 'wechat',
            'store-id': '49006',
            'Qm-User-Token': self.token,
            'channelCode': '',
            'Qm-From-Type': 'catering',
            'promotion-code': '',
            'work-staff-name': '',
            'work-staff-id': '',
            'Accept': 'v=1.0',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Referer': 'https://servicewechat.com/wxafec6f8422cb357b/87/page-frame.html'
        }
        self.s.headers.update(self.headers)
        self.appid = 'wxafec6f8422cb357b'
        self.activity_id='947079313798000641'

    def personal_info(self):
        personal_info_valid = False

        try:
            # 请求的参数
            params = {'appid': self.appid}

            # 发送GET请求
            response = self.s.get('https://webapi.qmai.cn/web/catering/crm/personal-info', json=params)
            result = response.json()

            # 检查请求是否成功
            if result.get('code','-1') == '0':
                personal_info_valid = True
                # 提取个人信息
                mobile_phone = result['data']['mobilePhone'] if 'data' in result and 'mobilePhone' in result[
                    'data'] else None
                self.mobile_phone = mobile_phone[:3] + "*" * 4 + mobile_phone[7:]
                self.name = result['data']['name'] if 'data' in result and 'name' in result['data'] else None

                Log(f"账号[{self.index}]登陆成功！\n用户名：【{self.name}】 \n手机号：【{self.mobile_phone}】")
            else:
                # 如果请求不成功，则打印错误信息
                message = result.get('message', '')
                Log(f'登录失败: {message}')

        except Exception as e:
            # 捕获任何异常并打印
            print(e)

        finally:
            # 最终返回请求是否成功的标志
            return personal_info_valid

    def user_sign_statistics(self):
        try:

            json_data = {
                'activityId': self.activity_id,
                'appid': self.appid
            }

            # Send the POST request
            response = self.s.post('https://webapi.qmai.cn/web/cmk-center/sign/userSignStatistics', json=json_data)
            result = response.json()
            status_code = response.status_code

            # Check if the request was successful
            if result.get('code', status_code) == 0:
                data = result.get('data', {})
                sign_days = data.get('signDays', '')
                sign_status = data.get('signStatus', 0) == 1
                Log(f'新版签到今天{"已" if sign_status else "未"}签到, 已连续签到{sign_days}天')
                if not sign_status:
                    self.take_part_in_sign()
                return sign_status, sign_days
            else:
                message = result.get('message', '')
                Log(f'查询新版签到失败: {message}')
                return False, 0
        except Exception as e:
            print(e)
            return False, 0

    def take_part_in_sign(self):
        try:
            json_data = {
                'activityId': self.activity_id,
                'appid': self.appid
            }
            response = self.s.post('https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign', json=json_data)
            result = response.json()
            status_code = response.status_code

            if result.get('code', status_code) == 0:
                data = result.get('data',{})
                rewardDetailList = data.get('rewardDetailList',[{}])
                if rewardDetailList:
                    rewardName = rewardDetailList[0].get('rewardName','')
                    sendNum = rewardDetailList[0].get('sendNum','')
                    Log(f'新版签到成功，获得【{sendNum}】{rewardName}')
                    return True
                else:
                    Log(f'签到失败：【{result.get("message","")}】')
                    return True
            else:
                message = result.get('message', '')
                Log(f'新版签到失败: {message}')
                return False
        except Exception as e:
            print(e)
            return False

    def points_info(self):
        try:
            json_data = {
                'appid': self.appid
            }

            response = self.s.post('https://webapi.qmai.cn/web/catering/crm/points-info', json=json_data)
            result = response.json()
            status_code = response.status_code

            if result.get('code', status_code) == '0':
                data = result.get('data', {})
                soon_expired_points = data.get('soonExpiredPoints', 0)
                total_points = data.get('totalPoints', 0)
                expired_time = data.get('expiredTime', '')

                if soon_expired_points:
                    Log(f'有【{soon_expired_points}】积分将于（ {expired_time}）过期')

                Log(f'当前积分: 【{total_points}】')
                return total_points, soon_expired_points, expired_time
            else:
                message = result.get('message', '')
                Log(f'查询积分失败: {message}')
                return None
        except Exception as e:
            print(e)
            return False

    def main(self):
        if not self.personal_info() :
            Log("用户信息无效，请更新CK")
            self.sendMsg()
            return False
        self.user_sign_statistics()
        self.points_info()
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
    APP_NAME = '霸王茶姬小程序'
    ENV_NAME = 'BWCJ'
    CK_NAME = 'qm-user-token'
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
参数示例：Fks8FqmiTksnmZSj2fDvxxxxxxxxx@UID_xxxxx
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
        if send: send(f'{APP_NAME}挂机通知', send_msg + TIPS_HTML)