#翻译token:     24.520ff7c623116d8f96977efb7da5dbf6.2592000.1688951227.282335-34628604
#关键词token:   24.d07194df57c7d0f885bc29e5fd36dcdb.2592000.1688951300.282335-34628489
#信息提取token: 24.15a2f3f0e5e61624b089570e858864d2.2592000.1688951336.282335-34628487
#文本纠错token: 24.51b0d23125076fbe45ca7cde54884adc.2592000.1688951717.282335-34628483
import requests
import json 
def fy(f,t,q): 
    token="24.520ff7c623116d8f96977efb7da5dbf6.2592000.1688951227.282335-34628604"
    url = "https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token="+token
    
    payload = json.dumps({
        "from": f,
        "to": t,
        "q": q
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    r=response.text
    with open("fyrs.txt","w",encoding="utf-8") as wr:
        for i in r:
            if i=="{":
                wr.write("{\n   ")
            elif i=="}":
                wr.write("\n}")
            elif i=="[":
                wr.write("[\n   ")
            elif i=="]":
                wr.write("\n]") 
            else:
                wr.write(i)
    with open("fyrs.txt","r",encoding="utf-8") as re:
        reul=re.readlines()
        res=reul[4].replace("\n","")
    return res     