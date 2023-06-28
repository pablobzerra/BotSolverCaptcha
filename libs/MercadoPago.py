from mercadopago import SDK
import requests

url  = "https://api.mercadopago.com"

class MercadoPago:
    def __init__(self, token_public, token_private):
        self.token_public = token_public
        self.token_private = token_private
        self.mp = SDK(self.token_private)
        self.base_pagamento = {
            "payer": {
                "email": None
            },
            "transaction_amount": None,
            "description": None,
            "payment_method_id": "pix"
        }

        self.base_genpix = {
            "transaction_amount": None,
            "description": None,
            "payment_method_id": "pix",
            "payer": {
                "email": None
            },
            "external_reference": None
        }

        self.headers = {
            "Authorization": f"Bearer {token_private}"
        }

        self.pagamento_data = None 
        pass

    def genPix(self, user_id, amount,amount_captchas,description, email="seu_email@gmail.com"):
        pix_data = self.base_genpix

        pix_data["transaction_amount"] = amount
        pix_data["description"] = description
        pix_data["payer"]["email"] = email
        pix_data["external_reference"] = user_id+":"+amount_captchas
        o = self.mp.payment().create(pix_data)

        pix = o["pix"]["code"]
        id_payment = o["id"]

        return id_payment, pix


    def pay(self, pay, receiver,amount, desctiption, type="email"):
        andpoint = "/v1/payments"

        self.pagamento_data = self.base_pagamento

        if type == "email":
            self.pagamento_data["payer"]["email"] = pay
            self.pagamento_data["receiver"] = receiver
            self.pagamento_data["transaction_amount"] = amount
            self.pagamento_data["description"] = desctiption
            pass
        elif type == "cpf":
            self.pagamento_data["payer"]["email"] = pay
            self.pagamento_data["identification"]["type"] = "CPF"
            self.pagamento_data["identification"]["number"] = receiver
            self.pagamento_data["transaction_amount"] = amount
            self.pagamento_data["description"] = desctiption
            pass
        elif type == "phone":
            self.pagamento_data["payer"]["email"] = pay
            self.pagamento_data["identification"]["type"] = "phone"
            self.pagamento_data["identification"]["number"] = receiver
            self.pagamento_data["transaction_amount"] = amount
            self.pagamento_data["description"] = desctiption
            pass

        response = requests.post(url + andpoint, json=self.pagamento_data, headers=self.headers)

        if response.status_code == 200:
            print("Pagamento efetuado com sucesso!")
            return "Tudo Correto"
        else:
            print("Erro ao efetuar o pagamento:", response.json())
            return "Ops aconteceu um problema"
 