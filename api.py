from flask import Flask, jsonify, request
from threading import Event
from telebot import TeleBot
from libs.db import *
from secrets import token_hex
import requests

#Carregar as configuraçao do bot
file_config = open("config.json", "r").read()
config = json.loads(file_config)

token_bot = config["token"]
channel_admin = config["channels"]

#Estanciando BOT
bot = TeleBot(token_bot)

#Estanciando API
web = Flask(__name__)

#PAGINAS WEB
trabalhador_page = open("web/trabalhador.html", "r").read()
cliente_page = open("web/client.html", "r").read()
docs_page = open("web/docs.html", "r").read()

#TEXTOS
menssages = config["menssages"]
history_trabalhador = open(menssages["history_trabalhador"], "r").read()
history_cliente = open(menssages["history_cliente"], "r").read()
admin_history = open(menssages["history_admin"], "r").read()

captchas_temp = {} #CAPTCHAS RESOLVIDOS SERAO ARMAZENADO AQUI TEMPORARIAMENTE
events_temp = {} #GATILHO DE QUANDO A RESOLUSAO DO CAPTCHA FOR RESOLVIDO PERMITIR ENVIAR A RESPOTA
workers_temp = {} #ARMAZENA TEMPORARIAMENTE OS CAPTCHAS QUE ESTA SENDO RESOLVIDO
responses = {}


path = os.getcwd()

timer = 35

@web.route("/api/solution/send", methods=["GET"])
def send_solution():
    global captchas_temp, workers_temp, events_temp
    #PARAMETROS DO API
    id_worker = request.args.get("id_worker")
    id_captcha = request.args.get("id_captcha")
    text = request.args.get("text")

    #DELETAR DO BANCO DE DADOS O CAPTCHA QUE JA FOI RESOLVIDO
    try:
        workers_temp[id_worker] = User.solveCaptcha(id_captcha, id_worker)
        
    except:
        return jsonify({"status": "Captcha resolvido ou nao existe - 3"})
    
    #RMAZENA A RESPOSTA DO CAPTCHA RESOLVIDO
    workers_temp[id_worker]["text"] = str(text)
    workers_temp[id_worker]["id_captcha"] = id_captcha
    #RECOMPENSA DO TRABALHOR 
    #TIPO 0 = HUMANO(GANHA DINHEIRO)
    #TIPO 1 = EXTRA(GANHA PONTOS)
    if workers_temp[id_worker]["type"] == "text":
        #FAZER ALTERACAO DO DINHEIRO NO BANCO DS DADOS
        User.setSaldo(id_worker, "give", workers_temp[id_worker]["reward"])
        

        #BUSCAR DADOS DO USUARIO = TRABALHADOR
        worker = User.load(path+"/users/"+str(id_worker)+"/"+str(id_worker)+".json")
        client = User.getClient(token)
        #CONFIGURANDO DADOS
        username_worker = worker["username"]
        saldo = worker["saldo"]
        channel_history = worker["history_channel"]

        #ABRIR O CAPTCHA
        img = open(f"data/imgs/{id_captcha}.png", "rb")

        #CHECAR SE O HISTORICO ESTA ATIVADO
        if channel_history != None:
            #SEPARAR O ID DO CANAL DO HISTORICO
            chat_id = channel_history["channel_id"]

            #FORMATAR O TEXTO
            format_text = history_trabalhador.format(id_captcha=id_captcha, recompensa=workers_temp[id_worker]["reward"], saldo=User.formatSaldo(saldo), text=workers_temp[id_worker]["text"])
            
            #ENVIAR O TEXTO E A IMAGEM
            bot.send_photo(chat_id, img)
            bot.send_message(chat_id, format_text, parse_mode="HTML")

        #####ENVIAR PARA O ADMIN####
        chat_id = channel_admin["admin_history"]

        format_text = admin_history.format(id_trabalhador=id_worker, user_trabalhador=username_worker, id_cliente=client[1], user_cliente=client[0], token=token, id_captcha=id_captcha, recompensa=workers_temp[id_worker]["reward"], resposta=workers_temp[id_worker]["text"])
        bot.send_photo(chat_id, img)
        bot.send_message(chat_id, format_text, parse_mode="HTML")
        
        #ENVIAR PARA O CLIENT
        if client["history_channel"] != None:
            format_text = history_cliente.format(id_trabalhador=id_worker, resposta=text, id_captcha=id_captcha)
            bot.send_photo(client["id"], format_text, parse_mode="HTML")
        pass

    elif workers_temp[id_worker]["type"] == "None":
        #FAZER ALTERACAO DOS PONTOS NO BANCO DE DADOS
        #NAO FIZ A FUNCAO DE PONTOS POR ENQUANTO
        User.setSaldo(id_worker, "give", workers_temp[id_worker]["reward"])
        pass
    
    #DELETANDO ALGUMS DADOS
    del workers_temp[id_worker]["reward"]
    del workers_temp[id_worker]["type"]

    #GUARDA A TOKEN POR ENQUANTO
    token = workers_temp[id_worker]["token"]

    #SEPARAR DADOS PARA O CLIENT DO CAPTCHA
    captchas_temp[token] = workers_temp[id_worker]

    del captchas_temp[token]["token"]
    del workers_temp[id_worker]

    #ATIAVAR O GATILHO
    events_temp[token].set()
    User.setCaptcha(token, "deduct", 1)
    return jsonify({"status": "Resolucao do captcha enviado!! - 0"})

