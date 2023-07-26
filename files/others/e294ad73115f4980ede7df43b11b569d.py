import time
import pandas
start=time.time()
def gd(n):
    result1=[]#从0开始
    result2=[]#每个数据
    bj=-1
    while True:
        bj=bj+1
        result1.append(bj)
        result2.append(n)
        if n==1:
            break
        else:
            if n%2==0:
                n=int(n/2)
            else:
                n=1+3*n
    return result1,result2   

 
def dmax(a:list):
    ma=a[0]
    for i in a:
        if i>ma:
            ma=i
    return ma        

times=[start]
nums=[]
step=[]
maxs=[]
for j in range(1,100000000): 
    if j%100000==0:
        t1=time.time()
        times.append(t1)
        dt1=t1-start
        dt2=times[-1]-times[-2]
        print(f'Up to {j}, work done, cost time(all):{dt1}, this 2000 numbers cost time:{dt2}.')  
    a,b=gd(j)
    nums.append(j)
    step.append(a[-1])
    maxs.append(dmax(b))


dic={'Start':nums,'Steps':step,'Maxium':maxs} 
DF2=pandas.DataFrame(dic)
DF2.to_csv("result.csv",index=False)