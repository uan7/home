# -*- coding:utf-8 -*-
'''
cron: 20 10 */7 * *
new Env('禁用重复任务');
'''
 
import json
import os, sys
import requests
import time
 
ip="localhost"
//填写你要保留的脚本的前缀
substr="cdle_carry" 
 
def loadSend():
    print("加载推送功能")
    global send
    send = None
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/sendNotify.py"):
        try:
            from sendNotify import send
        except Exception as e:
            send = None
            print("加载通知服务失败~",e)
 
headers={
    "Accept":        "application/json",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
}
 
def getTaskList():
    t = round(time.time() * 1000)
    url = "http://%s:5700/api/crons?searchValue=&t=%d" % (ip, t)
    response = requests.get(url=url, headers=headers)
    responseContent=json.loads(response.content.decode('utf-8'))
    if responseContent['code']==200:
        taskList= responseContent['data']
       
        return taskList
    else:
        # 没有获取到taskList，返回空
        return []
 
 
def getDuplicate(taskList):
    wholeNames={}
    duplicateID=[]
    taskListTemp=[]
    for index in range(len(taskList)):
        task=taskList[index]
        if task['name'] in wholeNames.keys() and task['command'].find(substr) < 0:
            duplicateID.append(task['_id'])
        else:
            taskListTemp.append(task)
            wholeNames[task['name']] = 1
    #print(taskListTemp)
    return getDuplicateCommon(taskListTemp,duplicateID)
 
def getDuplicateCommon(taskListTemp,duplicateID):
    #if len(duplicateID)==0:
     #   return duplicateID
    duplicateIDTemp=[]
    for task in taskListTemp:
        for taskTemp in taskListTemp:
            if task['_id'] != taskTemp['_id'] and task['name'] == taskTemp['name'] and task['command'].find(substr) < 0:
                duplicateID.append(task['_id'])
    return duplicateID
 
def getData(duplicateID):
    rawData = "["
    count=0
    for id in duplicateID:
        rawData += "\"%s\""%id
        if count<len(duplicateID)-1:
            rawData += ", "
        count+=1
    rawData += "]"
    return rawData
 
def disableDuplicateTasks(duplicateID):
    t = round(time.time() * 1000)
    url = "http://%s:5700/api/crons/disable?t=%d" % (ip, t)
    data=json.dumps(duplicateID)
    headers["Content-Type"]="application/json;charset=UTF-8"
    response=requests.put(url=url,headers=headers,data=data)
    msg = json.loads(response.content.decode('utf-8'))
    if msg['code']!=200:
        print("出错！，错误信息为：%s"%msg)
    else:
        print("成功禁用重复任务")
 
def loadToken():
    # cur_path = os.path.abspath(os.path.dirname(__file__))
    # send("当前路径：",cur_path)
    try:
        with open("/ql/config/auth.json","r",encoding="utf-8") as f:
            data=json.load(f)
    except:
        # pass
        send("无法获取token","")
    return data['token']
 
 
 
 
if __name__ == '__main__':
    print("开始！")
    loadSend()
    # 直接从 /ql/config/auth.json中读取当前token
    token=loadToken()
    # send("成功获取token!","")
    headers["Authorization"] = "Bearer %s"%token
    taskList=getTaskList()
    # 如果仍旧是空的，则报警
    if len(taskList)==0:
        print("无法获取taskList!")
    duplicateID=getDuplicate(taskList)
    before="禁用前数量为：%d"%len(taskList)
    print(before)
    after="禁用重复任务后，数量为:%d"%(len(taskList)-len(duplicateID))
    print(after)
    if len(duplicateID)==0:
        print("没有重复任务")
    else:
        disableDuplicateTasks(duplicateID)
    if send:
        send("禁用成功","\n%s\n%s"%(before,after))
        # print("禁用结束！")