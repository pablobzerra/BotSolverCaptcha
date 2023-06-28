from libs.db import *
from telebot import TeleBot
from libs.TelegramBotoes import *
from libs.TelegramRequestApi import *
from libs.MercadoPago import *
import json, requests, codecs
from os.path import isfile as Exists
import threading
#EMOJIS
emojis = ["\U0001F464", 
          "\U0001F4BC", 
          "\U0001F467", 
          "\U0001F680", 
          "\U0001F512", 
          "\U0001F64C",
          "\U00002714",
          "\U0000274E",
          "\U0001F7E9",
          "\U0001F7E5",
          "\U00000031\U0000FE0F\U000020E3",
          "\U00000032\U0000FE0F\U000020E3",
          "\U00000033\U0000FE0F\U000020E3",
          "\U00000034\U0000FE0F\U000020E3",
          "\U00000035\U0000FE0F\U000020E3",
          "\U00000036\U0000FE0F\U000020E3",
          "\U00000037\U0000FE0F\U000020E3"]

#emoji: 0 = Rosto azul
#emoji: 1 = maleta 
#emoji: 2 = rosto com pc
#emoji: 3 = foguete
#emoji: 4 = cadeado
#emoji: 5 = Maos para cima 
#emoji: 6 = ✓
#emoji: 7 = X
#emoji: 8 = Quadrado Verde
#emoji: 9 = Quadrado Vermelho
#emoji: 10 = 1
#emoji: 11 = 2
#emoji: 12 = 3
#emoji: 13 = 4
#emoji: 14 = 5
#emoji: 15 = 6
#emoji: 16 = 7


#BOTOES
btn = TelegramBotoes()
user_btn = UserBtns()

#CARREGAR O ARQUIVO DE CONFIGURAÇAO
file_config = open("config.json", "r").read()
config = json.loads(file_config)
email = config["email"]
path = os.getcwd()
#CARREGAR ID DOS CANAIS
channels = config["channels"]

#MERCADO PAGO
mercado_pago = config["mercado_pago"]
mp = MercadoPago(mercado_pago["token_id"], mercado_pago["token_private"])
#CARRAGAR MENSSAGES 
menssages_bot = config["menssages"]

trabalhadores = []
captchas_r = {} #captchas sendo resolvidos
check_trabalhador = {}


#MENSSAGES
menu_bem_vindo = open(menssages_bot["bem_vindo"], "r").read().format(id0=emojis[0], id1=emojis[1])
trabalhador_iniciando = open(menssages_bot["trabalhador_iniciando"], "r").read().format(emoji0=emojis[0], emoji1=emojis[6], emoji2=emojis[1], emoji3=emojis[3], emoji4=emojis[4], emoji5=emojis[5])
cliente_iniciando = open(menssages_bot["cliente_iniciando"], "r").read().format(emoji0=emojis[0], emoji1=emojis[6], emoji2=emojis[1], emoji3=emojis[3], emoji4=emojis[4],emoji5=emojis[5])
trabalhador_registrado = open(menssages_bot["trabalhador_registrado"], "r").read()
cliente_registrado = open(menssages_bot["cliente_registrado"], "r").read()
perfil_trabalhador = open(menssages_bot["perfil_trabalhador"], "r").read()
perfil_cliente = open(menssages_bot["perfil_cliente"], "r").read()
tutorial_historico = open(menssages_bot["tutorial_historico"], "r").read()
tabela_preco = open(menssages_bot["tabela_precos"], "r").read()
preco_personalizado = open(menssages_bot["preco_personalizado"], "r").read()

#ID DO TOKEN
token = config["token"]

message_users = {} #DESNECESSARIO MAS ESTA AQUI
etapas_users = {}
preco = {}
sacar = {}
config_pag = {}

#CANAIS
TROLLS_CHANNEL = channels["trolls_channel"]
ERRADOS_CHANNEL = channels["errados_channel"]
#CLIENTES_CHANNEL = channels["clientes_channel"]
#TRABALHADORES_CHANNEL = channels["trabalhadores_channel"]

