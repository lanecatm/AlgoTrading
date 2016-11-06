# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 20:11:28 2016

@author: user
"""

import tushare as ts
import pymysql
#import traceback
import calendar

conn= pymysql.connectconn= pymysql.connect(host = "localhost", user = "root", passwd = "haopan09", port = 3306, charset = 'utf8')
cur = conn.cursor()
#cur.execute("create database if not exists stockamount")
cur.execute("use stockamount")

cur.execute("create table if not exists stockdata (code_tick varchar(20), date_tick varchar(20), minu_tick varchar(20), amou_tick int )")


year = 2014
monthlist = []
if(calendar.isleap(year)==True):
    datelength = [31,29,31,30,31,30,31,31,30,31,30,31]
else:
    datelength = [31,28,31,30,31,30,31,31,30,31,30,31]

workdaystringlist= []

for i in range(1,13):
    monthlist.append(i)

for i in range(len(monthlist)):
    for j in range(1,datelength[i]+1):
        if(calendar.weekday(year,i+1,j)<5):
            workdaystringlist.append(str(year)+"-"+str(i+1)+"-"+str(j))

codestring = '601006'
#datestring = '2016-08-30'


def getdf(codestring,datestring):
    while(1):
        try:
            df = ts.get_tick_data(codestring,datestring)
            return df
            break
        except:
            print ("waiting")
            pass
        

for datestring in workdaystringlist: 
    df = getdf(codestring,datestring)
    print (df.head(10))
    runflag = 1
    if(((df['time'][0]=='alert("当天没有数据");')and(df['time'][1]=='window.close();')and(df['time'][2]=='</script>'))or(len(df)<5)):
        runflag = 0
        continue
    
    if(runflag == 1):
        minute = []
        minuteamount = []
        
        tmpsecond = df['time'][0]
        tmpsplit = tmpsecond.split(':')
        tmpminute = tmpsplit[0]+'\''+tmpsplit[1]
        minute.append(tmpminute)
        
        lasttmpminute = tmpminute
        
        tmptotal = 0
        
        for i in range(1, len(df)):
            tmpsecond = df['time'][i]
            tmpsplit = tmpsecond.split(':')
            tmpminute = tmpsplit[0]+'\''+tmpsplit[1]
            if(tmpminute!=lasttmpminute):
                minute.append(tmpminute)
                minuteamount.append(tmptotal)
                tmptotal = 0
            else:
                tmptotal = tmptotal + df['amount'][i]
            lasttmpminute = tmpminute
        
        #Analysis the last two timestamp
        tmpsecond_2 = df['time'][len(df)-2]
        tmpsplit_2 = tmpsecond_2.split(':')
        tmpminute_2 = tmpsplit_2[0]+'\''+tmpsplit_2[1]
        
        tmpsecond_1 = df['time'][len(df)-1]
        tmpsplit_1 = tmpsecond_1.split(':')
        tmpminute_1 = tmpsplit_1[0]+'\''+tmpsplit_1[1]
        
        if(tmpminute_1 == tmpminute_2):
            minuteamount[-1] = minuteamount[-1] + df['amount'][len(df)-1]
        
        if(tmpminute_1 != tmpminute_2):
            minuteamount.append(df['amount'][len(df)-1])
        
        print (minute)
        print (len(minute))
        print (minuteamount)
        print (len(minuteamount))
        
        
        for index in range(len(minuteamount)):
            SQL = "insert into stockdata (code_tick, date_tick, minu_tick, amou_tick) values (%s, %r, %r, %d)"%(codestring, datestring, minute[index], minuteamount[index])
            cur.execute(SQL)
            conn.commit()