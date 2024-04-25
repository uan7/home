"""
项目名称 smart汽车+
变量 sadi#saui#请求体
变量 sadi#saui#请求体#备注  可以增加备注
变量名 smartCK
多账号   换行/回车
脚本作者: QGh3amllamll 版本2.0

搜api/smart/web/1.0/oauth/miniapp/quicklogin
全部请求体
{"gbk":"dpe...=","encryptedData":"WVT...==","openid":"oWAvd5.....","unionid":"oiRgW6lL4TtwjaTUwc85rgfa-cms","tongdun_token":"Pb..jV9","extras":{"checkBinding":true}}

例如：
sadi#saui#{"gbk":"dpe...=","encryptedData":"WVT...==","openid":"oWAvd5.....","unionid":"oiRgW6lL4TtwjaTUwc85rgfa-cms","tongdun_token":"Pb..jV9","extras":{"checkBinding":true}}


saui不在一起   任意找一个
---------------------更新说明----------
1.1版本更新  获取token数据的 UTC时间
时间2013.11.19.21
1.2版本更新  打印信息  时间2023.11.20.1:30
1.3版本 更新  通知  重写打印 2023年11月28日01:33:28
1.4版本  更新  30天开宝箱   重写发送通知  2023.12.18 01点
2.0版本    重写代码    2023.12.18 02点
"""
import os
import requests
from datetime import datetime, timezone, timedelta
import json
import time
import random
import sys
from io import StringIO
# 控制变量，用于控制是否发送通知
enable_notification = 1    #0 不发送     1发送通知

# 如果需要发送通知，则尝试导入notify模块
if enable_notification:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。程序将退出。")
        sys.exit(1)

#---------简化的框架0.4--------
# 配置参数
#base_url = "https://hxxxy.gov.cn"  # 已修改为实际的基础URL
user_agent = "Mozilla/5.0 (Linux; Android 11; ONEPLUS A6000 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/1110005 MMWEBSDK/20230405 MMWEBID/2930 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android"

def get_time_info(format="beijing", timestamp_required=False, year_month_only=False):
    if format == "beijing":
        current_time = datetime.now(timezone(timedelta(hours=8)))
    elif format == "utc":
        current_time = datetime.now(timezone.utc)
    else:
        raise ValueError("不支持的时间格式")

    if year_month_only:
        return current_time.strftime('%Y-%m')

    formatted_time = current_time.strftime('%Y%m%dT%H%M%SZ')
    date_only = current_time.date()
    timestamp = int(current_time.timestamp())

    if timestamp_required:
        return formatted_time, timestamp
    else:
        return formatted_time, date_only


# 获取环境变量
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f'环境变量{var_name}未设置，请检查。')
        return None
    accounts = value.strip().split('\n')
    num_accounts = len(accounts)
    print(f'-----------本次账号运行数量：{num_accounts}-----------')
    print(f'-----------项目 smart汽车  -----------')
    return accounts

