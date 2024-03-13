"""
created  by 吃GV个
没毛，没毛，买毛，一分钱也没有，大学生专用
抓包userapi.qiekj.com域名请求体里的token
变量名pgsh，格式 cookie，多账号用@
"""
import  requests
import  json
import os
import time
accounts = os.getenv('pgsh')
accounts_list = os.environ.get('pgsh').split('@')
num_of_accounts = len(accounts_list)
print(f"获取到 {num_of_accounts} 个账号")
for i, account in enumerate(accounts_list, start=1):
    token = account
    url="https://userapi.qiekj.com/task/completed"
    headers= {
        "Host": "userapi.qiekj.com",
        "Authorization": token,
        "Version": "1.35.0",
        "channel": "android_app",
        "content-length": "60",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
    }
    print(f"\n=======开始执行账号{i}=======")
    print(f"{'-' * 15}执行看广告{'-' * 15}") 
    for j in range(11):
      data=f"taskType=2&token={token}"
      response=requests.post(url,headers=headers,data=data).json()
      print(response)
      time.sleep(5)
      if response['data']== True:
        print(f"第{j+1}个任务成功")
      else:
        print("app广告任务完成")
        break
    for t in range(11):
      data=f"taskType=9&token={token}"
      response=requests.post(url,headers=headers,data=data).json()
      print(response)
      time.sleep(5)
      if response['data']==True:
        print(f"第{t+1}个任务成功")
      else:
        print("支付宝广告任务完成")
        break
    for y in range(6):
      data=f"taskType=3&token={token}"
      response=requests.post(url,headers=headers,data=data).json()
      print(response)
      time.sleep(5)
      if response['data']==True:
        print(f"第{y+1}个任务成功")
      else:
        break
    for u in range(6):
      data=f"taskType=6&token={token}"
      response=requests.post(url,headers=headers,data=data).json()
      print(response)
      time.sleep(10)
      if response['data']==True:
        print(f"第{u+1}个任务成功")
      else:
        break
    print(f"{'-' * 15}执行日常任务{'-' * 15}") 
    for h in range(1, 21):
      data1=f"taskType={h}&token={token}"
      response=requests.post(url,headers=headers,data=data1).json()
      print(response)
      if response['data']==True:
        print(f"第{h+1}个任务成功")
      time.sleep(3)
    print(f"{'-' * 15}执行浏览商品{'-' * 15}") 
    url="https://qemyapi.qiekj.com/api/search_item_list"
    headers= {
        "Host": "qemyapi.qiekj.com",
        "Authorization": token,
        "Version": "1.35.0",
        "channel": "android_app",
        "content-length": "60",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
    }
    data2=f"keyWord=%E9%98%B2%E6%99%92%E8%A1%A3&page=1&pageSize=20&token={token}"
    response=requests.post(url,headers=headers,data=data2).json()
    task_ids = [taskItem['item_id'] for taskItem in response['data']['data'][:6]]
    for task_id in task_ids:
      url = "https://userapi.qiekj.com/integralUmp/rewardIntegral"
      headers= {
        "Host": "userapi.qiekj.com",
        "Authorization": token,
        "Version": "1.35.0",
        "channel": "android_app",
        "content-length": "60",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9",
      }
      data3 = f"itemCode={task_id}&token={token}"
      response = requests.post(url, headers=headers, data=data3).json()
      if response['data'] is None:
        print("浏览完成")
        break
      else:
        score = response['data']['rewardIntegral']
        print(f"浏览商品获得{score}")
      time.sleep(2)
     