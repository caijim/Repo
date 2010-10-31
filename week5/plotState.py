import sqlite3 as sql
import csv, BeautifulSoup, urllib2, webbrowser, sys, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

code_to_state = {"WA": "WASHINGTON", "VA": "VIRGINIA", "DE": "DELAWARE", "DC": "DISTRICT OF COLUMBIA", "WI": "WISCONSIN", "WV": "WEST VIRGINIA", "HI": "HAWAII", "AE": "Armed Forces Middle East", "FL": "FLORIDA", "FM": "FEDERATED STATES OF MICRONESIA", "WY": "WYOMING", "NH": "NEW HAMPSHIRE", "NJ": "NEW JERSEY", "NM": "NEW MEXICO", "TX": "TEXAS", "LA": "LOUISIANA", "NC": "NORTH CAROLINA", "ND": "NORTH DAKOTA", "NE": "NEBRASKA", "TN": "TENNESSEE", "NY": "NEW YORK", "PA": "PENNSYLVANIA", "CA": "CALIFORNIA", "NV": "NEVADA", "AA": "Armed Forces Americas", "PW": "PALAU", "GU": "GUAM", "CO": "COLORADO", "VI": "VIRGIN ISLANDS", "AK": "ALASKA", "AL": "ALABAMA", "AP": "Armed Forces Pacific", "AS": "AMERICAN SAMOA", "AR": "ARKANSAS", "VT": "VERMONT", "IL": "ILLINOIS", "GA": "GEORGIA", "IN": "INDIANA", "IA": "IOWA", "OK": "OKLAHOMA", "AZ": "ARIZONA", "ID": "IDAHO", "CT": "CONNECTICUT", "ME": "MAINE", "MD": "MARYLAND", "MA": "MASSACHUSETTS", "OH": "OHIO", "UT": "UTAH", "MO": "MISSOURI", "MN": "MINNESOTA", "MI": "MICHIGAN", "MH": "MARSHALL ISLANDS", "RI": "RHODE ISLAND", "KS": "KANSAS", "MT": "MONTANA", "MP": "NORTHERN MARIANA ISLANDS", "MS": "MISSISSIPPI", "PR": "PUERTO RICO", "SC": "SOUTH CAROLINA", "KY": "KENTUCKY", "OR": "OREGON", "SD": "SOUTH DAKOTA"}

state_to_code = {"VERMONT": "VT", "GEORGIA": "GA", "IOWA": "IA", "Armed Forces Pacific": "AP", "GUAM": "GU", "KANSAS": "KS", "FLORIDA": "FL", "AMERICAN SAMOA": "AS", "NORTH CAROLINA": "NC", "HAWAII": "HI", "NEW YORK": "NY", "CALIFORNIA": "CA", "ALABAMA": "AL", "IDAHO": "ID", "FEDERATED STATES OF MICRONESIA": "FM", "Armed Forces Americas": "AA", "DELAWARE": "DE", "ALASKA": "AK", "ILLINOIS": "IL", "Armed Forces Africa": "AE", "SOUTH DAKOTA": "SD", "CONNECTICUT": "CT", "MONTANA": "MT", "MASSACHUSETTS": "MA", "PUERTO RICO": "PR", "Armed Forces Canada": "AE", "NEW HAMPSHIRE": "NH", "MARYLAND": "MD", "NEW MEXICO": "NM", "MISSISSIPPI": "MS", "TENNESSEE": "TN", "PALAU": "PW", "COLORADO": "CO", "Armed Forces Middle East": "AE", "NEW JERSEY": "NJ", "UTAH": "UT", "MICHIGAN": "MI", "WEST VIRGINIA": "WV", "WASHINGTON": "WA", "MINNESOTA": "MN", "OREGON": "OR", "VIRGINIA": "VA", "VIRGIN ISLANDS": "VI", "MARSHALL ISLANDS": "MH", "WYOMING": "WY", "OHIO": "OH", "SOUTH CAROLINA": "SC", "INDIANA": "IN", " NEVADA": "NV", "LOUISIANA": "LA", "NORTHERN MARIANA ISLANDS": "MP", "NEBRASKA": "NE", "ARIZONA": "AZ", "WISCONSIN": "WI", "NORTH DAKOTA": "ND", "Armed Forces Europe": "AE", "PENNSYLVANIA": "PA", "OKLAHOMA": "OK", "KENTUCKY": "KY", "RHODE ISLAND": "RI", "DISTRICT OF COLUMBIA": "DC", "ARKANSAS": "AR", "MISSOURI": "MO", "TEXAS": "TX", "MAINE": "ME"}


latest = sys.argv[1].strip()
if latest.upper() in code_to_state:
    latest = code_to_state[latest.upper()]
else:
    latest = latest.upper()

connection = sql.connect("political.db")
cursor = connection.cursor()

join_cmd = """SELECT polls.id, polls.day, polls.len, polls.state, polls.ev, polls.dem, polls.gop,polls.ind,polls.date,polls.pollster,candidates.state,candidates.democrat,candidates.id, candidates.republican,candidates.independent,candidates.incumbentparty
 FROM polls LEFT JOIN candidates ON
 polls.stateabbrev = candidates.state"""

cursor.execute(join_cmd)
db_info = cursor.fetchall()
state_info = []
for entry in db_info:
    if entry[3].upper()==latest:
        state_info.append(entry)

time = np.array([entry[1] for entry in state_info])
demVotes = np.array([entry[5] for entry in state_info])
gopVotes = np.array([entry[6] for entry in state_info])
indVotes = np.array([entry[7] for entry in state_info])

for votes in [demVotes, gopVotes, indVotes]:
    for i in range(len(votes)):
        try:
            int(votes[i])
        except:
            votes[i]=0

pic_join = """SELECT pictures.id,pictures.name, pictures.url, candidates.id,candidates.state,candidates.democrat,candidates.republican,candidates.independent,candidates.incumbentparty
 FROM pictures LEFT JOIN candidates ON
 pictures.name = candidates.democrat OR
 pictures.name = candidates.republican OR
 pictures.name = candidates.independent"""



latest = state_to_code[latest.upper()]

person_info = None
cursor.execute(pic_join)

pix = cursor.fetchall()
for person in pix:
    if latest==person[4]:
        person_info = person
        break

dem = person[-4]
rep = person[-3]
ind = person[-2]
if person[-2].strip()==u'':
    ind = None
    

latest = code_to_state[latest]
fig = plt.figure(figsize=(15,10))
host = fig.add_subplot(111)
host.set_xlabel("Date (Days into Political Cycle)",size="large")
host.set_ylabel("Votes",size="large")
host.set_title("Senate Race for %s"%latest[0].upper()+latest[1:].lower(), size="x-large",weight='bold')
p1, = host.plot(time,demVotes,'blue', label="Dem",lw=2)
p2, = host.plot(time,gopVotes,'r--', label="Rep",lw=2)
if ind:
    p3, =host.plot(time,indVotes,'green', label="Rep",lw=2)
if ind:
    plt.legend((p1,p2,p3),(dem,rep,ind), 'center left', numpoints=8 )
else:
    plt.legend((p1,p2),(dem,rep), 'center left', numpoints=8 )
plt.draw()
plt.show()
canvas = FigureCanvasAgg(fig)
canvas.print_figure("partf.png",dpi=144)

