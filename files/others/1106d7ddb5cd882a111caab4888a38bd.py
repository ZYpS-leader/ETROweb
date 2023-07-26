def resplit(old:str):
    answer=[""]
    new=old.split("1")
    for i in range(len(new)):
        if i!=len(new)-1:
            if new[i]=="":
                answer[-1]+="1"
            else:
                answer.append(new[i])
                answer.append("1")
        else:
            if new[-1]=="":
                pass
            else:
                answer.append(new[-1])

    if answer[0]=="":
        answer.pop(0)
    result=[]
    for j in answer:
        linshi=gd(j)
        for k in linshi:
            result.append(k)
        del linshi
    answer=[]
    for l in range(len(result)):
        if len(result[l])!=1:
            answer.append(result[l])
        else:
            if l<=len(result)-3:
                if len(result[l])==len(result[l+1]) and len(result[l+1])==len(result[l+2]) and len(result[l])==1:
                    if result[l]=="1":
                        answer.append("101")
                    else:
                        answer.append("010")
                    l+=3
                else:
                    answer.append(result[l])
            else:
                answer.append(result[l])
    return answer

def gd(old):
    answer=[]
    for i in range(len(old)):
        if i%7==0:
            answer.append("")
        answer[-1]+=old[i]
    return answer

def make_zip(old:str):
    old_list=resplit(old)
    answer=[]
    oldl=len(old)
    dui={
        "0":"00",
        "1":"01",
        "00":"010",
        "11":"011",
        "000":"100",
        "111":"101",
        "0000":"1000",
        "1111":"1001",
        "00000":"1010",
        "11111":"1011",
        "000000":"1100",
        "111111":"1101",
        "0000000":"1110",
        "1111111":"1111",
        "010":"110",
        "101":"111"
    }
    for i in old_list:
        answer.append(dui[i])
    newl=4*len(answer)
    return answer,newl/oldl

import random
def get(length):
    s=""
    for _ in range(length):
        s+=str(random.randint(0,1))
    return s

bs=0
sas=[]
sbs=[]
import matplotlib.pyplot as plt
for i in range(1000,20001):
    a,b=make_zip(get(i))
    bs+=b 
    if i%1000==0:
        print(i,"           ",100*b,"%")
        sas.append(i)
        sbs.append(b)
        
print("average        ",100*bs/19000,"%")
plt.plot(sas,sbs)
plt.show()