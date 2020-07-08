import requests,json,os

# 钉钉开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
sever = os.environ["SERVER"]

# 填写钉钉token,不开启则不用填
token = os.environ["TOKEN"]

# 填入glados账号对应cookie
cookie = os.environ["COOKIE"]

def push2ding(token, title, content):
    headers = {"Content-Type": "application/json"}
    # 消息类型和数据格式参照钉钉开发文档
    # URL: https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    data = {"msgtype": "markdown", "markdown": {"title": f"glados_{title}"}}
    data['markdown']['text'] = content

    r = requests.post(f"https://oapi.dingtalk.com/robot/send?access_token={token}", data=json.dumps(data),
                      headers=headers)
    print(r.text)

def start():    
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer })
    state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer})
    #print(res)

    if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        print(time)
        if sever == 'on':
            #requests.get('https://sc.ftqq.com/' + sckey + '.send?text='+mess+'，you have '+time+' days left')
            title = f"{mess} checkin success"
            msg = f"""# {title}
            
            > {mess} ，you have {time} days left
            
            """
            print(msg)
            push2ding(token, title, msg)
    else:
        #requests.get('https://sc.ftqq.com/' + sckey + '.send?text=cookie过期')
        title = 'checkin error'
        msg = f"""# {title} 
        
        > cookie过期
        
        """
        push2ding(token, title, msg)

def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()
