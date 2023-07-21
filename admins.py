from forms import get_time
def check(date=get_time()[0:10].replace("/","-")):
    
    with open("P:\\ETRO.web\\project\\logging\\loggings-%s.log"%(date),"r",encoding="utf8") as loga:
        jilus=loga.readlines()
    infos=0;warns=0;quess=0;error=0;elses=0
    for i in jilus:
        type_=i[23:28]
        #print(type_)
        if type_=="INFO-":
            infos+=1
        elif type_=="QUES-":
            quess+=1
        elif type_=="WARN-":
            warns+=1
        elif type_=="ERROR":
            error+=1
        else:
            elses+=1
    print("审核了今天(%s)的日志文件,其中共%s条记录.\nINFO记录共 %s 条, QUES记录共 %s 条;\nWARN记录共 %s 条, ERROR记录共 %s 条, 其它记录共 %s 条."%(date.replace("-","/"),infos+quess+warns+error+elses,infos,quess,warns,error,elses))
check("2023-07-16")

