
"""
Created on Mon Nov 20 14:16:10 2017

@jonnyjohnson: home
"""

###
### Dictionary Class
### make_Dict( medium = book, genre = , numWords = )
### Makes a dictionary using some book genre


# In[4]:

## 1. GET DATA

# Filter Genre

import sys
sys.path.append("/Volumes/NewVolume/Emotional-Arcs/tools/")
from gbmetadata import *
md = readmetadata()
filteredbooks = []
for book in md.keys():
    if md[book]['subjects']['Adventure stories'] in md[book]['subjects']:
        filteredbooks.append(book)


## 2. GET DICTIONARIES FROM BOOKS
## use books from filter

# load_raw_book_data (from bookclass)
class Book_raw_data(object):
    '''Book class to handle loading the calibre expanded epub format.
    Or just a text file.

    Now closely wrapping the database.

    Initialize with an instance of the database like this:
    b = Book.objects.all()[0]
    b_data = Book_raw_data(b)

    Store all of the word lists, etc, in one place.'''

    def load_all_combined(self):
        # didn't do a perfect job creating the updated gutenberg
        # database...so still watch out for bad encodings
        #Old filepath type that I commented out to eperiment with new ones
        #filename = join("/Volumes/NewVolume/Emotional Arcs/database",self.this_Book.txt_file_path)
        
        filename = join("/Volumes/NewVolume/Emotional-Arcs/",self.this_Book.txt_file_path)
        ##if not isfile(filename):
        #print(filename)
            ##raise ValueError(filename + 'Hey man, why you no haz file?')
            ##pass
        try:
            print("opening:",filename)
            f = open(filename,"r")
            rawtext = f.read()
            print("Finished reading: ",filename)
            f.close()
        except:
            print("failed, opening with iso8859:",filename)
            f = open(filename,"r",encoding="iso8859")
            rawtext = f.read()
            f.close()
            # print("writing as unicode:",filename)
            f = open(filename,"w")
            f.write(rawtext)
            f.close()
        self.all_word_list = listify(rawtext)
        lines = get_maintext_lines_gutenberg(rawtext)
    
    
    
    
## 3. FIND SIMILAR WORDS AMONG DICTIONARIES



    
    
## 4. RETURN DICTIONARY OF SET NUMBER OF WORDS

