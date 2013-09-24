#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
script to convert dict html to sqlite database
"""
import re
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from lxml import etree
import codecs

engine = create_engine('sqlite:///d:/dict.db')
Base = declarative_base() 

class Word(Base):
  __tablename__ = 'words'
  prefix = Column(Integer, primary_key=True)
  word = Column(String, primary_key=True)
  postfix = Column(Integer, primary_key=True)
  html = Column(String)

  def __init__(self, prefix, word, postfix, html):
    self.prefix = -1
    if prefix:
      self.prefix = int(prefix)

    self.word = word
    self.word = self.word.replace("'", "\'").decode('UTF-8')

    self.postfix = -1
    if postfix:
      self.postfix = int(postfix)

    self.html = html
    self.html = self.html.replace("'", "\'").decode('UTF-8')

  def __repr__(self):
    return "<Word('%d','%s', '%d', %s)>" % (self.prefix, self.word, self.postfix, self.html)

metadata = MetaData()
players_table = Table('words', metadata,
     Column('prefix', Integer),
     Column('word', String),
     Column('postfix', Integer),
     Column('html', String)
  )

metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()

permit_chars = '[çü&()/äñîâûêèé,\w\-\.\s\'à]'
dict_html = open(r"D:\Dropbox\code\amaozn\dict_html.html")
for line in dict_html:
  m = re.match('<span><font size="3">H<sub>2</sub>O</font></span>', line)
  if m:
    continue  #skip H2O
  
  word, prefix, postfix = None, None, None
  m = re.match('<span><font size="3">(%s+)</font></span>' % permit_chars, line)
  if m:
    word = m.group(1)
  else:
    m = re.match('<span><font size="3"><sup>(\d+)</sup>(%s+)</font></span>' % permit_chars, line)
    if m:
      prefix  = m.group(1)
      word    = m.group(2)
    else:
      m = re.match('<span><font size="3"><sub>\s{0,1}</sub><sup>(\d+)</sup>(%s+)</font></span>' % permit_chars, line)
      if m:
        postfix = m.group(1)
        word    = m.group(2)  
      else:
        m = re.match('<span><font size="3">(%s+)<sub>(\d+)</sub></font></span>' % permit_chars, line)
        if m:
          word    = m.group(1) 
          postfix  = m.group(2) 
        else:  
          print "--->", line
          break
  w = Word(prefix, word, postfix, line)

  etree.fromstring("<root>" + line + "</root>")
  try:
    etree.fromstring("<root>" + line + "</root>")
  except :
    print line
    break
  
  session.add(w)

session.commit()
print "done"