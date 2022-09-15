from cmdUtile import cmd_util


def check_raid_all():
    # 检擦磁盘坏道
    cmd = 'fdisk -l'
    data = cmd_util.exec_cmd(cmd)
    # 获取磁盘名称
    disk_name = str(data).split(' ')[1].split(':')[0]
    # 磁盘只读检测
    cmd2 = f'badblocks -s -v {disk_name}'
    bad = cmd_util.exec_cmd(cmd2)
    if bad is None:
        print('没有坏道')
