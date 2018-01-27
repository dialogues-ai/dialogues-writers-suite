import requests,bs4
from stringProcessing import *

def get_dict_word(word):
    try:
        response=requests.get('http://www.dictionary.com/browse/'+word)
        response.raise_for_status()
        fetched_data=bs4.BeautifulSoup(response.text)
        elements=fetched_data.select('section[class="def-pbk ce-spot"]')
        with open("Output.txt", "w") as text_file:
            print("Dictionary: {}".format(Words), file=text_file)
        return elements[0].getText()
    except (requests.HTTPError , requests.ConnectionError):
        return ''

def get_dict_string(word):
    return get_dict_word(word)

def get_dict_definition(word):
    meaning=get_dict_string(word)
    if len(meaning)>0:
        return format_definition(meaning)
    else:
        return ''
