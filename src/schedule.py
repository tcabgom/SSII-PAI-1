import time
from add_element import update_rel_paths
from exam import check_integrity


def read_hours_between_tests():
    try:
        with open('hids.config', 'r') as config_file:
            content = config_file.read().strip()
            if content.startswith("horas = "):
                return int(content[len("horas = "):])
            else:
                return 1
    except FileNotFoundError:
        return 5

def schedule_integrity_check():

    hours_between_tests = read_hours_between_tests()
    
    while True:
        update_rel_paths()
        check_integrity()
        time.sleep(hours_between_tests)
        #time.sleep(hours_between_tests * 3600)