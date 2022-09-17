from raid import check_raid
from centos import check_os

if __name__ == '__main__':

    # 检查磁盘
    # check_raid.check_raid_all()

    # 检查os 实例化os对象
    os = check_os.CentOS()
    # check_os.check_numa()
    os.check_io_scheduler()
