import json, os, secrets
from decimal import Decimal, ROUND_HALF_UP, getcontext
path = os.getcwd()



class User:
    def register(id, username):
        user = {
            "id": None,
            "username": None,
            "saldo": None,
            "type": None,
            "token": None,
            "reports_A": 0,
            "reports_B": 0,
            "avisos": 0,
            "solved": 0,
            "ban": 0,
            "kd": 0,
            "history_channel": None,
            "pix": {
                "type": None,
                "chave": None
            }
        }

        if os.path.exists(path+"/users"+str(id)):
            return True
        
        else:
            os.mkdir(path+"/users/"+str(id))

            user["id"] = id
            user["username"] = username
            user["saldo"] = "0.000"
            
            User.save(path+"/users/"+str(id)+"/"+str(id)+".json", user)

            return False
        
    def setSaldo(id, expressao, saldo):
        user = User.load(path+"/users/"+str(id)+"/"+str(id)+".json")

        c = getcontext()
        c.rounding =  ROUND_HALF_UP

        s = Decimal(user["saldo"]).quantize(Decimal("0.000", context=c))

        if "give" == expressao:
            result = s + Decimal(saldo).quantize(Decimal("0.000", context=c))
            user["saldo"] = str(result)
        elif "deduct" == expressao:
            result = s - Decimal(saldo).quantize(Decimal("0.000", context=c))
            user["saldo"] = str(result) 


        User.save(path+"/users/"+str(id)+"/"+str(id)+".json", user)

    def setType(id, type):
        user = User.load(path+"/users/"+str(id)+"/"+str(id)+".json")
        user["type"] = type
        User.save(path+"/users/"+str(id)+"/"+str(id)+".json", user)

    #Seta a quantidade de captchas
    def setCaptcha(api_key, expressao, captchas):
        api_data = User.load(path+"/api_users/"+str(api_key)+".json")
        captchas_temp = api_data["captchas"]
        
        if "give" == expressao:
            api_data["captchas"] = captchas_temp + captchas
        elif "deduct" == expressao:
            api_data["captchas"] = captchas_temp - captchas
        User.save(path+"/api_users/"+str(api_key)+".json", api_data)
    
    def setHistorico(chat_id, channel_name, user_id):
        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")
        user["history_channel"] = {
            "channel_id": chat_id,
            "channel_name": channel_name
        }

        User.save(path+"/users/"+str(user_id)+"/"+str(user_id)+".json", user)
    
    def setPix(user_id, type, chave):
        user = User.load(path+"/users/"+str(user_id)+"/"+str(user_id)+".json")
        
        user["pix"]["type"] = type
        user["pix"]["chave"] = chave

        User.save(path+"/users/"+str(user_id)+"/"+str(user_id)+".json", user)
        pass
    def setPlan(token, reward, captchas=None):
        client = User.load(path+"/api_users/"+str(token)+".json")
        if captchas != None:
            client["captchas"] = captchas
        client["reward"] = reward
        client["type"] = "text"
        User.save(path+"/api_users/"+str(token)+".json", client)
        pass


    def genTokenApi(id_user):
        token = secrets.token_hex(25)
        api_data = {
            "id": id_user,
            "token": token,
            "captchas": 0,
            "reward": "0.000",
            "ban": 0
        }

        user = User.load(path+"/users/"+str(id_user)+"/"+str(id_user)+".json")
        user["token"] = token
        User.save(path+"/users/"+str(id_user)+"/"+str(id_user)+".json", user)

        if os.path.isfile(path+"/api_users/"+str(token)+".json"):
            pass
        else:
            User.save(path+"/api_users/"+str(token)+".json", api_data)
    
    def getToken(id_user):
        user = User.load(path+"/users/"+str(id_user)+"/"+str(id_user)+".json")
        return user["token"]
    
    def getClientCaptchas(token):
        user = User.load(path+"/api_users/"+str(token)+".json")
        saldo = user["captchas"]
        return saldo

    def sendCaptcha(id, token, reward, type="text"):
        captchas = User.load(path+"/data/captchas.json")
        #ID DO CAPTCHA + NOME DA IMAGEN
        captchas[id] = {
            "token": token, #TOKEN DO CLIENT
            "type": type,
            "reward": str(reward),
            "text": "",
            "id_worker": None,
            "skip": None
        }

        User.save(path+"/data/captchas.json", captchas)
    
    def solveCaptcha(id_captcha, id_worker):
        captchas = User.load(path+"/data/captchas.json")

        captcha = captchas[id_captcha]
        captcha["id_worker"] = id_worker

        del captchas[id_captcha]

        User.save(path+"/data/captchas.json", captchas)
        return captcha
    
    
    def getCaptchas():
        captchas = User.load(path+"/data/captchas.json")
        ids = []
        for key, value in captchas.items():
            if value["id_worker"] == None:
                ids.append(key)

        return ids
    
    def getCaptcha(id_captcha):
        captchas = User.load(path+"/data/captchas.json")
        captcha = captchas[id]
        return captcha

    def formatSaldo(saldo, format="0.00"):
        c = getcontext()
        c.rounding =  ROUND_HALF_UP

        s = Decimal(saldo).quantize(Decimal(format, context=c))
        return s
    
    def getClient(token):
        user_api = User.load(path+"/api_users/"+str(token)+".json")
        user_id = user_api["id"]
        
        user = User.load(path+"/users/"+str(id)+"/"+str(id)+".json")
        username = user["username"]
        id = user["id"]
        return username, id

    def setSkip(user_id, id_captcha):
        captchas = User.load(path+"/data/captchas.json")
        captchas[id_captcha]["skyp"] = user_id
        User.save(path+"/data/captchas.json", captchas)


    def setTrabalhador(user_id, id_captcha):
        captchas = User.load(path+"/data/captchas.json")
        captchas[id_captcha]["id_worker"] = user_id
        User.save(path+"/data/captchas.json", captchas)
        

    def removeTrabalhador(user_id, id_captcha):
        captchas = User.load(path+"/data/captchas.json")
        captchas[id_captcha]["id_worker"] = None
        User.save(path+"/data/captchas.json", captchas)


        






    def save(path, data):
        with open(path, "w") as arquivo:
            json.dump(data, arquivo)

    def load(path):
        with open(path, "r") as arquivo:
            return json.load(arquivo)


if __name__ == "__main__":
    User.register(102, "Biel")
    User.setType(102, "Cliente")
    User.genTokenApi(102)
    #User.setPlan(User.getToken(102), 1000, "0.005")

    