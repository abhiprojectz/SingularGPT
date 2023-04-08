from zexui_lib.zexui import ZexUI
from time import sleep


zex = ZexUI()

zex.text('Writer Document').click()
sleep(4)
zex.write('Hello, i am SingularGPT developed by @abhiprojectz.')
sleep(3)
zex.write('Now, i will find the icon you specified, and click on it for you :)')
zex.image('/content/zx_1.PNG').click()
sleep(3)
zex.write('Have, you seen?')
zex.write('Now. i will close it.')
zex.mouseMoveTo('center')
zex.image('/content/zx_1.PNG').click()