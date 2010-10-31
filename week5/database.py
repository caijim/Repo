import sqlite3 as sql
import csv, BeautifulSoup, urllib2


#obtained from http://www.cmmichael.com/blog/2006/12/29/state-code-mappings-for-python
state_to_code = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA": "IA", "Armed Forces Pacific": "AP", "GUAM": "GU", "KANSAS": "KS", "FLORIDA": "FL", "AMERICAN SAMOA": "AS", "NORTH CAROLINA": "NC", "HAWAII": "HI", "NEW YORK": "NY", "CALIFORNIA": "CA", "ALABAMA": "AL", "IDAHO": "ID", "FEDERATED STATES OF MICRONESIA": "FM", "Armed Forces Americas": "AA", "DELAWARE": "DE", "ALASKA": "AK", "ILLINOIS": "IL", "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD", "CONNECTICUT": "CT", "MONTANA": "MT", "MASSACHUSETTS": "MA", "PUERTO RICO": "PR", "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH", "MARYLAND": "MD", "NEW MEXICO": "NM", "MISSISSIPPI": "MS", "TENNESSEE": "TN", "PALAU": "PW", "COLORADO": "CO", "Armed Forces Middle East": "AE", "NEW JERSEY": "NJ", "UTAH": "UT", "MICHIGAN": "MI", "WEST VIRGINIA": "WV", "WASHINGTON": "WA", "MINNESOTA": "MN", "OREGON": "OR", "VIRGINIA": "VA", "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH", "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC", "INDIANA": "IN", "NEVADA": "NV", "LOUISIANA": "LA", "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE", "ARIZONA": "AZ", "WISCONSIN": "WI", "NORTH DAKOTA": "ND", "Armed Forces Europe": "AE", "PENNSYLVANIA": "PA", "OKLAHOMA": "OK", "KENTUCKY": "KY", "RHODE ISLAND": "RI", "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR", "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}

connection = sql.connect("political.db")
cursor = connection.cursor()
sql_cmd = """CREATE TABLE polls (id INTEGER PRIMARY KEY AUTOINCREMENT, day float, len INT, state TEXT,stateabbrev TEXT, ev TEXT, dem INT, gop INT, ind TEXT, date TEXT, pollster TEXT)"""
cursor.execute(sql_cmd)

# csv.DictReader uses the first line in the file as column headings by default
dr = csv.DictReader(open('senate_polls.csv'))
to_db = [(i['Day'], i['Len'], i['State'],state_to_code[i['State'].upper()], i['EV'], i['Dem'],i['GOP'],i['Ind'],i['Date'], i['Pollster']) for i in dr]
cursor.executemany("insert into polls (Day, Len, State,Stateabbrev, EV, Dem, GOP, Ind, Date, Pollster) values (?, ?, ?, ?, ?, ?, ?, ?, ?,?);", to_db)

new_cmd = """CREATE TABLE candidates (id INTEGER PRIMARY KEY AUTOINCREMENT, state TEXT, democrat TEXT, republican TEXT, independent TEXT, incumbentparty TEXT)"""
cursor.execute(new_cmd)
new_dr = csv.DictReader(open('candidate_names.txt'))
new_to_db = [(i['State'], i['Democrat'], i['Republican'], i['Independent'], i['IncumbentParty']) for i in new_dr]
cursor.executemany("insert into candidates (state, democrat, republican, independent, incumbentparty) values (?, ?, ?, ?, ?);", new_to_db)

url = 'http://astro.berkeley.edu/~amorgan/candidates/'
page = urllib2.urlopen(url)
soup =BeautifulSoup.BeautifulSoup(page)
names = soup.findAll('a')
not_interested = ['Name','Last modified','Size','Description','Parent Directory']
cleaned = [(name.string.split('.gif')[0], url+name['href']) for name in names if name.string not in not_interested]
#print cleaned

new_cmd = """CREATE TABLE pictures (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, url TEXT)"""
cursor.execute(new_cmd)
new_to_db = [(i['State'], i['Democrat'], i['Republican'], i['Independent'], i['IncumbentParty']) for i in new_dr]

cursor.executemany("insert into pictures (name,url) values (?, ?);", cleaned)
connection.commit()
connection.close()



