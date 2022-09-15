from cmdUtile import cmd_util


def check_numa():
    # 首先判断是否启动了numa
    cmd = 'grep -i numa /var/log/dmesg'
    result = cmd_util.exec_cmd(cmd)
    print(result)
