from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
import os.path
from whoosh.index import create_in
import re, sys, sqlite3
from whoosh.index import open_dir

schema = Schema(title=TEXT(stored=True), author=TEXT(stored=True), editorial_review=TEXT, filename=TEXT(stored=True))
if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)
ix = open_dir("index")
writer = ix.writer()

conn = sqlite3.connect('books.db')
conn.text_factory = str
c = conn.cursor()  

for row in c.execute("SELECT title, author, editorial_review, filename  FROM books"):
  if u'The Heist' in row[3].decode('utf-8', 'ignore'):
    continue   
  filename_keywords = re.sub(u"[-_]", u" ", row[3].decode('utf-8', 'ignore'))
  filename_keywords = filename_keywords.replace('.mobi', '')
  writer.add_document(title=row[0].decode('utf-8'), 
                      author=row[1].decode('utf-8'), 
            editorial_review=row[2].decode('utf-8'),
            filename=filename_keywords )

writer.commit()