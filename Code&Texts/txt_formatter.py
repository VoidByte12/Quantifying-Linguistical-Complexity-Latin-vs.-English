import re
import string
import os

def format_txt(txt):

    current_dir = os.path.dirname(os.path.abspath(__file__))# Get the directory of the current script
    
    file_path = os.path.join(current_dir, "Texts", txt)  # Construct full path to the text file
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find file: {file_path}") # Check if file exists
    
    with open(file_path, 'r', encoding='utf-8') as file: # opens file in read mode
        file_content = file.read() 
        
    counter = 0
    char_list = []

    for char in file_content:  # removes all text within []
        if char == '[':
            counter = 1
            continue # Skip the '[' character itself
        elif char == ']':
            counter = 0
            continue
        if counter == 0:
            char_list.append(char)

    temp_text = ''.join(char_list)
    temp_text = re.sub(r'\b\d+\.\s*', '', temp_text) # regex matches numbers followed by a dot and optional space
    temp_text = re.sub(r'\n', '', temp_text) # removes all new line characters

    digits = '0123456789'
    temp_text = temp_text.translate(str.maketrans('', '', digits)) # removes all digits

    counter_2 = 0
    char_list_2 = list(temp_text)
    results_list = []

    for i in char_list_2: # ensures no more than one space in a row
        if i == ' ':
            counter_2 += 1
        else:
            counter_2 = 0
        if not (i == ' ' and counter_2 >= 2):
            results_list.append(i)  
            
    formatted_txt = ''.join(results_list).lower()   
    punctuation = string.punctuation.replace('-', '')  # Keep hyphens for compound words
    formatted_txt = formatted_txt.translate(str.maketrans('', '', punctuation)) # deletes all puncuation except hyphens
    return formatted_txt