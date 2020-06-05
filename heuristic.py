#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lee
A heuristic defense policy
state: perfect observation
len(a)==len(d)
最大限制类的参数设置为无穷大
来袭导弹序列中,将资产 value 最高的设置为current interest
根据问题的物理限制和最大限制，对于攻击 current interest 资产的导弹, 为来袭的每一个导弹分配一个拦截导弹
分配完之后, 将 current interest 设置为下一个最有价值的资产类别；如果没有下一个的话就停止
设置最大限制，即拦截导弹超过导弹的剩余量减去所有资产类别中价值大于当前利益类别的资产总数，最有价值的剩余资产类别除外
回到步骤3
"""
import math
import random
import numpy as np


def allocation_interceptor(i, a):
    '''
    为每个攻击 current interest 资产类别的 missile 分配一个 interceptor
    :param i: state
    :param a: current attack
    :return: defense vector
    '''
    print("input_i is ", i)
    print("input_a is ", a)
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
    a2 = a[asset1:asset1+asset2]
    a3 = a[asset1+asset2:asset3+asset2+asset1]

    # 分别统计三种类型资产被攻击的数量
    attack_asset1 = 0
    attack_asset2 = 0
    attack_asset3 = 0
    for j in a1:
        if j:
            attack_asset1 += 1
    for j in a2:
        if j:
            attack_asset2 += 1
    for j in a3:
        if j:
            attack_asset3 += 1

    defence = np.zeros(len(a))


    '''current interest 是我们要保护的资产中价值最高的一类'''
    c_i = -1
    # 判断当前状态下初始的current interest
    if sum(a3) != 0:  # 对资产2有攻击的行为
        c_i = 2
    elif sum(a2) != 0:  # 对资产1有攻击的行为
        c_i = 1
    elif sum(a1) != 0:  # 对资产0有攻击行为
        c_i = 0

    max_limit = -2  # 设置最大限制

    loop = 0  # 记录循环次数, 主要是用来控制第二次及以后的拦截弹分配, 适合拦截弹比导弹多的场景
    while c_i!=-1 and max_limit!=0 and max_limit!=-1:
        surplus = int_num - missile_num  # interceptor 与 missile 的差值
        print("surplus is ", surplus)
        if c_i==2:  # current interest 的资产类别是价值最高的, value=3
            if loop==0:
                defence[asset1+asset2:asset3+asset2+asset1] = a3
                int_num = int_num - sum(a3)  # interceptor 库存减少
            elif loop!=0 and max_limit>0:
                for k in range(max_limit):
                    if defence[len(defence)-k-1]:
                        defence[len(defence) - k - 1] += 1
                        int_num -= 1
            if surplus - (asset1+asset2)>0:
                max_limit = surplus - (asset1+asset2)
            else:
                max_limit = -1
            if sum(a2)!=0:
                c_i = 1
            elif sum(a1)!=0:
                c_i = 0
            elif sum(a1)==0 and sum(a2)==0:
                c_i = -1
        if c_i == 1:  # current interest 的资产类别 初始为1或者由上转移而来, value=2
            if loop==0:
                defence[asset1:asset2+asset1] = a2
                int_num = int_num - sum(a2)
            elif loop != 0 and max_limit > 0:
                for k in range(max_limit):
                    if defence[len(defence) - k - 1]:
                        defence[len(defence) - k - 1] += 1
                        int_num -= 1
            if surplus - (asset2+asset1)>0:
                max_limit = surplus - (asset2+asset1)
            else:
                max_limit = -1
            if sum(a1)!=0:
                c_i = 0
            else:
                c_i = -1
        if c_i == 0:
            if loop==0:
                defence[:asset1] = a1
                int_num = int_num - sum(a1)
            elif loop != 0 and max_limit > 0:
                for k in range(max_limit):
                    if defence[len(defence) - k - 1]:
                        defence[len(defence) - k - 1] += 1
                        int_num -= 1

            if surplus - (asset2+asset1)>0:
                max_limit = surplus - (asset2+asset1)
            else:
                max_limit = -1
        loop = loop+1

    return defence



if __name__=="__main__":
    i = np.array([1, 1, 2, 7,4])
    a = np.array([1, 1, 1, 2])
    d = allocation_interceptor(i, a)
    print("defense is ", d)