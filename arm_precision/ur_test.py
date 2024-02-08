import time
import csv
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.0.17"
#ROBOT_IP = "192.168.0.125"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

def save_result(name, columns, result):
    csv_file = name + ".csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(result)

def test_idle_read():
    result_tcp = []
    result_joint = []

    for i in range(0, 100):
        tcp = rtde_r.getActualTCPPose()
        result_tcp.append(tcp)

        joint = rtde_r.getActualQ()
        result_joint.append(joint)

        print(tcp, joint)

        time.sleep(0.5)

    save_result("test_idle_read_tcp_ur", ['x', 'y', 'z', 'rx', 'ry', 'rz'], result_tcp)
    save_result("test_idle_read_joint_ur", ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'], result_joint)

def test_tcp_servo():
    p0 = rtde_r.getActualTCPPose()
    p1 = [item + 0.01 if i < 3 else item + 0.0175 for i, item in enumerate(p0)]
    print(p0)
    print(p1)

    result = []
    speed = 0.1             # NOT used
    acceleration = 0.1      # NOT used
    ctrl_time = 1.0
    lookahead_time = 0.1
    gain = 300

    for i in range(0, 300):
        if i % 2 == 0:
            #start_time = time.time()
            rtde_c.servoL(p1, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(ctrl_time + 2.0)
            #print("elapsed:", time.time() - start_time)

            p = rtde_r.getActualTCPPose()
            diff = [abs(a - b) for a, b in zip(p, p1)]
            diff = [item * 1000.0 if i < 3 else item for i, item in enumerate(diff)]
            print(i, "diff:", diff)
            result.append(diff)
        else:
            #start_time = time.time()
            rtde_c.servoL(p0, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(ctrl_time + 2.0)
            #print("elapsed:", time.time() - start_time)

            p = rtde_r.getActualTCPPose()
            diff = [abs(a - b) for a, b in zip(p0, p)]
            diff = [item * 1000.0 if i < 3 else item for i, item in enumerate(diff)]
            print(i, "diff:", diff)
            result.append(diff)

    save_result("test2_tcp_ur", ['x', 'y', 'z', 'rx', 'ry', 'rz'], result)

def test_joint_servo():
    p0 = rtde_r.getActualQ()
    p1 = [item + 0.0175 for item in p0]
    print(p0, p1)

    result = []
    speed = 0.1
    acceleration = 0.1
    ctrl_time = 1.0
    lookahead_time = 0.1
    gain = 100

    for i in range(0, 100):
        if i % 2 == 0:
            rtde_c.servoJ(p1, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(3)

            p = rtde_r.getActualQ()
            diff = [abs(a - b) for a, b in zip(p, p1)]
            print(i, "diff:", diff)
            result.append(diff)
        else:
            rtde_c.servoJ(p0, speed, acceleration, ctrl_time, lookahead_time, gain)
            time.sleep(3)

            p = rtde_r.getActualQ()
            diff = [abs(a - b) for a, b in zip(p0, p)]
            print(i, "diff:", diff)
            result.append(diff)

    save_result("test_joint_servo_ur", ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'], result)

if __name__ == '__main__':
  try:
    test_idle_read()

  except Exception as e:
    print("An error occurred:", e)

  finally:
    rtde_c.disconnect()
    rtde_r.disconnect()
