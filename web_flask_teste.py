from flask import Flask, jsonify, request
from secrets import token_hex
from libs.responser_api import *
from timeout_decorator import timeout
import threading 
import signal, socket
from threading import Event
web = Flask(__name__)

teste = {}

lock = threading.Lock()
    
@web.route('/api/solved/<id>', methods=["POST"])
def send(id):
    global teste
    id = str(id)
   
    teste[id]["R"] = "HeheBoy"
    teste[id]["event"].set()
    return jsonify({"status": "enviado"})

@web.route('/api/solver', methods=["POST"])
def solver():
    global teste

    id = request.args.get("id")
    id = str(id)


    '''def timeout_handler():
        with lock:
            if teste[id] is None:
                teste[id] = "tesye"

    
    timer = threading.Timer(30, timeout_handler)
    timer.start()'''

    event = Event()
    teste[id] = {}
    teste[id]['event'] = event
    print(str(teste[id]["event"]))
    t = 30
    if not event.wait(t):
        return jsonify({"status": "t"})
    
    r = teste[id]["R"]
    return jsonify({"msg": r})




    


    #return "Tempo limite"

   # return jsonify({"status": "Tempo limite excedido"})
    

@web.route("/")
def index():
    return "Aaaaaa"


web.run()