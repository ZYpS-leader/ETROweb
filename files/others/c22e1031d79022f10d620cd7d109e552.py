import statsmodels.api as sm
import pandas as pd
import numpy as np
def st(path,x:float,mode=0):      
    la=pd.read_csv(path,usecols=['特征组'] )
    lb=pd.read_csv(path,usecols=["目标组"]) 
    la1=list(la["特征组"])
    lb1=list(lb["目标组"])
    X=la1
    Y=lb1
    if mode==0:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.sin(X),np.tan(X),np.cos(X)  ))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.sin(x),np.tan(x),np.cos(x)])
    elif mode==1:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.sin(X)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.sin(x) ])
    elif mode==2:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4)])   
    elif mode==3:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,5)])   
    elif mode==4:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,5),np.power(X,6)])   
    elif mode==5:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,5),np.power(X,6),np.power(X,7)])   
    elif mode==6:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8)])   
    elif mode==7:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9)]) 
    elif mode==8:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10)])   
    elif mode==9:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11)])   
    elif mode==10:
        dX=np.column_stack((X,np.power(X,2),np.power(X,3),np.power(X,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11),np.power(X,12)))
        X_added=sm.add_constant(dX)
        model=sm.OLS(Y,X_added)
        results=model.fit() 
        p1="本次精度为"+str(results.rsquared*100)+"%"   
        p2=results.predict([1,x,np.power(x,2),np.power(x,3),np.power(x,4),np.power(X,4),np.power(X,5),np.power(X,6),np.power(X,7),np.power(X,8),np.power(X,9),np.power(X,10),np.power(X,11),np.power(X,12)]) 
    a1=p1;a2=p2                                             
    try:
        p=p2[0]
        p=list(p)
        p0=p[0]
        sum0=0
        for i in p0:
            sum0=sum0+i
        p2=sum0/len(p0)
    except:
        p1=a1
        p2=a2
    return p1,p2
