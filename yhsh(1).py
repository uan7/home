#'' 
#new Env('永辉生活');
#抓任意域名的deviceid和access_token(有bug及时反馈)，多帐号换行，变量yhsh
#果园任务七点之后才刷新
#2.11 4:35(修复浇水任务完整执行跳过)
#2.14 16:00(增加会员成长值任务和推送)
#'''
import requests
import time
import os

# 控制是否启用变量
enable_notification = 1  # 0不发送通知   1发送通知

# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

def send_notification(title, content):
    if enable_notification == 1:
        send(title, content)

def member(device_id, access_token):
    timestamp = str(int(time.time() * 1000))
    url = f"https://api.yonghuivip.com/web/coupon/signreward/sign?timestamp={timestamp}&channel=ios&platform=ios&v=10.1.0.6&app_version=10.1.0.6&sellerid=&channelSub=&jysessionid=8eba2fe1-ea26-4a83-98ab-72992f390e44&brand=iPhone&model=iPhone%206s%20(A1633%2FA1688%2FA1691%2FA1700)&os=ios&osVersion=15.7.9&networkType=WIFI&screen=375*667&productLine=YhStore&appType=h5&cityid=11&deviceid={device_id}&shopid=9637&memberid=242976506184457885&access_token={access_token}"
    headers = {
        "Host": "api.yonghuivip.com",
        "Connection": "keep-alive",
        "Content-Length": "64",
        "X-YH-Biz-Params": "ncjkdy=,'+(&nzggzmdy=(&xdotdy=--&gib=--,0(-$,&gvo=+\$0_+)*,+&vkkdy=yKWHqna(DlqXsuHhk",
        "Accept": "application/json",
        "X-YH-Context": "origin=h5&morse=1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/10.1.0(client/phone; iOS 15.7.9; iPhone8,1)",
        "Content-Type": "application/json",
        "Origin": "https://m.yonghuivip.com",
        "X-Requested-With": "cn.yonghui.hyd",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://m.yonghuivip.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    data = {
        "memberId": "962892903519470906",
        "shopId": "9637",
        "missionid": 39
    }
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    code = response_data["code"]
    if code == 0:
        credit = response_data["data"]["signrewardvo"]["credit"]
        return f"首页签到任务：恭喜获得{credit}积分"
    else:
        message = response_data["message"]
        return f"首页签到任务：{message}"

def membertask(device_id, access_token):
    timestamp = str(int(time.time() * 1000))
    url = f"https://api.yonghuivip.com/web/member/task/doTask?timestamp={timestamp}&channel=ios&platform=ios&v=10.1.0.6&app_version=10.1.0.6&sellerid=7&channelSub=&jysessionid=8eba2fe1-ea26-4a83-98ab-72992f390e44&brand=iPhone&model=iPhone%206s%20(A1633%2FA1688%2FA1691%2FA1700)&os=ios&osVersion=15.7.9&networkType=WIFI&screen=375*667&productLine=YhStore&appType=h5&cityid=14&deviceid={device_id}&shopid=95DN&memberid=242976506184457885&access_token={access_token}"
    headers = {
        "Host": "api.yonghuivip.com",
        "Connection": "keep-alive",
        "Content-Length": "53",
        "X-YH-Biz-Params": "ncjkdy=,'+(&nzggzmdy=(&xdotdy=--&gib=--,0(-$,&gvo=+\$0_+)*,+&vkkdy=yKWHqna(DlqXsuHhk",
        "Accept": "application/json",
        "X-YH-Context": "origin=h5&morse=1",
        "X-YH-Biz-Params": "ncjkdy=,*HR&nzggzmdy=(&xdotdy=-!&gib=--)0-*$_'-+!)+*$-!&gvo=_!0!)$(!*($_+*$++",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/10.1.0(client/phone; iOS 15.7.9; iPhone8,1)",
        "Content-Type": "application/json",
        "Origin": "yhwebcachehttps://m.yonghuivip.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    data = {
        "taskId": "813",
        "shopId": "95DN",
        "taskCode": "2yue-HYRW"
    }
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    code = response_data["code"]
    if code == 0:
        data = response_data["data"]
        if isinstance(data, int):
            credit = data
        else:
            credit = data["data"]
        return f"成长值任务：恭喜获得{credit}成长值"
    else:
        message = response_data["message"]
        return f"成长值任务：{message}"

