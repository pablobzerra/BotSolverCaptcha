from libs.db import *
import os
from time import sleep
while True:
    captchas = User.getCaptchas()
    os.system("clear")
    for i in captchas:
        print(i)
        sleep(10)
    sleep(5)
