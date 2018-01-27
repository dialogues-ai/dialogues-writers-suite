import csv
import booksBackend

f = open('emotional-arc_data.csv', newline='')
bookreader = csv.reader(f)

csvcols = {'Index':0, 'Gut_ID':1, 'Title':2, 'Genre':3, 'Subgenre':4,
           'Genre2':5, 'Genre3':6, 'Last Name':8, 'First Name':9,
           'Honorifics':10, 'Birth':11, 'Death':12, 'Length':13,
           'NumUniqWords':14, 'Downloads':15}
emoArcOffset = 16
emoArcPoints = 200

for index,row in enumerate(bookreader):
    if index == 0:  # ignore the csv header
        continue
    # csv interprets arc data points as strings, so convert them here
    emoarc = [float(e) for e in row[emoArcOffset:emoArcOffset+emoArcPoints]]
    booksBackend.insert(row[csvcols['Gut_ID']], row[csvcols['Title']],
                            row[csvcols['Genre']], row[csvcols['Last Name']]
                            + ', ' + row[csvcols['First Name']], emoarc=emoarc)


#cur.execute("SELECT points FROM emoarc WHERE bookid in (SELECT bookid from book where title=?)"
# rows = cur.fetchall() 
#    points=json.loads(rows[0][0]) 
#    len(points) 