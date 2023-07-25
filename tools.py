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
