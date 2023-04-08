from instructions_lib.generate_commands import generate, execute_commands
from instructions_lib.process_instructions import generate_script, execute_commands 
import subprocess 

_prompt = 'Query: click on the item with text "Document Writer" after that click on the image with path "image.png" after that scroll down and then find element that is top of text "File" , double left click it.'



commands = generate(_prompt)
generate_script(commands)


subprocess.run('python script.py', shell=True)
# execute_commands(commands)