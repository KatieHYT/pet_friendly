import json
import openai

def get_file_contents(filename):
    """ 
    src: https://github.com/dylburger/reading-api-key-from-file/blob/master/Keeping%20API%20Keys%20Secret.ipynb
        Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

def save_string_to_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
        print("String successfully saved to file.")
    except Exception as e:
        print(f"Error occurred while saving the string: {e}")

def read_json(f_path):
   with open(f_path, 'r') as f:
       data = json.load(f)

   return data

def talk2gpt(txt, if_stream=False):
    msg = {
        "role": "user",
        "content": txt,
         #"temperature": 0.7,
    #     "top_p": 0.1,
        "name": "cradle",
    }

    # create a chat completion
    # TODO: stream the chat completion
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            msg
        ],
        stream=if_stream,
    #     temperature=1,
    #     top_p=0.1,
    #     n=3,
    )
    
    if if_stream:
        return chat_completion
    else:
        return chat_completion.choices[0].message.content

    
def remove_empty_lines(input_string):
    lines = input_string.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