def flow(device_id, access_token):
    timestamp = str(int(time.time() * 1000))
    url = f"https://activity.yonghuivip.com/api/web/flow/farm/doTask?timestamp={timestamp}&channel=ios&platform=ios&v=10.1.0.6&sellerid=&deviceid={device_id}&shopid=9637&memberid=242976506184457885&app_version=10.1.0.6&channelSub=&brand=iPhone&model=iPhone%206s%20(A1633%2FA1688%2FA1691%2FA1700)&os=ios&osVersion=15.7.9&networkType=WIFI&screen=375*667&productLine=YhStore&appType=h5&access_token={access_token}"
    headers = {
        "X-YH-Biz-Params": "xdotdy=--&gib=--,0(-$,&gvo=+\$0_+)*,+",
        "X-YH-Context": "origin=h5&morse=1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/10.1.0(client/phone; iOS 15.7.9; iPhone8,1)",
        "Content-Type": "application/json",
        "Origin": "https://m.yonghuivip.com",
        "X-Requested-With": "cn.yonghui.hyd",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://m.yonghuivip.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    payload = {
        "taskType": "sign",
        "activityCode": "HXNC-QG",
        "shopId": "",
        "channel": ""
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    sign = response_data["data"]["signText"]
    return f"果园签到结果:{sign}"

def watering(device_id, access_token):
    results = []  # 存储执行结果的列表
    while True:
        timestamp = str(int(time.time() * 1000))
        url = f"https://activity.yonghuivip.com/api/web/flow/farm/watering?timestamp={timestamp}&channel=ios&platform=ios&v=10.1.0.6&sellerid=&deviceid={device_id}&shopid=9637&memberid=242976506184457885&app_version=10.1.0.6&channelSub=&brand=iPhone&model=iPhone%206s%20(A1633%2FA1688%2FA1691%2FA1700)&os=ios&osVersion=15.7.9&networkType=WIFI&screen=375*667&productLine=YhStore&appType=h5&access_token={access_token}"
        headers = {
            "Host": "activity.yonghuivip.com",
            "Connection": "keep-alive",
            "Content-Length": "87",
            "X-YH-Biz-Params": "xdotdy=--&gib=--,0(-$,&gvo=+\\$0_+)*,+",
            "Accept": "application/json",
            "X-YH-Context": "origin=h5&morse=1",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YhStore/10.1.0(client/phone; iOS 15.7.9; iPhone8,1)",
            "Content-Type": "application/json",
            "Origin": "https://m.yonghuivip.com",
            "X-Requested-With": "cn.yonghui.hyd",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://m.yonghuivip.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        data = {
            "activityCode": "HXNC-QG",
            "shopId": "",
            "channel": "",
            "inviteTicket": "",
            "inviteShopId": ""
        }
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        if response_data and "code" in response_data:
            code = response_data["code"]
            message = response_data.get("message", "")

            if code == 0:
                ladder_text = response_data["data"].get("ladderText", "")
                result = f"果园浇水结果: {ladder_text}"
                results.append(result)  # 将结果添加到列表中
                print(result)
            else:
                result = f"果园浇水失败: {message}"
                results.append(result)  # 将结果添加到列表中
                print(result)
                break
        else:
            result = "果园浇水失败: 无法解析响应数据"
            results.append(result)  # 将结果添加到列表中
            print(result)
            break

    # 返回结果列表
    return results

def main():
    tokens_str = os.environ.get('yhsh')
    if not tokens_str:
        print("请设置环境变量yhsh")
        return
    notifications = []  # 存储每个设备的执行结果
    token_pairs = tokens_str.split('\n')
    for idx, pair in enumerate(token_pairs, start=1):
        device_id, access_token = pair.split('&')
        member_result = member(device_id, access_token)
        membertask_result = membertask(device_id, access_token)
        flow_result = flow(device_id, access_token)
        #wateringtask_result=wateringtask(device_id, access_token)
        watering_results = watering(device_id, access_token)
        # 整合每个设备的执行结果
        device_notification = f"帐号{idx}\n{member_result}\n{membertask_result}\n{flow_result}\n"
        device_notification += "\n".join(watering_results)
        notifications.append(device_notification)
    # 将所有设备的执行结果发送通知
    summary_notification = "\n\n".join(notifications)
    # 去掉括号并每次循环执行结果换行
    summary_notification = summary_notification.replace("[", "").replace("]", "").replace(", ", "\n")
    # 保留单引号
    summary_notification = summary_notification.replace("'", "\\'")
    summary_notification += "\n🎉🎉🎉🎉🎉🎉🎉\n\n"  # 添加一个换行符
    send("永辉生活任务执行汇总", summary_notification) # 调用notify.py中的send函数发送通知
if __name__ == "__main__":
    print(">>>>>开始执行所有任务<<<<<")
    main()
    print(">>>>>所有任务执行结束<<<<<")
