"""
项目名称 屈臣氏回馈金签到
入口：#小程序://屈臣氏/p4PXyRIEkAJccuw

要去掉authorization的Bearer     例如   Authorization: Bearer abcd。。13。B  只需要abcd。。13。B
变量：authorization#unionid#openid#备注（没有备注也可以）

变量名： qsccs
例如： export qsccs="abcd。。13。B#unionid#openid"
多账号   换行/回车   
脚本作者: QGh3amllamll  

------更新记录----  
1.1 测试版  连签七天没有先判断 下次更新判断签到7天


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
import random
enable_notification = 1   #0不发送通知   1发送通知


# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

jbxmmz = "屈臣氏回馈金"
jbxmbb = "1.1"
#---------简化的框架 0.5 带通知--------

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
    log("如果喜欢请打赏支持维护和开发    更要钱动力 来 更新/维护脚本")
    log("" * 10)
    log(f'这个是怎么东西？？？')
    log(f'U2FsdGVkX1/F371b27nTzUeMknDFjABXyQBHINWvVPRkUVoUe6ZdZ508DVGF7dMc')
    log("" * 10)
    log("" * 10)
    log(f'-----------{jbxmmz} {jbxmbb}-----------')


# 获取环境变量
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f'环境变量{var_name}未设置，请检查。')
        return None
    accounts = value.strip().split('\n')
    num_accounts = len(accounts)
    print(f'-----------本次账号运行数量：{num_accounts}-----------')
   
    print_disclaimer()
    return accounts


#-------------------------------封装请求-------------

base_url = "https://mystore-01api.watsonsvip.com.cn"
def create_headers(an, op_id, un_id):
    headers = {
        "Authorization": f"Bearer {an}",
        "Content-Type": "application/json",
        "authorizer-appid": "wx1ffbd6927043dff7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555",
        "openId": op_id,
        "unionId": un_id,

    }
    return headers

#-------------------------------封装请求---完成----------



def qcsqd(an, op_id, un_id):   # 签到
    urlqd = f"{base_url}/wx/signIn/iter/sign"
    headers = create_headers(an, op_id, un_id)
    body = json.dumps({"unionId": op_id, "isSorttion": False})

    try:
        response = requests.post(urlqd, headers=headers, data=body)
        response.raise_for_status()  # 确保请求成功
        response_data = response.json()
        
        if response_data.get("code") == 11000:  # 已经签到，也算签到成功
            print(f"签到提示：{response_data.get('errorMsg')}")
            return True  # 签到成功
        elif response_data.get("code") == 0:
            # 将奖励金额除以100来转换为元
            reward_amount = response_data['result'].get('rewardAmount', 0) / 100
            beauty_amount = response_data['result'].get('beautyAmount', 0) / 100
            print(f"签到成功：连续签到天数: {response_data['result'].get('continueDays')}, "
                  f"序列号: {response_data['result'].get('dailySignInCouponSerialNum')}, "
                  f"类型编号: {response_data['result'].get('typeNum')}, "
                  f"奖励金额: {reward_amount}, "  # 使用转换后的金额
                  f"美容金额: {beauty_amount}")  # 使用转换后的金额
            return True  # 签到成功
        elif response_data.get("code") == 1403:
            print("权限不足，数据过期/不正常退出账号。")
            return False  # 签到失败
        else:
            print("签到响应：", response_data)
            return False  # 签到失败
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
        return False  # 签到失败
    except Exception as err:
        print(f"请求异常：{err}")
        return False  # 签到失败

#                               任务判断        始        -------

def rwmwcid(an, op_id, un_id):  # 没有完成任务的ID，并返回任务ID列表
    url = f"{base_url}/cloudapi/v2/users/bubbles/filterNot/taskType/4"
    headers = create_headers(an, op_id, un_id)
    task_ids = []  # 初始化任务ID列表
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        response_data = response.json()
        
        if response_data.get("code") == 0:
            tasks = response_data.get("result", [])
            if not tasks:  
               # print("当前没有可用的任务或奖励。1️⃣跑个毛线脚本")
                #pass
                print()

            else:
                for task in tasks:
                    task_id = task.get("taskId")
                    task_ids.append(task_id)  
        else:
            print("响应内容：", response_data)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")
    return task_ids  # 返回任务ID列表

def pb_rwid(an, op_id, un_id, task_ids):  
    url = f"{base_url}/cloudapi/v2/users/tasks"
    headers = create_headers(an, op_id, un_id)
    print(f"任务ID列表：{task_ids}")
    task_ids_str = [str(id) for id in task_ids]  
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        response_data = response.json()

        if response_data.get("code") == 0:
            tasks = response_data['result'].get('list', [])
            categorized_tasks = {}
            for task in tasks:
                task_type = task.get('type')
                if task_type not in categorized_tasks:
                    categorized_tasks[task_type] = []
                categorized_tasks[task_type].append(task)

            for task_type, tasks_in_category in categorized_tasks.items():
                for task in tasks_in_category:
                    if str(task['id']) in task_ids_str:
                        print(f"准备执行任务：{task['name']} (ID: {task['id']})")
                        if task_type == 'Browse':
                            browse(an, op_id, un_id, task['id'])
                        elif task_type in ['Jump', 'Subscribe']:
                            jumprw(an, op_id, un_id, task['id'])
                        #print(f"任务完成：{task['name']} (ID: {task['id']})")
        else:
            print("响应内容：", response_data)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

#                               任务判断        完        -------

#                       提交任务        始        -------
def jumprw(an, op_id, un_id, task_id):  # 跳转/订阅类任务
    url = f"{base_url}/cloudapi/v2/users/tasks/complete"
    headers = create_headers(an, op_id, un_id)
    data = {"taskId": task_id}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        
        
        if response_data.get("code") == 0:
            print(f"任务 {task_id} 完成成功。")
        elif response_data.get("code") == 11000:
       
            print(f"任务 {task_id} 完成失败，原因：{response_data.get('errorMsg')}")
        else:
        
            print("响应内容：", response_data)

       
        sleep_time = random.randint(1, 3)
        #print(f"暂停 {sleep_time} 秒...")
        time.sleep(sleep_time)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def browse(an, op_id, un_id, task_id):  # 执行浏览任务并提交数据
    browse_url = f"{base_url}/cloudapi/v2/users/tasks/browserTask/token/{task_id}"
    complete_url = f"{base_url}/cloudapi/v2/users/tasks/complete"
    headers = create_headers(an, op_id, un_id)
    #print(browse_url)

    try:
        # 获取浏览任务的令牌
        browse_response = requests.get(browse_url, headers=headers)
        browse_response.raise_for_status()
        browse_result = browse_response.json()
        token = browse_result.get('result', {}).get('token')

        if not token:
            print("未获取到有效的token")
            return None

        # 暂停10-13秒模拟浏览
        time.sleep(random.randint(11, 13))

        # 提交浏览任务数据
        payload = json.dumps({
            "taskId": str(task_id),
            "completeBrowserTaskToken": token
        })
        complete_response = requests.post(complete_url, headers=headers, data=payload)
        complete_response.raise_for_status()

        # 解析响应数据
        complete_data = complete_response.json()
        if complete_data.get('code') == 0:
            # 处理成功的请求
            amount = complete_data['result'][0]['amount']
            print(f"任务完成，奖励金额为：{amount}")
        elif complete_data.get('code') == 11000:
            # 处理重复的请求
            print(f"错误信息：{complete_data['errorMsg']}")
        else:
            # 处理其他错误
            print(f"未知错误，错误代码：{complete_data.get('code')}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

#                       提交任务        完        -------

#                 奖励        始        -------
def hq_jlid(an, op_id, un_id):  # 获取没有领取奖励ID
    url = f"{base_url}/cloudapi/v2/users/bubbles/filterNot/taskType/4"
    headers = create_headers(an, op_id, un_id)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        response_data = response.json()
        
        if response_data.get("code") == 0:
            tasks = response_data.get("result", [])
            if not tasks:  
                print("当前没有可用的任务或奖励。1️⃣跑个毛线脚本")
            else:
                for task in tasks:
                    task_id = task.get("taskId")
                    task_name = task.get("taskName")
                    prize = task.get("prize")
                    prize_id = task.get("prizeId")
                    
                    
                    #print(f"任务ID: {task_id}, 任务名称: {task_name}, 奖励: {prize}")
                    print(f"任务ID: {task_id}, 奖励: {prize}")

                    tjjl(an, op_id, un_id, prize_id)
                    
        else:
            print("响应内容：", response_data)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def tjjl(an, op_id, un_id, prize_id):
    url = f"{base_url}/cloudapi/v2/users/receive"
    headers = create_headers(an, op_id, un_id)
    data = {"prizeId": prize_id}
    
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        
        if response_data.get("code") == 0:
            
            amount = response_data.get("result", {}).get("amount", "0")
            prize_biz_param = json.loads(response_data.get("result", {}).get("prizeBizParam", "{}"))
            sub_play_name = prize_biz_param.get("subPlayName", "Unknown")
            
            
            amount_in_yuan = float(amount) / 100
            print(f"奖励领取成功，金额: {amount_in_yuan}元")

            
            sleep_time = random.randint(10, 13)
            print(f"暂停 {sleep_time} 秒...")
            time.sleep(sleep_time)

        else:
         
            print("响应内容：", response_data)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

#                 奖励        完        -------

def xc_ye(an, op_id, un_id):#查询余额
    url = f"{base_url}/wx/signIn/index?unionId={un_id}"
    headers = create_headers(an, op_id, un_id)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        response_data = response.json()
        

        if response_data.get("code") == 0:
            amount = response_data['result']['amount'] / 100
            print(f"回馈金余额：{amount}元")  
            
           
            for welfare in response_data['result'].get('oldUserSignInWelfareList', []):
                if 'couponName' in welfare:
                    coupon_name = welfare['couponName']
                    print(f"优惠券：{coupon_name}")
        else:
            
            print("请求未成功，完整响应内容：", response_data)
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")


def sign_in(an, op_id, un_id):
    url = f"{base_url}/signIn/turntable/lotteryDraw"
    headers = create_headers(an, op_id, un_id)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 确保请求成功
        response_data = response.json()
        
        if response_data.get("code") == 11000:  # 特定条件
            print(f"提示信息：{response_data.get('errorMsg')}")
        else:
            print("连签七天响应：", response_data)
            
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
    var_name = 'qsccs'
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
        if len(parts) < 3:
            print("令牌格式不正确。跳过处理。")
            continue

        an = parts[0]  
        un_id = parts[1] 
        op_id = parts[2]  
        account_no = parts[3] if len(parts) > 3 else ""  # 备注信息
        print(f'------账号 {i+1}/{total_accounts} {account_no} -------')
        sign_in_success = qcsqd(an, op_id, un_id)  # 签到并获取签到是否成功的状态
        if not sign_in_success:
            print("由于签到失败，跳过此账号的后续操作。")
            continue  # 跳过当前循环的剩余部分，直接处理下一个账号
        #qcsqd(an, op_id, un_id)#签到
        sign_in(an, op_id, un_id)#连签七天
        task_ids = rwmwcid(an, op_id, un_id)  # 没有完成   任务ID列表
        pb_rwid(an, op_id, un_id, task_ids)  # 匹配  任务ID 执行任务

        hq_jlid(an, op_id, un_id)#领取奖励/判断任务是不是完成
        xc_ye(an, op_id, un_id)#查询余额
       
    

    sys.stdout = original_stdout
    output_content = captured_output.getvalue()
    captured_output.close()


    if enable_notification == 1:
        try:
            send("通知", output_content)  # 尝试发送通知
            print("通知已发送。输出内容为：")
            #print(output_content)
        except NameError:
            print("通知发送失败，send函数未定义。")



if __name__ == "__main__":
    main()     
