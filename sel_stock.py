#!/usr/bin/env python

from futuquant import *
import pandas as pd
import talib

host = '127.0.0.1'
start = "2018-07-01"
end = None

quote_ctx = OpenQuoteContext(host=host,port=11111)

ret, data = quote_ctx.get_plate_stock('SH.3000005')

codelist = data.code.values

n = 0 # Count the total number of stocks which fit our condition

for code in codelist:
    ret, data = quote_ctx.get_history_kline(code,start=start, end=end)
    close = data.close.values
    open = data.open.values
    high = data.high.values
    low = data.low.values
    day = data.time_key.values

    if len(close)<3:
        continue

    # Just to remove the comment if need to use the MA line
    MA13 = talib.MA(close, timeperiod=13, matype=0)
    MA34 = talib.MA(close, timeperiod=34, matype=0)
    MA55 = talib.MA(close, timeperiod=55, matype=0)

    # Price change in last serverl days
    maxP = talib.MAX(high, timeperiod=15)
    minP = talib.MIN(low, timeperiod=15)

    # 股价在15分交易日下跌或者振幅超过20%后，出现跳空的底分型
    if max(close[-2],open[-2])<min(close[-3],open[-3])\
         and min(close[-1],open[-1])>max(close[-2],open[-2])\
         and high[-2]<high[-1] and high[-3]>high[-2] and low[-2]<low[-3] and low[-1]>low[-2]\
         and (maxP[-1]-minP[-1])/minP[-1]>0.2: # Ensur the price down 20% recently
         print(day[-1] + "\t" + code + "\t : 跳空底分型")
         n = n + 1

    # 股价在15个交易日下跌超过20%后，13周期线走平，股价在13周期线上方得到支撑，没有远离13周期线
    #if MA13[-3]>MA13[-2] and MA13[-2]<MA13[-1] \
    #    and min(open[-1],open[-2],open[-3]) < MA13[-2]\
    #    and (maxP[-1]-minP[-1])/minP[-1]>0.2\
    #    and (MA55[-1]-MA13[-1])/MA13[-1]>0.1 \
    #    and close[-1]>MA13[-1] :
    #    print(day[-1] + "\t" + code + "\t : 底部13周期线支撑")
    #    n = n + 1

    # 13，34和55周期线多头排列，股价没有启动：
    #if MA13[-1]>MA34[-1]>MA55[-1] and MA13[-1]>MA13[-2]:
    #    count = 0 #统计最近9个交易日股价得到34周期线支撑的情形
    #    for i in [-1,-2,-3,-4,-5,-6,-7,-8,-9]:
    #        if low[i]<=MA34[i] and close[i]>=MA34[i]:
    #            count = count + 1
    #    if count>=2:
    #        print(day[-1] + "\t" + code + "\t : 均线多头，没有启动")
    #        n = n + 1

print("total stocks:" + str(n))

quote_ctx.close()
