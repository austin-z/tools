import time
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.0.157"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

try:
  current_pose = rtde_r.getActualTCPPose()
  print("Current TCP Pose:", current_pose)
  init_pose = current_pose

  for i in range(0, 50):
    target_pose = current_pose[:]
    if i % 2 == 0:
      target_pose[0] += 0.05
    else:
      target_pose[0] -= 0.05
    rtde_c.moveL(target_pose)

    time.sleep(1)

    current_pose = rtde_r.getActualTCPPose()
    print("Current TCP Pose:", current_pose)

    # 读取新的TCP位置和关节位置
    #joint_positions = rtde_r.getActualQ()

  print("Pose diff:", [a - b for a, b in zip(init_pose, current_pose)])

except Exception as e:
  print("An error occurred:", e)

finally:
  rtde_c.disconnect()
  rtde_r.disconnect()