bot = TeleBot(token)
#Funcao adicionais para telegram
funcTele = TelegramApi(token, bot)



check_trabalhos = False
while check_trabalhos == True:
    print("TESTE")
    captchas = User.getCaptchas()
    if len(trabalhadores) != 0:
        for id in captchas:
            captcha = User.getCaptcha(id)
            trabalhador = trabalhadores[0]
            if trabalhador == captcha["skip"]:
                pass
            else:
                if check_trabalhador[trabalhador] == True:
                    captchas_r[trabalhador] = id
                    User.setTrabalhador(trabalhador, id)
                    img = open(path+"/data/imgs/"+str(id)+".png", "rb")
                    bot.send_photo(trabalhador, img, reply_markup=btn.captcha_menu())

@bot.message_handler(commands=["start", "stopTrabalho", "trabalhos"]) 
def h_commands(data):
    global message_users, captchas_r, trabalhadores, check_trabalhador, check_trabalhos
    message = data.text
    user_id = data.from_user.id
    chat_id = data.chat.id
    print(message)
    if message == "/start" and Exists(path+"/users/"+str(user_id)+"/"+str(user_id)+".json"):

        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")

        type = user["type"]

        if type == "Trabalhador":
            bot.send_message(chat_id,"bem vindo", reply_markup=user_btn.trabalhador())
        elif type == "Cliente":
            bot.send_message(chat_id,"bem vindo", reply_markup=user_btn.cliente())
            pass
    elif message == "/stopTrabalho":
        check_trabalhador[user_id] = False

    elif message == "/trabalhos":
        check_trabalhos = True
        print("aaaa")
            
    else:
        msg = bot.send_message(chat_id, menu_bem_vindo, reply_markup=btn.create_work_client_buttons(), parse_mode="HTML")
        message_users[user_id] = msg.id
    pass

#CANAIS COMAND
@bot.channel_post_handler(commands=["setHistorico"])
def message_channel(data):
    command = data.text
    chat_id = data.chat.id
    print(command)
    check_group = funcTele.getGroup(chat_id)
    if command  == "/setHistorico":
        if check_group[0] != 0:
            User.setHistorico(check_group[0], check_group[1], check_group[2])
            bot.send_message(chat_id, f"Este chat foi definido com sucesso")
            bot.send_message(check_group[2], f"O {check_group[1]} foi definido com sucesso")
        else:
            bot.send_message(chat_id, "Ocorreu um erro ao definir este chat")
            
