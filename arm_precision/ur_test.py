import time
import csv
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.0.17"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

def save_result(name, columns, result):
    csv_file = name + ".csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(result)

def test1():
    result_tcp = []
    result_joint = []

    for i in range(0, 100):
        tcp = rtde_r.getActualTCPPose()
        result_tcp.append(tcp)

        joint = rtde_r.getActualQ()
        result_joint.append(joint)

        time.sleep(0.5)

    save_result("test1_tcp_ur", ['x', 'y', 'z', 'rx', 'ry', 'rz'], result_tcp)
    save_result("test1_joint_ur", ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'], result_joint)

def test2():
    p0 = rtde_r.getActualTCPPose()
    p1 = [item + 0.01 if i < 3 else item + 0.0175 for i, item in enumerate(p0)]
    print(p0, p1)

    result = []
    speed = 0.1
    acceleration = 0.1
    ctrl_time = 1.0
    lookahead_time = 0.1
    gain = 100

    for i in range(0, 200):
        if i % 2 == 0:
            rtde_c.servoL(p1, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(2)

            p = rtde_r.getActualTCPPose()
            diff = [abs(a - b) for a, b in zip(p, p1)]
            print(i, "diff:", diff)
            result.append(diff)
        else:
            rtde_c.servoL(p0, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(2)

            p = rtde_r.getActualTCPPose()
            diff = [abs(a - b) for a, b in zip(p0, p)]
            print(i, "diff:", diff)
            result.append(diff)

    save_result("test2_tcp_ur", ['x', 'y', 'z', 'rx', 'ry', 'rz'], result)

def test3():
    p0 = rtde_r.getActualQ()
    p1 = [item + 0.0175 for item in p0]
    print(p0, p1)

    result = []
    speed = 0.1
    acceleration = 0.1
    ctrl_time = 1.0
    lookahead_time = 0.1
    gain = 100

    for i in range(0, 50):
        if i % 2 == 0:
            rtde_c.servoJ(p1, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(2)

            p = rtde_r.getActualQ()
            diff = [abs(a - b) for a, b in zip(p, p1)]
            print(i, "diff:", diff)
            result.append(diff)
        else:
            rtde_c.servoJ(p0, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(2)

            p = rtde_r.getActualQ()
            diff = [abs(a - b) for a, b in zip(p0, p)]
            print(i, "diff:", diff)
            result.append(diff)

    save_result("test3_joint_ur", ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'], result)

if __name__ == '__main__':
  try:
    test2()

  except Exception as e:
    print("An error occurred:", e)

  finally:
    rtde_c.disconnect()
    rtde_r.disconnect()
