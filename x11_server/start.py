import subprocess
from time import sleep
import re
from pyvirtualdisplay import Display
import os 


def start():
    disp = Display(size=(1536, 864), color_depth=24)
    disp.start()
    print(os.environ['DISPLAY'])

    subprocess.run(f"export DISPLAY={os.environ['DISPLAY']}", shell=True)
    sleep(3)
    # subprocess.run("sudo google-chrome --window-size=1536,864 --no-sandbox https://google.com &", shell=True)


    # Changing window dimensions
    window = subprocess.check_output("xdotool getmouselocation", shell=True)
    win__ = int(re.search(r'\d+', str(window).split(" ")[-1].strip()).group()) 
    print(win__)
    subprocess.run(f"xdotool windowmove {win__} 0 0", shell=True)
    print('x11 screen buffer successfully setup.')



if __name__ == '__main__':
    start()