#CHAT PRIVADO 
@bot.message_handler(func=lambda data: True)
def h_messages(data):
    global etapas_users, preco, captchas_r, trabalhadores, check_trabalhador

    text = data.text #.replace("\U0001F464 ", "")
    user_id = data.from_user.id
    chat_id = data.chat.id

    print(text)
    if text == "\U0001F464 Perfil":
        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")

        id = user["id"]
        username = user["username"]
        type = user["type"]

        if type == "Trabalhador":
            saldo = user["saldo"]
            bot.send_message(chat_id, perfil_trabalhador.format(id=id, username=username, saldo=saldo), parse_mode="HTML", reply_markup=btn.sacar())
            pass
        elif type == "Cliente":
            token = user["token"]
            saldo = User.getClientCaptchas(token)

            bot.send_message(chat_id, perfil_cliente.format(id=id, username=username, token=token, captchas=saldo), parse_mode="HTML")
            pass
        
        
        pass
    elif text == "\U0001F198 Suporte":
        pass

    elif text == "\U0001F5C2 Histórico de Trabalhos":
        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")
        history_id = user["history_channel"]
        if history_id == None:
            bot.send_message(chat_id, tutorial_historico)
        else:
            bot.send_message(chat_id, "Bot configurado corretamente")
            pass
        pass
    elif text == "\U0001F468\U0000200D\U0001F527 Comprar Serviço":
        bot.send_message(chat_id, tabela_preco, reply_markup=btn.precos())
        pass

    
    elif text == "\U00002699\ufe0f Configuração de pagamento":
        bot.send_message(chat_id, "Selecio o tipo de chave pix", reply_markup=btn.chaves_pix())
        pass
    
    elif text == "\U0001F4BC Trabalhar":
        if user_id in trabalhadores:
            bot.send_message(chat_id, "Vocé ja esta trabalhando")
        else:
            trabalhadores.append(user_id)
            check_trabalhador[user_id] = True
            bot.send_message(user_id, "aguarde o captcha chegar")
        pass

    if len(etapas_users) != 0:
        try:
            if etapas_users[user_id]["genPix"] == 0:
                r = str(float(int(text) / 10 / 10)) + "0"
                r = r.replace('"', "")
                preco[user_id] = [r, text]
                bot.send_message(chat_id, preco_personalizado.format(c=text, preco=r), reply_markup=btn.confirma_pix())
            
            elif etapas_users[user_id]["sacar"] == 0:
                if int(text) >= 5:
                    sacar[user_id] = text
                    bot.send_message(chat_id, f"Vocé confirma esse valor? R${int(text)}", reply_markup=btn.confirmar_sacar())
                else:
                    bot.send_message(chat_id, "Saldo insuficiente")
            elif etapas_users[user_id]["config_pag"] == 0:
                config_pag[user_id]["chave"] = text
                bot.send_message(chat_id, f"Você confirma?\Chave: {text}", reply_markup=btn.confirmar_dados())
                pass

            elif etapas_users[user_id]["captcha"] == 0:
                etapas_users[user_id]["captcha"] = 1
                r = requests.get("http://127.0.0.1:5000/api/solution/send?id_worker={}&id_captcha={}&text={}".format(user_id, captchas_r[user_id], text))
                del captchas_r[user_id]
                if r.status_code == 200:
                    bot.send_message(user_id, "Respota enviada")
                pass
        except:
            pass
    pass

