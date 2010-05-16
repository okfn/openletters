from sqlalchemy import *
from meta import engine, metadata, Session

from openletters.model.letter import Letter

#define the table mappings here
users = Table('letters', metadata, autoload=True)
#notes = Table('annotation', metadata, autoload=True)

session = Session()

def run(stmt):
    rs = stmt.execute()
    for row in rs:
        #print "row", row
        return row
 
#gets the letter text - where letter_text  
#need to map this to the correct table
def get_letter_text(uri): 
    ret_arr = {}
    url = ''
    text = ''
    for url, text in session.query(Letter.id, Letter.letter_text).filter(Letter.id==uri):
        ret_arr[url] = text

    print "session", ret_arr
    return ret_arr

#returns all letters by an author 
def index_author (author):
    ret_index = {}
    index = users.select(users.c.type == author)
    #r =run(index)
    rs = index.execute()
    count = 0
    for row in rs:
        #create dictionary of url and correspondent 
        count += 1
        ret_index[count] = [row[3], row[5], row[7]]
        
    return ret_index

#returns correspondents
def createCorrespondents (author):
    ret_corr = {}

    index = users.select(users.c.type == author)
    #r =run(index)
    rs = index.execute()
    count = 0
    for row in rs:
        #create dictionary of url and correspondent 
        count += 1
        ret_corr[count] = [row[3], row[5], row[7]]

    return ret_corr

#gets the basic details for RDF representation of letter
def get_letter_rdf (url):
    ret_arr = {}
    s = users.select(users.c.perm_url == url)
    rs = s.execute()
    for row in rs:
        ret_arr[row[0]] = [row[3], row[5],row[6], row[7]]
    
    return ret_arr 
  
#gets data for all letters to create an endpoint
def get_endpoint_rdf ():
    ret_arr = {}
    s = users.select()
    rs = s.execute()
    for row in rs:
        ret_arr[row[0]] = [row[3], row[5],row[6], row[7], row[4]]
    
    return ret_arr

#gets the correspondent details to wrap in foaf
def get_correspondent (corr):
    ret_arr = {}
    corres = users.select(users.c.correspondent == corr)
    rs = corres.execute()
    for row in rs:
        ret_arr[row[4]] = [row[5]]
    
    return ret_arr
#gets any annotations for a letter - this will come later
def get_annotation (url):
    annotation = notes.select(notes.c.url == url)
    r = run(annotation)
    return r

#inserts the annotation - this will come later once the templating as been done
def insert_annotation (url):
    insertNote = notes.insert(notes.c.url == url)
    r = run(insertNote)
    return r

#void method to insert the data from the parser
#TODO: add in the date to the db  
def insert_letters(url, vol, corr, type, sal, letter, date):
    ins = users.insert()
    db.execute(ins, volume=vol, type=type, perm_url=url, correspondent=corr, salutation=sal, letter_text=letter, letter_date=date)