# 封装请求头
def create_headers(id_token):

    headers = {
        "X-Channel-Id": "smartapp",
        "Accept": "application/json, text/plain, */*",
        "X-Auth-Token": id_token,
        "User-Agent": user_agent,
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://app-obs-prod.smart.cn",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://app-obs-prod.smart.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    return headers



def hqtoken(sadi, user_agent, json_body):  # 获取userId和token
    try:
        # 获取x-sdk-date
        x_sdk_date, _ = get_time_info(format="beijing")

        url = "https://cms-api.smart.cn/api/smart/web/1.0/oauth/miniapp/quicklogin"
        headers = {
            "charset": "utf-8",
            "sadi": sadi,
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip,compress,br,deflate",
            "token-time": "[object Undefined]",
            "api-key": "90c5f74cb2214ea6927d02addf8333d9",
            "x-channel-id": "wechat-applet",
            "content-type": "application/json",
            "x-sdk-date": x_sdk_date,
            "Referer": "https://servicewechat.com/wx7268531cd0569eb5/78/page-frame.html"
        }

        # 将字符串格式的请求体转换为JSON对象
        payload = json.loads(json_body)

        # 发送请求
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()

        # 提取 userId 和 id_token
        userId = response_data['result'].get('userId')
        id_token = response_data['result'].get('id_token')

        # 打印userId和id_token以供调试
        #print(f"userId: {userId}, id_token: {id_token}")

        return userId, id_token

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None, None

def sign_in(sadi, saui, user_agent, userId, id_token):  # 签到操作
    try:
        # 使用合并后的函数获取北京时间的格式化字符串和时间戳
        formatted_time, timestamp = get_time_info(format="beijing", timestamp_required=True)
        url = "https://app-api.smart.cn/smartapp-me/signs/v2"
        # 设置请求头
        headers = {
            "charset": "utf-8",
            "sadi": sadi,
            "User-Agent": user_agent,
            "x-user-id": userId,
            "Accept-Encoding": "gzip,compress,br,deflate",
            "id-token": id_token,
            "token-time": str(timestamp),  # 使用时间戳
            "x-auth-token": id_token,
            "saui": saui,
            "x-channel-id": "wechat-applet",
            "content-type": "application/json",
            "x-sdk-date": formatted_time,  # 使用格式化的北京时间
            "Referer": "https://servicewechat.com/wx7268531cd0569eb5/78/page-frame.html"
        }
        #print("签到操作时间戳, token-time:", str(timestamp), "x-sdk-date:", formatted_time)

        response = requests.post(url, headers=headers, json={})  # 发送请求

        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('code') == 'err.userprofile.duplicate.sign':
                print("签到结果", response_json.get('message'))
            elif response_json.get('code') == 'success':
                #print("签到成功:", response_json)
                # 提取特定信息并打印
                sign_count = response_json['data']['signCount']
                prize_content = response_json['data']['signPrize']['prizeContent']
                total_integral = response_json['data']['totalIntegral']
                print(f"签到结果: 签到天数 {sign_count}，今日积分 {prize_content}，积分总数 {total_integral}")
            else:
                print("签到状态未知", response_json)

            return response_json
        else:
            print("签到失败, 状态码:", response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def qdts(id_token):  # 获取用户的宝箱签到天数 信息。
    url = "https://app-api.smart.cn/smartapp-me/signs/next-prize"
    headers = create_headers(id_token)

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            # print("获取用户的签到天数信息-响应:", response_data)

            sign_count_by_current_prize = response_data['data']['signCountByCurrentPrize']
            left_count = response_data['data']['leftCount']

            print(f"开宝箱30/{sign_count_by_current_prize}天数 还需要签到:{left_count}")
            if sign_count_by_current_prize == 0 and left_count == 30:
                ljpid(id_token)
            return sign_count_by_current_prize, left_count

        else:
            print(f"获取签到天数失败，状态码: {response.status_code}")
            return None, None
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return None, None

def ljpid(id_token):  # 获得30天奖品id
    url = "https://app-api.smart.cn/smartapp-me/signs/v2/prize-records"
    headers = create_headers(id_token)
    request_body = {
        "pageSize": 999,
        "status": 1
    }   
    try:
        response = requests.post(url, headers=headers, json=request_body)

        # 处理响应
        if response.status_code == 200:
            response_data = response.json()
            # print("获得30天奖品id-响应:", response_data)

            if response_data['code'] == 'success':
                # 检查是否有有效的数据
                if response_data['data']:
                    # 处理 data 中的奖品信息
                    for prize in response_data['data']:
                        # 根据需要处理每个奖品的信息
                        print("奖品Code:", prize['prizeCode'])  # 正确提取prizeCode
                        kbx(prize['prizeCode'], id_token)  # 传递prize_code和id_token
                    return response_data['data']
                else:
                    print("没有返回有效的奖品数据。")
                    return None
            else:
                print("请求未成功，消息:", response_data['message'])
                return None
        else:
            print(f"获取奖品ID失败，状态码: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def kbx(prize_code, id_token):  # 开30天宝箱
    url = "https://app-api.smart.cn/smartapp-me/signs/v2/prize-receive"
    headers = create_headers(id_token)
    request_body = {"prizeCode": prize_code}

    try:
        response = requests.post(url, headers=headers, json=request_body)
        if response.status_code == 200:
            response_json = response.json()
            print("开30天宝箱:", response_json)  # 打印完整的响应JSON

            # 检查code是否为success
            if response_json.get('code') == 'success':
                # 提取并打印prizeContent和prizeType
                prize_content = response_json.get('data', {}).get('prizeContent')
                prize_type = response_json.get('data', {}).get('prizeType')

                print("奖励内容:", prize_content, "奖励类型:", prize_type)
                

                return True, response_json  # 返回操作成功的标识和响应数据
            else:
                print("操作失败，code不是success")
                return False, None  # 返回操作失败的标识和空数据
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return False, None  # 返回操作失败的标识和空数据
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return False, None  # 返回操作失败的标识和空数据

#本地测试用 sadi#saui#请求体
os.environ['cscs'] = '''

'''



class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()  # 确保及时输出

    def flush(self):
        for file in self.files:
            file.flush()

# 保存原始stdout
original_stdout = sys.stdout


# 主函数 sadi#saui#请求体

def main():
    # 创建一个StringIO对象来捕获输出
    string_io = StringIO()
    sys.stdout = Tee(sys.stdout, string_io)

    var_name = 'smartCK'
    tokens = get_env_variable(var_name)
    if not tokens:
        print(f'环境变量{var_name}未设置，请检查。')
        return
    try:
        # 这里是主要的逻辑代码

        for index, token in enumerate(tokens, start=1):
            parts = token.split('#')
            if len(parts) < 3:
                print("令牌格式不正确。跳过处理。")
                continue

            sadi = parts[0]
            saui = parts[1]
            json_body = parts[2]
            remark = parts[3] if len(parts) > 3 else ""

            # 使用hqtoken函数获取userId和id_token
            userId, id_token = hqtoken(sadi, user_agent, json_body)#获取userId和id_token
            if userId and id_token:
                print(f"--------账号{index}/{len(tokens)}--{remark}----")
                sign_in(sadi, saui, user_agent, userId, id_token) #签到
                qdts(id_token)  #获取用户的签到天数信息
                #ljpid(id_token)  # 获得30天奖品id  测试完要删除
                
            else:
                print("未能获取userId和id_token")

            # 随机停止一段时间（10-30秒）
            account_sleep_duration = random.randint(3, 6)
            #print(f"账号 {index} 休息时间：{account_sleep_duration} 秒")
            time.sleep(account_sleep_duration)    




    finally:
        # 恢复原始stdout
        sys.stdout = original_stdout
        output_content = string_io.getvalue()  # 获取捕获的输出内容
        if enable_notification:
            try:
                from notify import send
                send("smart汽车通知-jie", output_content)  # 发送通知
            except ModuleNotFoundError:
                print("通知模块未找到。")

if __name__ == "__main__":
    main()