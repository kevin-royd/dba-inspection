from cmdUtile import cmd_util


class Raid(object):

    def __init__(self):
        self.disk_name = ''

    def get_disk_name(self):
        cmd = 'fdisk -l'
        data = cmd_util.exec_cmd(cmd)
        # 获取磁盘名称
        self.disk_name = str(data).split(' ')[1].split(':')[0]
        return self.disk_name

    # 检擦磁盘坏道
    def check_raid_all(self):
        # 磁盘只读检测
        cmd2 = f'badblocks -s -v {self.disk_name}'
        bad = cmd_util.exec_cmd(cmd2)
        if bad is None:
            print('没有坏道')
