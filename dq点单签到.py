"""
变量： 手机号码
变量名： dqqdck
例如 export dqqdck='1380013800#备注
多账号   换行/回车   
脚本作者: QGh3amllamll  
版本 1.0
------更新记录----  
1.0 测试版


"""
import os
import requests
from datetime import datetime, timezone, timedelta
import json
import time
import io
import sys
import requests
import base64

enable_notification = 1   #0不发送通知   1发送通知


# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

#---------简化的框架 0.41 带通知--------

import sys
import os
def get_python_version():
    version = "python" + ".".join(str(i) for i in sys.version_info[:2])
    return version

# 使用函数获取Python版本并打印
PYTHON_VERSION = get_python_version()
print("本程序只支持在Python 3.10环境下运行。当前Python版本:", PYTHON_VERSION)
print()


enable_notification = 1   #0不发送通知   1发送通知
# 获取北京日期的函数
def get_beijing_date():  
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time.date()

def dq_time():
    # 获取当前时间戳
    dqsj = int(time.time())

    # 将时间戳转换为可读的时间格式
    dysj = datetime.fromtimestamp(dqsj).strftime('%Y-%m-%d %H:%M:%S')
    #print("当前时间戳:", dqsj)
    #print("转换后的时间:", dysj)

    return dqsj, dysj

def log(message):
    print(message)

def print_disclaimer():
    log("📢 请认真阅读以下声明")
    log("      【免责声明】         ")
    log("✨ 脚本及其中涉及的任何解密分析程序，仅用于测试和学习研究")
    log("✨ 禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断")
    log("✨ 禁止任何公众号、自媒体进行任何形式的转载、发布")
    log("✨ 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害")
    log("✨ 脚本文件请在下载试用后24小时内自行删除")
    log("✨ 脚本文件如有不慎被破解或修改由破解或修改者承担")
    log("✨ 如不接受此条款请立即删除脚本文件")
    log("" * 10)
    log(f'-----------DQ 签到  1.0-----------')
    log(	" .....................阿弥陀佛.......................")
    log(	"                       _oo0oo_                      ")
    log(	"                      o8888888o                     ")
    log(	'                      88" . "88                     ')
    log(	"                      (| -_- |)                     ")
    log(	"                      0\\  =  /0                    ")
    log(	"                   ___/‘---’\\___                   ")
    log(	"                  .' \\|       |/ '.                ")
    log(	"                 / \\\\|||  :  |||// \\             ")  
    log(	"                / _||||| -卍-|||||_ \\              ")
    log(	"               |   | \\\\\\  -  /// |   |           ")  
    log(	"               | \\_|  ''\\---/''  |_/ |            ") 
    log(	"               \\  .-\\__  '-'  ___/-. /            ") 
    log(	"             ___'. .'  /--.--\\  '. .'___           ")
    log(	"         ."" ‘<  ‘.___\\_<|>_/___.’>’ "".           ")
    log(	"       | | :  ‘- \\‘.;‘\\ _ /’;.’/ - ’ : | |        ")
    log(	"         \\  \\ ‘_.   \\_ __\\ /__ _/   .-’ /  /    ")   
    log(	"    =====‘-.____‘.___ \\_____/___.-’___.-’=====     ")
    log(	"                       ‘=---=’                      ")
    log(	"                                                    ")
    log(	"...................佛祖保佑 ,永无BUG.................")
    log(f'-----------DQ 签到  1.0-----------')


# 获取环境变量
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f'环境变量{var_name}未设置，请检查。')
        return None
    accounts = value.strip().split('\n')
    num_accounts = len(accounts)
    print(f'-----------本次账号运行数量：{num_accounts}-----------')
    #print(f'-----------DQ 签到  1.0-----------')
    print_disclaimer()
    return accounts


#-------------------------------封装请求-------------


def create_headers(new_session):
    headers = {       
        "accept": "application/json, text/plain, */*",
        "content-length": "2",
        "channel": "311",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555",
        "tenant": "1",
        "content-type": "application/json;charset=UTF-8",
        "host": "wechat.dairyqueen.com.cn",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": f"SESSION={new_session}"  
    }
    return headers


#-------------------------------封装请求---完成----------




