import os
from jinja2 import Template

# Need to implement a semantic syntax matcher that purifies the GPT generated commands response 
_ZEXUI_INSTRUCTIONS_TEMPLATE = Template("""from ZexUI.zexui import ZexUI

zex = ZexUI()
{{ _code }}
""")

# current directory
location = os.path.dirname(os.path.realpath(__file__))

# Get the path of the parent directory (i.e., one level up)
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Construct the path to the file to be written in the parent directory
file_path = os.path.join(parent_dir, 'script.py')


def generate_script(_code):
    print(location)
    with open(file_path, 'w', encoding='utf-8') as f:
        _content = _ZEXUI_INSTRUCTIONS_TEMPLATE.render(_code=_code)
        data = f.write(_content)
    print("[Automation script has been generated.]")


def execute_commands(_code):
    pass