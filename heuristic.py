#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lee
A heuristic defense policy
state: perfect observation
len(a)==len(d)
"""
import math
import random
import numpy as np

state_i = [10, 10, 10, 60, 40]
L_M = 6
L_I = 4

def allocation_interceptor(i, a):
    '''
    为每个攻击 current interest 资产类别的 missile 分配一个 interceptor
    :param i: state
    :param a: current attack
    :return: defense vector
    '''
    # 三类资产的剩余量
    asset1 = i[0]
    asset2 = i[1]
    asset3 = i[2]
    asset_sum = asset3 + asset2 + asset1

    # interceptor 和 missile 的剩余量
    int_num = i[3]
    missile_num = i[4]

    # 对三类资产的攻击向量
    a1 = a[:asset1]
    a2 = a[asset1:asset2]
    a3 = a[asset2:asset3]

    defence = np.zeros(len(a))


    '''current interest 是我们要保护的资产中价值最高的一类'''
    c_r = -1
    if sum(a3) != 0:
        c_r = 3
    elif sum(a2) != 0:
        c_r = 2
    elif sum(a1) != 0:
        c_r  = 1
    else:
        c_r = 0  # attack vector 攻击部分全部为0，即missile库存为0，因为要求最少发射一枚missile

    if c_r==3:
        pass
    if c_r==2:
        pass
    if c_r==1:
        pass


    if int_num>missile_num:  # 当interceptor 比 missile 多的时候
        surplus = int_num-missile_num  # interceptor 比 missile 多了多少
        d = a.copy()
        for i in range(surplus):
            pass

    else:                    # 当 missile 比 interceptor 多的时候
        if c_r==3:
            pass
        elif c_r==2:
            pass
        elif c_r==1:
            pass
        elif c_r==0:
            pass




    return defence



if __name__=="__main__":
    pass