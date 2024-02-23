import time
from add_element import update_rel_paths
from exam import check_integrity


def schedule_integrity_check():
    while True:
        update_rel_paths()
        check_integrity()
        time.sleep(1)  # 1 hora