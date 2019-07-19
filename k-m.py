#!/usr/bin/env python3

#############
# Least Action Principle
# Use the least acion principle to market
# Author: Robbin He
# Date: 2019-07-11
# Licence: Pravicy

############
        #  最小作用量原则是一个普遍的物理性原则，将市场看成物理现象的一部分，
        #  市场的行为应该也满足这个基本的原则。最小作用量原则和对称性，守恒
        #  定律紧密联系，当我们寻找市场中的作用量的具体形式时，无疑可以参考物理
        #  学上的3大守恒定律：

        #  - 能量守恒定律
        #  - 动量守恒定律
        #  - 角动量守恒定律

        #  因为市场中价格的运动是1维，这个和3维的真实世界并不一样，角动量就转化
        #  成了动量，因此没有单独的角动量。

        #  取1分图上的一根K线作为分析的基础，一根1分图上的K线抽象成物理世界的质点
        #  ，其重心设为1分K线的收盘价，开始这些作用量的设计。

############

import time
import re
from futu import *

CODE = 'HK.800000' # Hengshen Index
YEAR = '2019' # constant year
FNAME = 'actions.txt' #store the result
N = 2 # default display record in t mode and c mode


def fmtTime(start, end):
    regx = r'^\d\d\-\d\d\s\d\d:\d\d'

    if not re.match(regx, start):
        errlog('开始时间格式错误')
    elif not (re.match(regx, end) or end is ''):
        errlog('结束时间格式错误')
    elif end is '':
        start = YEAR + '-' + start + ':00'
        end = time.strftime('%m-%d %H:%M', time.localtime(time.time()))
        end = YEAR + '-' + end + ':00'
        return start, end
    elif start > end:
        errlog('结束时间应当晚于开始时间')
    else:
        start = YEAR + '-' + start + ':00'
        end = YEAR + '-' + end + ':00'
        return start, end


def calPenergy(data):
    close = data['close']
    h = len(data['high']) - 1  # 得到上升走势最后一个k线的索引
    l = len(data['low']) -1 # 下降走势最后一个k线的索引

    # 计算一段走势的能量，包括实能和虚能，在上升的走势中，实能为正，虚能为负
    # 在下降的走势中，实能为负，虚能为正

    # 标准上升线段，走势开始在最低点，结束于最高点，可以计算实能和虚能
    if data['low'][0] == data['low'].min() and data['high'][h] == data['high'].max():
        actionP1 = (close - data['low'][0]).sum()
        actionP2 = (close - data['high'][h]).sum() # 虚能计算
        return '%.2f' % actionP1, '%.2f' % actionP2

    # 上升中未完成的线段，或跨段合并能量计算，走势开始于最低点，只能计算实能，不能计算虚能
    elif data['low'][0] == data['low'].min() and data['high'][h] != data['high'].max():
        actionP1 = (close - data['low'][0]).sum()
        actionP2 = 0
        return '%.2f' % actionP1, '%.2f' % actionP2

    # 用于跨段的合并能量计算，因为计算能量的参考零能点必须是最值点，只能计算虚能，没法计算实能
    elif data['high'][h] == data['high'].max() and data['low'][0] != data['low'].min():
        actionP1 = 0
        actionP2 = (close - data['high'][h]).sum() # 虚能计算
        return '%.2f' % actionP1, '%.2f' % actionP2

    # 标准下降线段，走势开始在最高点，结束于最低点，可以就算实能和虚能
    elif data['high'][0] == data['high'].max() and data['low'][l] == data['low'].min():
        actionP1 = (close - data['high'][0]).sum()
        actionP2 = (close - data['low'][l]).sum()
        return '%.2f' % actionP1, '%.2f' % actionP2

    # 下降中未完成的线段，或跨段合并能量计算，走势开始于最高点，只能计算实能，不能计算虚能
    elif data['high'][0] == data['high'].max() and data['low'][l] != data['low'].min():
        actionP1 = (close -data['high'][0]).sum()
        actionP2 = 0
        return '%.2f' % actionP1, '%.2f' % actionP2

    # 用于跨段的合并能量计算，因为计算能量的参考零能点必须是最值点，只能计算虚能，没法计算实能
    elif data['low'][l] == data['low'].min() and data['high'][0] != data['high'].max():
        actionP1 = 0
        actionP2 = (close - data['low'][l]).sum()
        return '%.2f' % actionP1, '%.2f' % actionP2

    else:
        errlog()


def outActions(actionP1,actionP2, start, end, fname):
    str1 = ( start + " To\n " + end + "\t\t"
            + actionP1  + "\t\t"
            + actionP2 )
            #+ actions['M'])

    str2 = ("\n------------------------\t--------------\t\t-------------\n")

    print(str1, str2)

    with open(fname, 'a') as f:
        f.write(str1)
        f.write(str2)


def readActions(fname, n):
    with open(fname, 'r') as f:
        lines = f.readlines()
        if len(lines) < 3 * n:
            errlog("注意：历史记录长度不足")
        else:
            k = 3 * n # There are 3 lines for one record
            while(k > 0):
                print(lines[-k].strip("\n"))
                k = k - 1


def errlog(msg="走势中开头和结尾至少有一个最大或最小值"):
    print('\n\t\t *************')
    print('\t\t' + msg)
    print('\t\t **************')


def run():
    ctx = OpenQuoteContext()
    flag = False # Ensure entered corrent time range before switch to t mode or c mode or request data
    n = N # n, record the t mode loop count

    while(True):
        mode = input('\n\n\n \t\t追踪模式按t，连续模式按c, 观察模式按l,\n'
                '\t\t退出按q，直接回车为正常模式。\n->:')

        if mode is 't':
            if flag:
                start = start # Just for clear,it can be removed
                end = input('\t\t结束时间[mm-dd hh:mm, 缺省为当下]:')
                if not fmtTime(start, end):
                    flag = False
                    continue
                readActions(FNAME, n)
                n = n + 1 # Track mode, we need more record to inspect
            else:
                errlog('请直接回车输入一些数据')

        elif mode is 'c':
            if flag:
                if end is '':
                    errlog('从t模式到c模式没有意义')
                else:
                    start = end
                    end = input('\t\t结束时间[mm-dd hh:mm, 缺省为当下]:')
                    if not fmtTime(start, end):
                        flag = False
                        continue
                    readActions(FNAME, N)
            else:
                errlog('请直接回车输入一些数据')

        elif mode is 'l':
            readActions(FNAME,5)

        elif mode is 'q':
            break

        else:
            start = input('\n\n\t\t开始时间[mm-dd hh:mm]:')
            end = input('\t\t结束时间[mm-dd hh:mm,缺省为当下]:')
            if fmtTime(start, end):
                flag = True

        if flag:
            fstart, fend = fmtTime(start, end)
            _, data, _ = ctx.request_history_kline(CODE, start= fstart, end= fend, ktype='K_1M',max_count=None, fields=[KL_FIELD.HIGH, KL_FIELD.LOW, KL_FIELD.CLOSE])

            if calPenergy(data):
                actionP1, actionP2 = calPenergy(data)
                outActions(actionP1, actionP2, fstart, fend, FNAME)

    ctx.close()

if __name__ == '__main__':
    run()
