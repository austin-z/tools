import os
import sys
import ctypes

import platform

def init_env():
    base_dir = os.path.dirname(__file__)

    env_path = os.path.join(base_dir, r'./libjakaAPI.so')
    print(env_path)
    ctypes.CDLL(env_path)
    sys.path.append(env_path)

    env_path = os.path.join(base_dir, r'./jkrc.so')
    print(env_path)
    ctypes.CDLL(env_path)
    sys.path.append(env_path)

    # 加载Window Python jkzuc模块查找路径
    #syspath = os.path.join(base_dir, r'out/shared/jkrc.so') #out/python3
    #sys.path.append(syspath)
    # print('SYS PATH: {}\n {}'.format(sys.path, syspath))
    # print('LD_LIBRARY_PATH: {}'.format(os.environ['LD_LIBRARY_PATH']))

if __name__ == '__main__':
    init_env()
