# Save your prompts on the main prompts.txt file, try to describe as brief as you can.

def load_prompt():
    with open('../prompts.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    return data