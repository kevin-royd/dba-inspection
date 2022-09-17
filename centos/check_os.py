from cmdUtile import cmd_util, logger
from raid import check_raid
import re
from os import system


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
                cmd_util.exec_cmd(cmd_numa)
                # 校验上条命令是否有报错 因为sed命令无返回结果。如果有返回肯定是错误信息
                if cmd_util is not None:
                    self.log.error('请检查文件是否存在：/etc/default/grub')
                else:
                    print('numa关闭成功,重启机器生效')
                    # 需要重新读取配hi在
                    cmd_reload = 'grub2-mkconfig -o /boot/grub2/grub.cfg'
                    cmd_util.exec_cmd(cmd_reload)
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
        print(disk)
        cmd_get_io_scheduler = f'cat /sys/block/{disk}/queue/scheduler'
        io_scheduler = system(cmd_get_io_scheduler)
        # 判断当前的io算法是否为noon或
        now_scheduler = re.search('([a-zA-Z]+)', io_scheduler.split(' ')[0]).group(1)
        if now_scheduler != 'noop' or now_scheduler != 'mq-deadlin' or now_scheduler != 'deadlin':
            print('未设置io调度算法，设置为:mq-deadline')
            system(f'echo mq-deadline > /sys/block/{disk}/queue/scheduler')
            # 修改配置文件避免重启失效
            cmd_add_scheduler = "sed -i 's#biosdevname=0#biosdevname=0 elevator=deadline'"
            message_scheduler = cmd_util.exec_cmd(cmd_add_scheduler)
            if message_scheduler is not None:
                self.log.error('请检查文件是否存在：/etc/default/grub')
            else:
                system('grub2-mkconfig -o /boot/grub2/grub.cfg')
                print('io调度器持久化修改重启机器后生效')
        else:
            print(f'当前io调度算法为:{now_scheduler}。无需修改')
