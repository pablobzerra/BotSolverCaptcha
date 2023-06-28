import requests, os

path = os.getcwd()

class TelegramApi:
    def __init__(self, Token, Bot):
        self.token = Token
        self.bot = Bot

    def getGroup(self, chat_id):
            chat = self.bot.get_chat(chat_id)
            users = os.listdir("users/")
            for user in users:
                if chat.type == "channel":
                    try:
                        check = self.bot.get_chat_member(chat_id, int(user)).status
                        if check == "creator":
                            return chat_id,chat.title, int(user)
                            break
                    except:
                        return 0, 0, 0
                        pass
