import sqlite3 as sql
import csv, BeautifulSoup, urllib2, webbrowser, sys, os

code_to_state = {"WA": "WASHINGTON", "VA": "VIRGINIA", "DE": "DELAWARE", "DC": "DISTRICT OF COLUMBIA", "WI": "WISCONSIN", "WV": "WEST VIRGINIA", "HI": "HAWAII", "AE": "Armed Forces Middle East", "FL": "FLORIDA", "FM": "FEDERATED STATES OF MICRONESIA", "WY": "WYOMING", "NH": "NEW HAMPSHIRE", "NJ": "NEW JERSEY", "NM": "NEW MEXICO", "TX": "TEXAS", "LA": "LOUISIANA", "NC": "NORTH CAROLINA", "ND": "NORTH DAKOTA", "NE": "NEBRASKA", "TN": "TENNESSEE", "NY": "NEW YORK", "PA": "PENNSYLVANIA", "CA": "CALIFORNIA", "NV": "NEVADA", "AA": "Armed Forces Americas", "PW": "PALAU", "GU": "GUAM", "CO": "COLORADO", "VI": "VIRGIN ISLANDS", "AK": "ALASKA", "AL": "ALABAMA", "AP": "Armed Forces Pacific", "AS": "AMERICAN SAMOA", "AR": "ARKANSAS", "VT": "VERMONT", "IL": "ILLINOIS", "GA": "GEORGIA", "IN": "INDIANA", "IA": "IOWA", "OK": "OKLAHOMA", "AZ": "ARIZONA", "ID": "IDAHO", "CT": "CONNECTICUT", "ME": "MAINE", "MD": "MARYLAND", "MA": "MASSACHUSETTS", "OH": "OHIO", "UT": "UTAH", "MO": "MISSOURI", "MN": "MINNESOTA", "MI": "MICHIGAN", "MH": "MARSHALL ISLANDS", "RI": "RHODE ISLAND", "KS": "KANSAS", "MT": "MONTANA", "MP": "NORTHERN MARIANA ISLANDS", "MS": "MISSISSIPPI", "PR": "PUERTO RICO", "SC": "SOUTH CAROLINA", "KY": "KENTUCKY", "OR": "OREGON", "SD": "SOUTH DAKOTA"}

state_to_code = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA": "IA", "Armed Forces Pacific": "AP", "GUAM": "GU", "KANSAS": "KS", "FLORIDA": "FL", "AMERICAN SAMOA": "AS", "NORTH CAROLINA": "NC", "HAWAII": "HI", "NEW YORK": "NY", "CALIFORNIA": "CA", "ALABAMA": "AL", "IDAHO": "ID", "FEDERATED STATES OF MICRONESIA": "FM", "Armed Forces Americas": "AA", "DELAWARE": "DE", "ALASKA": "AK", "ILLINOIS": "IL", "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD", "CONNECTICUT": "CT", "MONTANA": "MT", "MASSACHUSETTS": "MA", "PUERTO RICO": "PR", "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH", "MARYLAND": "MD", "NEW MEXICO": "NM", "MISSISSIPPI": "MS", "TENNESSEE": "TN", "PALAU": "PW", "COLORADO": "CO", "Armed Forces Middle East": "AE", "NEW JERSEY": "NJ", "UTAH": "UT", "MICHIGAN": "MI", "WEST VIRGINIA": "WV", "WASHINGTON": "WA", "MINNESOTA": "MN", "OREGON": "OR", "VIRGINIA": "VA", "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH", "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC", "INDIANA": "IN", "NEVADA": "NV", "LOUISIANA": "LA", "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE", "ARIZONA": "AZ", "WISCONSIN": "WI", "NORTH DAKOTA": "ND", "Armed Forces Europe": "AE", "PENNSYLVANIA": "PA", "OKLAHOMA": "OK", "KENTUCKY": "KY", "RHODE ISLAND": "RI", "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR", "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}


latest = sys.argv[1].strip()
if latest.upper() in code_to_state:
    latest = code_to_state[latest.upper()]

connection = sql.connect("political.db")
cursor = connection.cursor()

join_cmd = """SELECT polls.id, polls.day, polls.len, polls.state, polls.ev, polls.dem, polls.gop,polls.ind,polls.date,polls.pollster,candidates.state,candidates.democrat,candidates.id, candidates.republican,candidates.independent,candidates.incumbentparty
 FROM polls LEFT JOIN candidates ON
 polls.stateabbrev = candidates.state"""

pic_join = """SELECT pictures.id,pictures.name, pictures.url, candidates.id,candidates.state,candidates.democrat,candidates.republican,candidates.independent,candidates.incumbentparty
 FROM pictures LEFT JOIN candidates ON
 pictures.name = candidates.democrat OR
 pictures.name = candidates.republican OR
 pictures.name = candidates.independent"""


cursor.execute(join_cmd)
db_info = cursor.fetchall()
for entry in db_info:
    if entry[3].upper()==latest:
        store = entry
        break

incumbent = store[-1]
demVote, gopVote, indVote = store[5:8]
if incumbent.lower()=='democrat':
    stay  = demVote > gopVote
if incumbent.lower()=='republican':
    stay = gopVote >demVote


latest = state_to_code[latest.upper()]

person_list = []
cursor.execute(pic_join)
pix = cursor.fetchall()
for person in pix:
    if latest==person[4]:
        person_list.append(person)

writefile = open("writing.txt","w")
for person in person_list:
    writefile.write(person[1]+'\t'+ person[2]+'\n')
if demVote:
    writefile.write( 'Current Democratic vote prediction is '+str(demVote)+'\n')
if gopVote:
    writefile.write( 'Current GOP vote prediction is '+str(gopVote)+'\n')
if indVote:
    writefile.write( 'Current Independent vote prediction is '+str(indVote)+'\n')
if stay:
    writefile.write( 'Predicted Party Switch'+'\n')
else:
    writefile.write( 'Incumbent Party Projected to Stay'+'\n')
writefile.close()
webbrowser.open(os.path.join(os.path.abspath(''),'writing.txt'))

