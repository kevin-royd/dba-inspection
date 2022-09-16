from raid import check_raid
from centos import check_os

if __name__ == '__main__':
    # 初始化日志文件

    # 检查磁盘
    check_raid.check_raid_all()

    # 检查os
    check_os.check_numa()
