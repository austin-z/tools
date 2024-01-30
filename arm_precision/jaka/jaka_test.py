# -*- coding: utf-8 -*-

import sys
import os
import math
import time
import __common
import csv

ABS = 0
INCR= 1

def get_tcp_position(robot):
    err, tcp = robot.get_tcp_position()
    if err:
        print("get_tcp_pos failed:", err)
        sys.exit()
    return tcp

def get_joint_position(robot):
    err, joint = robot.get_joint_position()
    if err:
        print("get_joint_position failed:", joint)
        sys.exit()
    return joint

def save_result(name, columns, result):
    csv_file = name + ".csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(result)

def test1(robot):
    result_tcp = []
    result_joint = []

    for i in range(0, 100):
        tcp = get_tcp_position(robot)
        result_tcp.append(tcp)

        joint = get_joint_position(robot)
        result_joint.append(joint)

        time.sleep(0.5)

    save_result("test1_tcp", ['x', 'y', 'z', 'rx', 'ry', 'rz'], result_tcp)
    save_result("test1_joint", ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'], result_joint)

def test2(robot):
    p0 = get_tcp_position(robot)
    p1 = [item + 10 if i < 3 else item + 0.0175 for i, item in enumerate(p0)]
    print(p0, p1)

    result = []

    for i in range(0, 100):
        if i % 2 == 0:
            robot.linear_move(p1, ABS, True, 10)
            time.sleep(1)

            p = get_tcp_position(robot)
            diff = [abs(a - b) for a, b in zip(p, p1)]
            print(i, "diff:", diff)
            result.append(diff)
        else:
            robot.linear_move(p0, ABS, True, 10)
            time.sleep(1)

            p = get_tcp_position(robot)
            diff = [abs(a - b) for a, b in zip(p0, p)]
            print(i, "diff:", diff)
            result.append(diff)

    save_result("test2_tcp", ['x', 'y', 'z', 'rx', 'ry', 'rz'], result)

def test3():
    p0 = get_joint_position(robot)
    p1 = [item + 0.0175 for item in p0]
    print(p0, p1)

    result = []

    for i in range(0, 50):
        if i % 2 == 0:
            robot.joint_move(p1, ABS, True, 5)
            time.sleep(1)

            p = get_joint_position(robot)
            diff = [abs(a - b) for a, b in zip(p, p1)]
            print(i, "diff:", diff)
            result.append(diff)
        else:
            robot.joint_move(p0, ABS, True, 5)
            time.sleep(1)

            p = get_joint_position(robot)
            diff = [abs(a - b) for a, b in zip(p0, p)]
            print(i, "diff:", diff)
            result.append(diff)

    save_result("test3_joint", ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'], result)

if __name__ == '__main__':
    __common.init_env()
    import jkrc

try:
    robot = jkrc.RC("192.168.0.204")
    print("login:", robot.login())
    #print("power_on: ", robot.power_on())
    #print("enable_robot: ", robot.enable_robot())

    test3()

except Exception as e:
  print("An error occurred:", e)

finally:
    #print("disable_robot: ", robot.disable_robot())
    #print("power_off: ", robot.power_off())
    print("logout: ", robot.logout())