@bot.callback_query_handler(func=lambda data: True)
def c_messages(data):
    global message_users, etapas_users, preco, trabalhadores, captchas_r, check_trabalhador
    callback = data.data
    chat_id = data.message.chat.id
    user_id = data.from_user.id
    username = data.from_user.username

    #OPCOES TRABALHADOR
    if callback == "OpTrabalhar":
        if Exists(path+"/users/"+str(user_id)+"/"+str(user_id)+".json"):
            pass
        else:
            bot.delete_message(chat_id, message_users[user_id])
            bot.send_message(chat_id, trabalhador_iniciando,reply_markup=btn.create_work_button(),parse_mode="HTML")
        pass

    #OPCOES CLIENTE
    elif callback == "OpClient":
        if Exists(path+"/users/"+str(user_id)+"/"+str(user_id)+".json"):
            pass
        else:
            bot.delete_message(chat_id, message_users[user_id])
            bot.send_message(chat_id, cliente_iniciando, parse_mode="HTML", reply_markup=btn.create_cliente_button())
        pass

    #REGISTRAR TRABALHADOR
    elif callback == "registrar_trabalhador":
        User.register(user_id, username)
        User.setType(user_id, "Trabalhador")
        bot.send_message(chat_id, trabalhador_registrado, parse_mode="HTML", reply_markup=user_btn.trabalhador())
        pass

    elif callback == "registrar_cliente":
        User.register(user_id, username)
        User.setType(user_id, "Cliente")
        User.genTokenApi(user_id)
        bot.send_message(chat_id, cliente_registrado, parse_mode="HTML", reply_markup=user_btn.cliente())
        pass

    #precos
    elif callback == "preco_01":
        preco[user_id] = [5.00, 500]
        bot.send_message(chat_id, preco_personalizado.format(c=1000, preco=10.00), reply_markup=btn.confirma_pix())  
        pass
    elif callback == "preco_02":
        preco[user_id] = [10.00, 1000]
  
        bot.send_message(chat_id, preco_personalizado.format(c=1000, preco=10.00), reply_markup=btn.confirma_pix())
        pass
    elif callback == "preco_03":
        preco[user_id] = [20.00, 2000]
        bot.send_message(chat_id, preco_personalizado.format(c=2000, preco=20.00), reply_markup=btn.confirma_pix())
                
        pass
    elif callback == "preco_04":
        preco[user_id] = [30.00, 3000]
        bot.send_message(chat_id, preco_personalizado.format(c=3000, preco=30.00), reply_markup=btn.confirma_pix())
        
        pass
    elif callback == "preco_05":
        preco[user_id] = [40.00, 4000]
        
        bot.send_message(chat_id, preco_personalizado.format(c=4000, preco=40.00), reply_markup=btn.confirma_pix())
                       
        pass
    elif callback == "preco_06":
        preco[user_id] = [50.00, 5000]
        bot.send_message(chat_id, preco_personalizado.format(c=5000, preco=50.00), reply_markup=btn.confirma_pix())
                 
        pass
    elif callback == "preco_personalizado":
        etapas_users[user_id]["genPix"] = 0
        bot.send_message(chat_id, "Digite a quantidade de captchas que deseja")
        pass

    elif callback == "confirmar_compra":
        del etapas_users[user_id]["genPix"]
        pix = mp.genPix(user_id, preco[user_id][0], preco[user_id][1], F"{preco[user_id][1]} captchas", config[""])
        bot.send_message(chat_id, pix)
        pass

    elif callback == "cancelar_compra":
        del etapas_users[user_id]["genPix"]

    elif callback == "sacar":
        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")
        
        check = user["pix"]["type"]
        
        if check != None:
            etapas_users[user_id]["sacar"] = 0
            bot.send_message(chat_id, "Digite a quantia que deseja retirar\nMin:R$5.00")

        else:
            bot.send_message(user_id, "configure seu metodo de pagamento antes")
        pass

    elif callback == "confirmar_sacar":
        User.setSaldo(user_id, "deduct", sacar[user_id])
        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")
        pix = user["pix"]
        o = mercado_pago.pay(email, pix["chave"], sacar[user_id], "Pagamento do seu trabalho", pix["type"])
        del sacar[user_id]
        del etapas_users[user_id]
        bot.send_message(chat_id, o)

    elif callback == "cancelar_compra":
        del sacar[user_id]
        del etapas_users[user_id]
        bot.send_message(chat_id, "Cancelado!!")

    elif callback == "chave_email":
        etapas_users[user_id]["config_pag"] = 0
        config_pag[user_id]["type"] = "email"
        bot.send_message(chat_id, "Digite seu Email\nExem: exemplo@gmail.com:")
        pass
    elif callback == "chave_phone":
        etapas_users[user_id]["config_pag"] = 0
        config_pag[user_id]["type"] = "phone"
        bot.send_message(chat_id, "Digite seu Telefone\nExem: +5500000000000:")
        pass
    elif callback == "chave_cpf":
        etapas_users[user_id]["config_pag"] = 0
        config_pag[user_id]["type"] = "cpf"
        bot.send_message(chat_id, "Digite seu Cpf\nExem: 00000000000:")
        pass

    elif callback == "confirmar_dados":
        chave = config_pag[user_id]["chave"]
        type = config_pag[user_id]["type"]
        User.setPix(user_id, type, email)
        del config_pag[user_id]
        del etapas_users[user_id]
        bot.send_message(chat_id, "Metodo de pagamento configurado!!")

    elif callback == "cancelar_dados":
        del config_pag[user_id]
        del etapas_users[user_id]
        bot.send_message(chat_id, "Cancelao")
    
    elif callback == "skip_captcha":
        id_captcha = captchas_r[user_id]
        User.removeTrabalhador(user_id, id_captcha)
        User.setSkip(user_id, id_captcha)
        pass


bot.polling(none_stop=True, timeout=10)