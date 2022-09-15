import subprocess


def check_raid_all():
    # 检擦磁盘坏道
    call = subprocess.call(['fdisk', '-l'], shell=True)
    print(call)
    # 过滤磁盘