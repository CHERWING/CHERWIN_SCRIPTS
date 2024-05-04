import json
import os
import importlib.util
import subprocess
import sys
import requests
from http import HTTPStatus

NOW_TOOLS_VERSION = '2024.05.04'
if os.path.isfile('DEV_ENV.py'):
    import DEV_ENV


# 尝试导入包
def import_or_install(package_name, import_name=None):
    # 如果传入了 import_name，则使用它来检查模块，否则默认与包名相同
    import_name = import_name or package_name

    try:
        # 检查模块是否已安装
        package_spec = importlib.util.find_spec(import_name)

        if package_spec is None:
            print(f"{package_name} 模块未安装. 开始安装...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            print(f"{package_name} 模块安装完成。")
        else:
            print(f"{package_name} 模块已安装。")

        # 尝试导入模块检查是否安装成功
        __import__(import_name)
        module = importlib.import_module(import_name)
        print(f"{import_name} 模块导入成功.")
        return module
    except ImportError as e:
        print(f"无法导入 {import_name} 模块. 错误信息: {e}")
    except subprocess.CalledProcessError as e:
        print(f"安装 {package_name} 模块时出错. 错误信息: {e}")
    except Exception as e:
        print(f"处理 {package_name} 模块时发生错误. 错误信息: {e}")


def SAVE_INVITE_CODE(file_name, new_data):
    # 读取现有JSON文件（如果存在）
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，创建所需目录并一个新的空JSON文件
        directory = os.path.dirname(file_name)
        if not os.path.exists(directory):
            os.makedirs(directory)
        data = {}

    # 检查是否已存在相同的键，如果存在，合并数据
    for key, value in new_data.items():
        if key in data:
            # 如果键已存在，将新数据合并到现有数据中
            data[key].update(value)
        else:
            # 如果键不存在，直接插入新数据
            data[key] = value

    # 将更新后的数据写入JSON文件
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


# 将参数转换为字典
def create_dict_from_string(self, data_string):
    params = {}
    key_value_pairs = data_string.split(',')
    for pair in key_value_pairs:
        key, value = pair.split('=')
        params[key] = value
    return params


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


def CHECK_UPDATE(local_version, server_version_url, server_script_url, script_filename):
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
    try:
        # 获取服务器版本号
        response = requests.get(server_version_url, verify=False)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        # print(response.text)
        server_version = response.text.strip()  # 去除首尾空格
        print(f'当前版本：【{local_version}】')
        print(f'服务器版本：【{server_version}】')

        if compare_versions(local_version, server_version):
            # 需要更新，下载服务器脚本
            AUTO_UPDATE = os.getenv("SCRIPT_UPDATE", "True").lower() != "false"
            # print(AUTO_UPDATE)
            if AUTO_UPDATE:
                print(">>>>>>>发现新版本的脚本，默认自动更新，准备更新...")
                print(">>>>>>>禁用更新请定义变量export SCRIPT_UPDATE = 'False'")
                response_script = requests.get(server_script_url, verify=False, timeout=10)
                response_script.raise_for_status()

                with open(script_filename, 'wb') as f:
                    f.write(response_script.content)
                print(f'{script_filename} 下载完成！')
                print(f'尝试运行新脚本')
                import subprocess, sys
                # 使用 sys.executable 获取 Python 可执行文件的完整路径
                python_executable = sys.executable
                subprocess.Popen([python_executable, script_filename])

            else:
                print(">>>>>>>发现新版本的脚本，您禁用了自动更新，如需启用请删除变量SCRIPT_UPDATE")
        else:
            print(f'当前版本高于或等于服务器版本')

    except requests.exceptions.RequestException as e:
        print(f'发生网络错误：{e}')

    except Exception as e:
        print(f'发生未知错误：{e}')

    return False  # 返回 False 表示没有进行更新操作


def CHECK_UPDATE_NEW(local_version, server_version, server_script_url, script_filename, server_version_url=None,
                     APP_NAME=None):
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
    print(f'当前检测：【{script_filename}】')
    try:
        if server_version_url:
            # 获取服务器版本号
            response = requests.get(server_version_url, verify=False)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            # print(response.text)
            server_version = response.text.strip()  # 去除首尾空格
            if "code" in server_version:
                print('【获取远程版本号失败,设为本地同版本】')
                server_version = local_version
        if not server_version: server_version = NOW_TOOLS_VERSION
        print(f'本地版本：【{local_version}】')
        print(f'服务器版本：【{server_version}】')

        if compare_versions(local_version, server_version):
            # 需要更新，下载服务器脚本
            AUTO_UPDATE = os.getenv("SCRIPT_UPDATE", "True").lower() != "false"
            # print(AUTO_UPDATE)
            if AUTO_UPDATE:
                print(">>>>>>>发现新版本的脚本，默认自动更新，准备更新...")
                print(">>>>>>>禁用更新请定义变量export SCRIPT_UPDATE = 'False'")
                if down_file(script_filename, server_script_url):
                    print(f'请重新运行新脚本\n')
                    return True
            else:
                print(">>>>>>>发现新版本的脚本，您禁用了自动更新，如需启用请删除变量SCRIPT_UPDATE\n")
        else:
            print(f'无需更新\n')
            return False

    except requests.exceptions.RequestException as e:
        print(f'发生网络错误：{e}')
        server_base_url = f"https://py.cherwin.cn/{APP_NAME}/"
        server_script_url = f"{server_base_url}{script_filename}"
        CHECK_UPDATE_NEW(local_version, server_version, server_script_url, script_filename, APP_NAME=APP_NAME)

    except Exception as e:
        print(f'发生未知错误：{e}')

    return False  # 返回 False 表示没有进行更新操作


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


def get_AuthorInviteCode(url):
    global AuthorCode
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            content = json.loads(response.text)
            AuthorCode = list(content.values())
            # print(f'获取到作者邀请码：{AuthorCode}')
            return AuthorCode
        else:
            # print("无法获取文件。状态代码:", response.status_code)
            return {}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def GET_TIPS(server_base_url):
    url = f'{server_base_url}tips.txt'
    try:
        response = requests.get(url, verify=False)
        # 检查响应的编码
        encoding = response.encoding
        # print(f"编码: {encoding}")
        # 设置正确的编码（根据实际情况可能需要调整）
        response.encoding = 'utf-8'
        # 读取内容
        content = response.text
        if 'code' in content:
            content = None
    except:
        content = None
        print('获取通知内容失败')
    if content:
        return (f'''
***********通知内容************\n
{content}
***********通知内容************\n
''')
    else:
        return (f'''
***********通知内容************\n
        @Author Cherwin
***********通知内容************\n
''')


def CHECK_PARAMENTERS(index, input_string, required_parameters):
    # required_parameters = ['deviceid', 'jysessionid', 'shopid', 'memberid', 'access_token', 'sign']

    # 记录缺少的参数
    missing_parameters = []

    # 将输入字符串和参数列表中的所有字符都转换为小写
    input_string_lower = input_string.lower()
    required_parameters_lower = [param.lower() for param in required_parameters]

    # 判断字符串中是否包含所有必需的参数
    for param in required_parameters_lower:
        if param not in input_string_lower:
            missing_parameters.append(param)

    if missing_parameters:
        print(f"\n第【{index + 1}】个账号，缺少以下参数:【{missing_parameters}】")
        return False
    else:
        print(f"\n第【{index + 1}】个账号，URL包含所有必需的参数，开始执行脚本")
        return True


def QIANWEN(tongyiSysPromt, content, api_key):
    print('开始调用通义千问')
    # 检查dashscope库是否已安装
    dashscope = import_or_install('dashscope')
    if dashscope:
        dashscope.api_key = api_key
        response = dashscope.Generation.call(
            model='qwen-max',
            messages=[
                {"role": "system",
                 "content": tongyiSysPromt},
                {"role": "user", "content": content}],
            seed=1234,
            top_p=0.8,
            result_format='message',
            enable_search=False,
            max_tokens=1500,
            temperature=1.0,
            repetition_penalty=1.0,
        )
        if response.status_code == HTTPStatus.OK:
            # print(response)
            video_info = response.output['choices'][0]['message']['content']
            print('通义生成【成功】！')
            return video_info
        else:
            print(f"无法解析通义返回的信息:{response}")
            return None
    else:
        print('dashscope 模块无法导入，函数无法执行。')


# 取环境变量，并分割
def ENV_SPLIT(input_str):
    parts = []
    if '&' in input_str:
        amp_parts = input_str.split('&')
        for part in amp_parts:
            if '#' in part:
                hash_parts = part.split('#')
                for hash_part in hash_parts:
                    parts.append(hash_part)
            else:
                parts.append(part)
        # print(parts)
        return (parts)

    elif '#' in input_str:
        hash_parts = input_str.split('#')
        # print(hash_parts)
        return (hash_parts)
    else:
        out_str = str(input_str)
        # print([out_str])
        return ([out_str])


# 使用导入的模块进行验证码识别
def CAPCODE(captcha_slider, captcha_bg):
    ddddocr = import_or_install('ddddocr')
    if ddddocr:
        slide = ddddocr.DdddOcr(det=False, ocr=False)
        with open(captcha_slider, 'rb') as f:
            target_bytes = f.read()
        with open(captcha_bg, 'rb') as f:
            background_bytes = f.read()
        res = slide.slide_match(target_bytes, background_bytes, simple_target=True)
        # print(res['target'][0])
        # print(type(res['target'][0]))
        return res['target'][0]
    else:
        print('ddddocr 模块无法导入，函数无法执行。')
        return False


def BASE64_TO_IMG(base64_string, output_path):
    import base64
    import io
    Image = import_or_install('Pillow', 'PIL.Image')

    if Image:
        try:
            # 解码base64字符串
            image_data = base64.b64decode(base64_string)
            # 将字节数据转换为字节流
            image_buf = Image.open(io.BytesIO(image_data))
            # 转换为RGB模式
            image_buf = image_buf.convert('RGB')
            # 保存图片到指定路径
            image_buf.save(output_path, format='JPEG')
            return True
        except Exception as e:
            print(f'发生错误：{e}')
            return False
    else:
        print('需要的模块[PIL]无法导入，函数无法执行。')
        return False


def send_wxpusher(UID, one_msg, APP_NAME, help=False):
    WXPUSHER = os.environ.get('WXPUSHER', False)
    if WXPUSHER:
        if help:
            push_res = wxpusher(WXPUSHER, APP_NAME + '互助', one_msg, UID, TIPS_HTML)
        else:
            push_res = wxpusher(WXPUSHER, APP_NAME, one_msg, UID, TIPS_HTML)
        print(push_res)


def wxpusher(UID, msg, title, help=False):
    """利用 wxpusher 的 web api 发送 json 数据包，实现微信信息的发送"""
    WXPUSHER = os.environ.get('WXPUSHER', False)
    if WXPUSHER:
        if help: title = title + '互助'
        print('\n------开始wxpusher推送------')
        print(f'标题：【{title}】\n内容：{msg}')
        webapi = 'http://wxpusher.zjiecode.com/api/send/message'
        msg = msg.replace("\n", "<br>")
        tips = TIPS_HTML.replace("\n", "<br>")
        data = {
            "appToken": WXPUSHER,
            "content": f'{title}<br>{msg}<br>{tips}',
            # "summary": msg[:99],  # 该参数可选，默认为 msg 的前10个字符
            "summary": title,
            "contentType": 2,
            "uids": [UID],
            "url": "https://gj.cherwin.cn"
        }

        try:
            result = requests.post(url=webapi, json=data)
            result.raise_for_status()  # 对于非2xx状态码，抛出异常
            response_json = result.json()
            if response_json["success"]:
                return "------消息发送成功------\n"
            else:
                return f"消息发送失败。错误信息：{response_json['msg']}"
        except requests.exceptions.RequestException as e:
            return f"发送消息时发生错误：{str(e)}"
        except Exception as e:
            return f"发生意外错误：{str(e)}"


def RESTART_SCRIPT(RESTART_SCRIPT_NAME):
    python = sys.executable
    os.execl(python, RESTART_SCRIPT_NAME, *sys.argv[1:])


def CHECK():
    global CHERWIN_SCRIPT_CONFIG
    print('>>>>>>>开始获取版本信息...')
    baseurl = 'https://py.cherwin.cn/'
    TOOLS_NAME = 'CHERWIN_TOOLS.py'
    server_script_url = f'https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/{TOOLS_NAME}'
    try:
        response = requests.get(f'{baseurl}CHERWIN_SCRIPT_CONFIG.json', verify=False)
        response.encoding = 'utf-8'
        # 读取内容
        CHERWIN_SCRIPT_CONFIG = response.json()
        if 'code' in CHERWIN_SCRIPT_CONFIG:
            CHERWIN_SCRIPT_CONFIG = None
        server_version = CHERWIN_SCRIPT_CONFIG.get('TOOLS_VERSION', NOW_TOOLS_VERSION)
        if CHECK_UPDATE_NEW(NOW_TOOLS_VERSION, server_version, server_script_url, TOOLS_NAME):
            print('更新脚本完成')
            # print(f'重新检测[{TOOLS_NAME}]版本')
            return False
        else:
            return True
    except:
        print('获取CHERWIN_SCRIPT_CONFIG.json失败')
        return False


def main(APP_NAME, local_script_name, ENV_NAME, local_version):
    global APP_INFO, TIPS, TIPS_HTML
    git_url = f'https://github.com/CHERWING/CHERWIN_SCRIPTS/raw/main/{local_script_name}'
    if CHECK():
        APP_INFO = CHERWIN_SCRIPT_CONFIG.get("APP_CONFIG", {}).get(ENV_NAME, {})
        # print(APP_INFO)
        server_version = APP_INFO.get('NEW_VERSION', '')
        if CHECK_UPDATE_NEW(local_version, server_version, git_url, local_script_name, APP_NAME=APP_NAME):
            print('更新成功，请重新运行脚本！')

        if not APP_INFO.get('ENABLE', False):
            print('当前脚本未开放')
            exit()
        TIPS = APP_INFO.get('NTC', '') if APP_INFO.get('NTC', '') else CHERWIN_SCRIPT_CONFIG.get('GLOBAL_NTC', '')

        TIPS_HTML = APP_INFO.get('NTC', '') if APP_INFO.get('NTC', '') else CHERWIN_SCRIPT_CONFIG.get('GLOBAL_NTC_HTML',
                                                                                                      '')
        ENV = os.environ.get(ENV_NAME)
        AuthorCode = get_AuthorInviteCode(f'https://yhsh.ziyuand.cn/{ENV_NAME}_INVITE_CODE.json')

        return ENV, APP_INFO, TIPS, TIPS_HTML, AuthorCode
    else:
        exit()


if __name__ == '__main__':
    pass