@web.route("/api/solution/solver", methods=["POST"])
def upload_captcha():
    global events_temp, workers_temp, captchas_temp
    #KEY DO API DO CLIENT
    token = request.form.get("token")
    
    if os.path.isfile(path+"/api_users/"+str(token)+".json"):
        client_config = User.load(path+"/api_users/"+str(token)+".json")
        saldo = client_config["captchas"]
        ban = client_config["ban"]
        if saldo > 0:
            pass
        elif saldo == 0:
            return jsonify({"status": "Você não tem captchas para enviar - 6"})
        elif ban == 1:
            return jsonify({"status": "Você esta banido - 69"})
    else:
        return jsonify({"status": "Token não registrado - 2"})

    #GERAR ID PARA O NOME DO ARQUIVO E DA RESOLUCAO
    id = token_hex(13)
    print(id)

    EVENT = Event() #PARA CRIAR UM NOVO GATILHO
    #CRIANDO E SALVANDO O GATILHO NO EVENTOS TEMPORARIOS
    events_temp[token] = EVENT

    #VERIFICAR SE TEM ALGUMA IMG NO CAMINHO
    if "captcha" not in request.files:
        return jsonify({"status": "Nenhuma imagem foi encontrada - 4"})
    
    #NOME DO ARQUIVO + CAMINHO PARA SER SALVO
    name_file = path+"/data/imgs/"+str(id)+".png"

    #PEGANDO O ARQUIVO
    captcha = request.files["captcha"]
    #SALVANDO O ARQUIVO
    captcha.save(name_file)

    #SALVAR O CAPTCHA PARA RESOLVER NO BANCO DE DADOS
    User.sendCaptcha(id, token, client_config["reward"])
    
    #SE O EVENTO ATIGIU O TEMPO LIMITE DO GATILHO
    if not events_temp[token].wait(timer):
        #SE SIM VAI REMOVER E DELETAR TUDO QUE FOI CRIADO
        os.remove(name_file)
        User.solveCaptcha(id, "null")
        return jsonify({"status": "Captcha não resolvido - 5"})
        
    responses[token] = captchas_temp[token]

    #DELETAR PARA NAO FICAR GUARDANDO COISA NA MEMORIA
    del captchas_temp[token]
    del events_temp[token]
    os.remove(name_file)

    return jsonify(responses[token])


@web.route("/webhook")
def webhook():
    data = request.get_json()

    if data['action'] == 'payment.created':
        payment_id = data['data']['id']
        status = data['data']['status']
        amount = data['data']['transaction_amount']

        if status == "approved":
            mini_data = data['data']['external_reference']
            mini_data = mini_data.split(":")

            user_id = mini_data[0]
            amount_captchas = int(mini_data[1])

            message = f"Seu pagamento de R${amount:.2f} foi aprovado. Obrigado!"
            token = User.getToken(user_id)
            User.setCaptcha(token, "give", amount_captchas)
            User.setPlan(token, "0.01")
            bot.send_message(user_id, message)

    pass


@web.route("/trabalho")
def trabalho():
    return trabalhador_page

@web.route("/cliente")
def tabela_precos():
    return cliente_page

@web.route("/docs")
def docs():
    return docs_page


web.run()