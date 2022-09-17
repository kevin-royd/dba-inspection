from cmdUtile import cmd_util, logger
from raid import check_raid
import re
import os


class CentOS(object):
    def __init__(self):
        self.log = logger.Logger().get_log
        self.disk_name = check_raid.Raid().get_disk_name()

    def check_numa(self):

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
                self.update_grub(cmd_numa)
            else:
                print('numa已关闭,重启机器生效')
                # 需要重新读取配hi在
                cmd_reload = 'grub2-mkconfig -o /boot/grub2/grub.cfg'
                cmd_util.exec_cmd(cmd_reload)
        else:
            print('numa已关闭')

    # 通过判断swap空间大小来判断是否启用
    def check_swap(self):
        cmd = "free -m | grep -i 'swap' | awk '{print $2}'"
        message = cmd_util.exec_cmd(cmd)
        # 对返回结果进行处理 b'0\n'
        result = int(re.search('.*([0-9]+)', str(message)).group(1))
        if result != 0:
            print('未关闭swap。现在开始关闭swap')
            cmd_buffer = 'echo 3 > /proc/sys/vm/drop_caches'
            # 该命令也无返回值 有返回值也报错
            message_buffer = cmd_util.exec_cmd(cmd_buffer)
            if message_buffer is not None:
                self.log.error('清空系统缓存错误')
            # 关闭swap
            cmd_swap = 'swapoff -a'
            message_buffer = cmd_util.exec_cmd(cmd_swap)
            if message_buffer is not None:
                self.log.error('关闭swap出错')
        print('swap已关闭')

    def check_io_scheduler(self):
        # 获取磁盘名称
        # 获取磁盘支持的io调度器和当前使用的调度器
        # 此时的disk_name为/dev 需要进行处理
        disk = re.search('/([0-9a-zA-z]+)$', self.disk_name).group(1)
        cmd_get_io_scheduler = f'cat /sys/block/{disk}/queue/scheduler'
        io_scheduler = os.popen(cmd_get_io_scheduler).readline()
        # 判断当前的io算法是否为noon或deadline
        now_scheduler = re.search('([a-zA-Z-]+)', io_scheduler.split(' ')[0])[0]
        if now_scheduler == 'noop' or now_scheduler == 'mq-deadline' or now_scheduler == 'deadline':
            # 检查是否持久化修改了 返回值类型为str
            elevator = os.popen('grep "elevator=" /etc/default/grub').readline()
            if len(elevator) == 0:
                # io调度算法已修改但未持久化
                cmd_add_scheduler = "sed -i 's#biosdevname=0#biosdevname=0 elevator=deadline#' /etc/default/grub"
                self.update_grub(cmd_add_scheduler)
            else:
                print('io调度算法配置文件已经修改')
        else:
            # 临时修改io调度算法，立即生效
            cmd_update_scheduler = f'echo mq-deadline > /sys/block/{disk}/queue/scheduler'
            echo_scheduler = cmd_util.exec_cmd(cmd_update_scheduler)
            if echo_scheduler is not None:
                self.log.error('请检查文件是否存在：/etc/default/grub')
            cmd_add_scheduler = "sed -i 's#biosdevname=0#biosdevname=0 elevator=deadline#' /etc/default/grub"
            self.update_grub(cmd_add_scheduler)

    def update_grub(self, cmd):
        sed_grub_message = cmd_util.exec_cmd(cmd)
        if sed_grub_message is not None:
            self.log.error('请检查文件是否存在：/etc/default/grub')
        else:
            os.system('grub2-mkconfig -o /boot/grub2/grub.cfg')
            print('内核配置文件：/etc/default/grub 修改成功，重启机器生效')
