import time
from add_element import update_rel_paths
from exam import check_integrity, generar_informe


def read_time_between_tests():
    try:
        with open('hids.config', 'r') as config_file:
            lines = config_file.readlines()
            tiempo = None
            informe = None
            for line in lines:
                if line.startswith("segundos"):
                    tiempo = int(line.split('=')[1].strip())
                elif line.startswith("num_logs"):
                    informe = int(line.split('=')[1].strip())
            
            if tiempo is None or informe is None:
                return (5, 2)
            
            return (tiempo, informe)
        
    except FileNotFoundError:
        return (5, 2)

def schedule_integrity_check():

    contador_logs = 0
    tiempo, informe = read_time_between_tests()
    
    while True:
        time.sleep(tiempo)
        update_rel_paths()
        check_integrity()
        contador_logs+=1
        
        if(contador_logs == informe):
            generar_informe()
            contador_logs=0
                    