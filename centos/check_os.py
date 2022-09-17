from cmdUtile import cmd_util, logger
import re


def check_numa():
    log = logger.Logger().get_log
    # 首先判断是否启动了numa
    cmd = 'dmesg | grep -i numa=off'
    message = cmd_util.exec_cmd(cmd)  # 管道符执行才会有结果输出
    if message is None:
        # 判断内核文件是否已经添加了numa=off
        cmd_grep_numa = 'cat /etc/default/grub | grep numa=off'
        numa_message = cmd_util.exec_cmd(cmd_grep_numa)
        # 如果为空表示未修改
        if numa_message is None:
            print('numa未关闭,执行修改内核参数')
            cmd_numa = "sed -i 's#biosdevname=0#biosdevname=0 numa=off#' /etc/default/grub"
            cmd_util.exec_cmd(cmd_numa)
            # 校验上条命令是否有报错 因为sed命令无返回结果。如果有返回肯定是错误信息
            if cmd_util is not None:
                log.error('请检查文件是否存在：/etc/default/grub')
            else:
                print('numa关闭成功,重启机器生效')
                # 需要重新读取配hi在
                cmd_reload = 'grub2-mkconfig -o /boot/grub2/grub.cfg'
                cmd_util.exec_cmd(cmd_reload)
        print('numa关闭成功,重启机器生效')
    else:
        print('numa已关闭')


# 通过判断swap空间大小来判断是否启用
def check_swap():
    log = logger.Logger.get_log()
    cmd = "free -m | grep -i 'swap' | awk '{print $2}'"
    message = cmd_util.exec_cmd(cmd)
    # 对返回结果进行处理 b'0\n'
    result = re.search('.*([0-9]+)', str(message)).group(1)
    if result != 0:
        print('未关闭swap。现在开始关闭swap')
        cmd_buffer = 'echo 3 > /proc/sys/vm/drop_caches'
        # 该命令也无返回值 有返回值也报错
        message_buffer = cmd_util.exec_cmd(cmd_buffer)
        if message_buffer is not None:
            log.error('清空系统缓存错误')
        # 关闭swap
        cmd_swap = 'swapoff -a'
        message_buffer = cmd_util.exec_cmd(cmd_swap)
        if message_buffer is not None:
            log.error('关闭swap出错')
        print('')
