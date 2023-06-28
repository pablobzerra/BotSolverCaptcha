from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

class TelegramBotoes:
    def __init__(self):
        self.markup = InlineKeyboardMarkup()

    def create_work_client_buttons(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Trabalhar Agora", callback_data="OpTrabalhar"),
            InlineKeyboardButton("Opções para Clientes", callback_data="OpClient")
        )

        return self.markup
    

    def create_work_button(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Registrar-se", callback_data="registrar_trabalhador")
        )
        
        return self.markup
    
    def create_cliente_button(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Registra-se", callback_data="registrar_cliente")
        )
        
        return self.markup
    
    def precos(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("R$5", callback_data="preco_01"),
            InlineKeyboardButton("R$10", callback_data="preco_02"),
        )

        self.markup.add(
            InlineKeyboardButton("R$20", callback_data="preco_03"),
            InlineKeyboardButton("R$30", callback_data="preco_04")
        )

        self.markup.add(
            InlineKeyboardButton("R$40", callback_data="preco_05"),
            InlineKeyboardButton("R$50", callback_data="preco_06")
        )

        self.markup.add(
            InlineKeyboardButton("Personalizado", callback_data="preco_personalizado")
        )


        return self.markup
    

    def confirma_pix(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Confirmar", callback_data="confirmar_compra"),
            InlineKeyboardButton("Cancelar", callback_data="cancelar_compra")
        )

        return self.markup
    
    def confirmar_sacar(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Confirmar", callback="confirmar_sacar"),
            InlineKeyboardButton("Cancelar", callback_data="cancelar_sacar")
        )

        return self.markup


    def confirmar_dados(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Confirmar", callback="confirmar_dados"),
            InlineKeyboardButton("Cancelar", callback_data="cancelar_dados")
        )
        return self.markup
    

    def sacar(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2

        self.markup.add(
            InlineKeyboardButton("Sacar", callback_data="sacar")
        )
        return self.markup

    def chaves_pix(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("email", callback_data="chave_email"),
            InlineKeyboardButton("phone", callback_data="chave_phone"),
            InlineKeyboardButton("cpf", callback_data="chave_cpf")
        )

        return self.markup
    
    def captcha_menu(self):
        self.markup = InlineKeyboardMarkup()
        self.markup.row_width = 2
        self.markup.add(
            InlineKeyboardButton("Skip", callback_data="skip_captcha")
        )
        return self.markup

class UserBtns:
    def trabalhador(self):
        buttons = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        buttons.row(
            KeyboardButton("\U0001F464 Perfil"),
            KeyboardButton("\U0001F4BC Trabalhar"),
            KeyboardButton("\U0001F198 Suporte")
        ) 
        buttons.row(
            KeyboardButton("\U00002699\ufe0f Configuração de pagamento"),
        )
        buttons.add(
            KeyboardButton("\U0001F5C2 Histórico de Trabalhos")
        )
        return buttons
    
    def cliente(self):
        buttons = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        buttons.add(
            KeyboardButton("\U0001F464 Perfil"),
            KeyboardButton("\U0001F468\U0000200D\U0001F527 Comprar Serviço")
        )

        buttons.add(
            KeyboardButton("\U0001F5C2 Histórico de Trabalhos")
        )

        buttons.add(
            KeyboardButton("\U0001F198 Suporte")
        )
        

        return buttons
    
    