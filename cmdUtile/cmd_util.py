import subprocess


def exec_cmd(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while p.poll() is None:
            if p.wait() != 0:
                print('命令执行失败。返回结果错误')
            else:
                result = p.stdout.readline()
                # 返回结果被byte
                return result

    except:
        print('命令执行失败。返回结果错误')
        exit(0)