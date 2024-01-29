# -*- coding: utf-8 -*-

import sys
import os
import math
import time
import __common
import csv

ABS = 0
INCR= 1

def save_result(tag, result):
    csv_file = tag + ".csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result)

def test1():
    robot = jkrc.RC("192.168.0.204")
    print("login: ", robot.login())

    result_tcp = []
    result_joint = []

    for i in range(0, 100):
        err, tcp = robot.get_tcp_position()
        if not err:
            result_tcp.append(tcp)
            print("jaka tcp: ", tcp)
        else:
            print("get_tcp_pos failed.")
            sys.exit()

        err, joint = robot.get_joint_position()
        if not err:
            result_joint.append(joint)
            print("jaka joint: ", joint)
        else:
            print("get_tcp_pos failed.")
            sys.exit()

        time.sleep(0.5)

    print("logout: ", robot.logout())

    save_result("test1_tcp", result_tcp)
    save_result("test1_joint", result_joint)

def test2():
    robot = jkrc.RC("192.168.0.204")
    print("login: ", robot.login())
    #print("power_on: ", rc.power_on())
    #print("enable_robot: ", rc.enable_robot())

    ret = robot.get_tcp_position()
    if not ret[0]:
        print("get_tcp_pos ok & tcp pos is: ", ret)
    else:
        print("get_tcp_pos failed.")
        sys.exit()

    init_pose = current_pose = ret[1]

    for i in range(0, 40):
        target_pose = current_pose[:]
        if i % 2 == 0:
            target_pose[0] += 10
            target_pose[1] += 10
            target_pose[2] += 10
        else:
            target_pose[0] -= 10
            target_pose[1] -= 10
            target_pose[2] -= 10

        robot.linear_move(target_pose, ABS, True, 10)
        time.sleep(1)

        ret = robot.get_tcp_position()
        if not ret[0]:
            current_pose = ret[1]
            print("get_tcp_pos ok & tcp pos is: {}".format(ret[1]))
        else:
            print("get_tcp_pos failed.")
            sys.exit()

    print("Pose diff(mm):", [a - b for a, b in zip(init_pose, current_pose)])

    #print("disable_robot: ", rc.disable_robot())
    #print("power_off: ", rc.power_off())
    print("logout: ", robot.logout())

if __name__ == '__main__':
    __common.init_env()
    import jkrc

    test1()