def tjhmhqsign(hm):  #提交号码   获取sign    1
    url = "https://wxxcx.dairyqueen.com.cn/UserXueLi?_actionName=getXueLiSign&serviceId=4&actionId=9&key=30274185e983a6c6"
    headers = {
        'host': 'wxxcx.dairyqueen.com.cn',
        'content-length': '99',
        'xweb_xhr': '1',
        #'cookie': 'JSESSIONID=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555',
        'content-type': 'application/json',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx22e5ce7c766b4b78/131/page-frame.html',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
    } 
    current_timestamp = int(time.time() * 1000)  # 动态生成时间戳
    payload = {
        "content": {
            "bindingAccount": hm,  # 动态传入的手机号码或账号
            "tenantId": 1,
            "channelId": 311,
            "timestamp": current_timestamp
        }
    }
    #print("获取学力成功：", payload)
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # 确保请求成功
        
        # 解析响应体中的JSON数据
        response_data = response.json()
        #print("获取学力成功：", response_data)
        
        # 从响应数据中提取 sign
        sign = response_data.get('data', {}).get('sign')
        # 从响应头中获取 JSESSIONID
        cookid = response.cookies.get('JSESSIONID')
        
        return sign, cookid, current_timestamp  # 返回包含时间戳的元组
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

    return None, None, None



def tj_signhqck(hm, sign, cookid, current_timestamp):  # 提交sign 获取Cookie  2
    url = "https://wechat.dairyqueen.com.cn/loginNoLandfall"
    jsessionid_base64 = base64.b64encode(cookid.encode()).decode()
   
    payload = {
        "bindingAccount": hm,
        "tenantId": "1",
        "channelId": "311",
        "timestamp": current_timestamp,
        "sign": sign
    }
    #print("Payload:", payload)
    headers = {
        "channel": "311",
        "tenant": "1",
        "origin": "https://wechat.dairyqueen.com.cn",
        "x-requested-with": "com.tencent.mm",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "content-type": "application/json;charset=UTF-8",
        "referer": f"https://wechat.dairyqueen.com.cn/webview/dq/index.html?bindingAccount={hm}&tenantId=1&channelId=311&timestamp={current_timestamp}&sign={sign}",
        "accept-encoding": "gzip, deflate",
        "Cookie": f"SESSION={jsessionid_base64}"
    }
    #print("Headers:", headers)

    response = requests.post(url, headers=headers, json=payload)
    #print("响应头:", response.headers)
    
 
    new_session = None
    set_cookie_header = response.headers.get('Set-Cookie')
    if set_cookie_header and "SESSION=" in set_cookie_header:
        for part in set_cookie_header.split(';'):
            if part.strip().startswith("SESSION="):
                new_session = part.strip().split('=')[1]
                break
    #print("新的 SESSION 值:", new_session)

    try:
        response.raise_for_status()  
        response_data = response.json()  
        #print("登录操作成功：", response_data)
        return response_data, new_session  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")
    return None, new_session  



def sign_in(new_session):#执行签到操作

    url = "https://wechat.dairyqueen.com.cn/memSignIn/signIn"
    headers = create_headers(new_session)  
    try:
        response = requests.post(url, headers=headers, json={})
        response.raise_for_status()  
        response_data = response.json()
        if response_data.get('code') == 200:
            print("成功签到")
        elif response_data.get('code') == 11028:
            print(response_data.get('message'))
        else:
            print("响应内容：", response_data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def xz(new_session):
    url = "https://wechat.dairyqueen.com.cn/member/info"
    headers = create_headers(new_session)  
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        response_data = response.json()
        if response_data.get('code') == 200:
           
            group_points = response_data.get('data', {}).get('groupPoints')
            print("我的积分：", group_points)
        else:
            
            print("响应体：", response_data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

#本地测试用 
os.environ['cscs'] = '''


'''



class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()

    def flush(self):
        for file in self.files:
            file.flush()

def main():
    var_name = 'dqqdck'
    tokens = get_env_variable(var_name)
    if not tokens:
        print(f'环境变量{var_name}未设置，请检查。')
        return

    captured_output = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = Tee(sys.stdout, captured_output)

    total_accounts = len(tokens)

    for i, token in enumerate(tokens):
        parts = token.split('#')
        if len(parts) < 1:
            print("令牌格式不正确。跳过处理。")
            continue

        hm = parts[0]  
        account_no = parts[1] if len(parts) > 1 else ""  # 备注信息
        print(f'------账号 {i+1}/{total_accounts} {account_no} -------')

        sign, cookid, current_timestamp = tjhmhqsign(hm)
        if sign and cookid and current_timestamp:
            response_data, new_session = tj_signhqck(hm, sign, cookid, current_timestamp)
            if new_session:  
                sign_in(new_session)  
                xz(new_session)
            else:
                print("未能获取新的SESSION值")
        else:
            print("手机号码获取sign失败")

    sys.stdout = original_stdout
    output_content = captured_output.getvalue()
    captured_output.close()


    if enable_notification == 1:
        send("dq点单签到 通知", output_content)  
        #print("通知已发送。输出内容为：")
        #print(output_content)

if __name__ == "__main__":
    main()