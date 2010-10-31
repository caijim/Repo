import sqlite3 as sql
import csv, BeautifulSoup, urllib2, webbrowser, sys, os

connection = sql.connect("political.db")
cursor = connection.cursor()

join_cmd = """SELECT polls.id, polls.day, polls.len, polls.state, polls.ev, polls.dem, polls.gop,polls.ind,polls.date,polls.pollster,candidates.state,candidates.democrat,candidates.id, candidates.republican,candidates.independent,candidates.incumbentparty
 FROM polls LEFT JOIN candidates ON
 polls.stateabbrev = candidates.state"""

cursor.execute(join_cmd)
db_info = cursor.fetchall()
curState = None
previous = 0
change = 0
b = 0
for entry in db_info:
    if not entry[3]==curState:
        b+=1
        curState = entry[3]
        store = entry
        incumbent = store[-1]
        demVote, gopVote, indVote = store[5:8]
        if incumbent.lower()=='democrat':
            if  demVote < gopVote:
                change-=1
        if incumbent.lower()=='republican':
            if demVote>gopVote:
                change+=1
        if incumbent.lower()=='democrat':
            previous+=1

print 'Democrats will have a change of %d seats' %change

