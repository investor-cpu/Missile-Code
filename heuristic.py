#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lee
A heuristic defense policy
state: perfect observation
len(a)==len(d)
最大限制类的参数设置为无穷大
来袭导弹序列中,将资产 value 最高的设置为current interest
对于攻击 current interest 资产的导弹, 为来袭的每一个导弹分配一个拦截导弹
（🖕终止条件）分配完之后, 将 current interest 设置为下一个最有价值的资产类别；如果没有下一个的话就停止
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
    int_num =    i[3]
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
    max_limit = 0  # 设置最大限制
    surplus = int_num - missile_num  # interceptor 与 missile 的差值

    '''current interest 是我们要保护的资产中价值最高的一类'''
    c_i = np.zeros(3)
    # 判断当前的攻击向量中，被攻击的资产中谁的value 最高
    if sum(a3) != 0:  # 对资产3有攻击的行为
        c_i[2] = 1
    elif sum(a2) != 0:  # 对资产2有攻击的行为
        c_i[1] = 1
    elif sum(a1) != 0:  # 对资产1有攻击行为
        c_i[0]  = 1


    if sum(c_i)==0:
        return defence
    while max_limit>=0:
        if c_i[2]==1:
            defence[asset1+asset2:asset3+asset2+asset1] = a3  # 为每个攻击c r 资产类别的导弹分配一个拦截导弹
            c_i[2] = 0
            if sum(a2):
                c_i[1] = 1
            elif sum(a1):
                c_i[0] = 1
        if c_i[1]==2:  # 要么 asset3 已经分配导弹，要么 asset3 未遭到攻击
            defence[asset1:asset2+asset1] = a2
            c_i[1] = 0
            if sum(a1):
                c_i = 1
        if c_i[0]==1:
            defence[:asset1] = a1
            max_limit = surplus - asset2
            c_i[0] = 0




    # if int_num>missile_num:  # 当interceptor 比 missile 多的时候
    #     surplus = int_num-missile_num  # interceptor 比 missile 多了多少
    #     d = a.copy()
    #     for i in range(surplus):
    #         if surplus<attack_asset3:  # 将盈余的拦截导弹分配给价值最高的资产
    #             if d[len(d)-i-1]:
    #                 d[len(d)-i-1] += 1
    #         if surplus<attack_asset3+attack_asset2 and surplus>attack_asset3:
    #             if d[len(d)-i-1]:
    #                 d[len(d)-i-1] += 1
    #         if surplus<attack_asset3+attack_asset2+attack_asset1 and surplus>attack_asset3+attack_asset2:
    #             if d[len(d)-i-1]:
    #                 d[len(d)-i-1] += 1
    #         if surplus>attack_asset3+attack_asset2+attack_asset1:
    #             if d[len(d)-i-1]:
    #                 d[len(d)-i-1] += 1

    return defence



if __name__=="__main__":
    i = np.array([1, 1, 2, 6,4])
    a = np.zeros(4)
    a[2] = 6
    a[3] = 9
    d = allocation_interceptor(i, a)
    print("defense is ", d)