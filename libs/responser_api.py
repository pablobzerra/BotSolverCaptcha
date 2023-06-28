from timeout_decorator import timeout
import socket


def get_reponse(data, id):
    if data[str(id)] is None:
        return {"status": "aguardando...."}
    else:
        return {"msg": data[str(id)]}
    
def handler(signum, fram):
    raise TimeoutError("Tempo limite excedido")


def waiting_handler(data, id, lock):
    with lock:
        if data[id] is None:
            return "Aguarde...."
        
def avaible_handler(data, id):
    if data[id] is None:
        return data[id]
        
    
