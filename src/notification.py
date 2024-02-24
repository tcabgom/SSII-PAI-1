from winotify import Notification

def mostrar_notificacion(titulo, mensaje):
   
   toast = Notification(app_id="HIDS",
                     title=titulo,
                     msg=mensaje,
                     duration="short")
   
   toast.show()