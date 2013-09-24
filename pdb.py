#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Script to transfer cmudict to sqlite database

"""
from __future__ import unicode_literals
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

s = {
  "0" : "",
  "1" : "'",
  "2" : "ˌ"
}
arpabet_ipa_table = {
    #Vowels (Monophthongs)
    "AO" : "ɔ",
    "AA" : "ɑ",
    "IY" : "i",
    "UW" : "u",
    "EH" : "ɛ",
    "IH" : "ɪ",
    "UH" : "ʊ",
    "AH" : {"1" : "ʌ", "2" : "ʌ", "0" : "ə"},
    "AX" : "ə",
    "AE" : "æ",
    #Vowels (Diphthongs)
    "EY" : "eɪ",
    "AY" : "aɪ",
    "OW" : "oʊ",
    "AW" : "aʊ",
    "OY" : "ɔɪ",
    #Vowels (R-colored)
    "ER" : "ɝ",
    "AXR" : "ɚ",
    #Semivowels
    "Y" : "j",
    "W" : "w",
    "Q" : "ʔ",
    #Consonants (Stops)
    "P" : "p",
    "B" : "b",
    "T" : "t",
    "D" : "d",
    "K" : "k",
    "G" : "ɡ",
    #Consonants (Affricates)
    "CH" : "tʃ",
    "JH" : "dʒ",
    #Consonants (Fricatives)
    "F" : "f",
    "V" : "v",
    "TH" : "θ",
    "DH" : "ð",
    "S" : "s",
    "Z" : "z",
    "SH" : "ʃ",
    "ZH" : "ʒ",
    #Consonants (Aspirate)
    "HH" : "h",
    #Nasals
    "M" : "m",
    "EM" : "m̩",
    "N" : "n",
    "EN" : "n̩",
    "NG" : "ŋ",
    "ENG" : "ŋ̍",
    #Liquids
    "L" : "ɫ",
    "EL" : "ɫ̩",
    "R" : "ɹ",
    "DX" : "ɾ",
    "NX" : "ɾ̃"
}

Base = declarative_base() 

class Phonetic(Base):
  __tablename__ = 'phonetic'
  word = Column(String, primary_key=True)
  postfix = Column(Integer, primary_key=True)
  arpabet = Column(String)
  phonetic = Column(String)

  def __init__(self, word, arpabet, phonetic):
    self.word = word
    print self.word
    self.postfix = -1
    if self.word[-1] == ')':
      self.postfix = int(self.word[-2])
      self.word = self.word[:-3]

    self.phonetic = phonetic
    self.arpabet = arpabet

  def __repr__(self):
    return "<Word('%s', ('%d'), %s)>" % (self.word, self.postfix, self.phonetic)


def trans (phoneme):
  if phoneme[-1].isdigit():
    if phoneme[:-1] == "AH":
      return s[phoneme[-1]] + arpabet_ipa_table["AH"][phoneme[-1]]
    else:
      return s[phoneme[-1]] + arpabet_ipa_table[phoneme[:-1]]

  else:
    return arpabet_ipa_table[phoneme]
    
if __name__ == '__main__':
    source = open('cmudict.0.7a', 'r')
    #dest = open('dict_ipa.txt',  'w')

    engine = create_engine('sqlite:///d:/phonetic.db')


    metadata = MetaData()
    players_table = Table('phonetic', metadata,
         Column('word', String),
         Column('postfix', Integer),
         Column('arpabet', String),         
         Column('phonetic', String)
      )
    metadata.create_all(engine) 
    Session = sessionmaker(bind=engine)
    session = Session()
    for line in source:
        if line[0] == ';':                   # header, comments
            continue                         # starts next iter of loop
        (word, pron) = line.rstrip().split('  ', 1)
        w = Phonetic( word, pron, u''.join( map(trans, pron.split())) )
        session.add(w)
        #dest.writelines( [ word , '\n', str( pron.split() ) , '\n',  ''.join( map(trans, pron.split()) ).encode('utf-8'), '\n'] )
        #dest.write(word.lower().encode('utf-8') + "\t[".encode('utf-8') + ''.join( map(trans, pron.split()) ).encode('utf-8') + "]\n".encode('utf-8'))

session.commit()