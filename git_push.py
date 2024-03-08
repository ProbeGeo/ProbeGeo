import os
import time


while True:
    os.system('git add . && git commit -m "update datasets" && git push')
    time.sleep(86400)
