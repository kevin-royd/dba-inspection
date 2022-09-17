import subprocess


def exec_cmd(cmd):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        while p.poll() is None:
            if p.wait() == 0:
                result = p.stdout.readline()
                p.stdout.close()
                # 返回结果被byte
                return result
            else:
                return None

    except:
        print('命令执行失败。返回结果错误')
        exit(0)
