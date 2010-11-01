#!/usr/bin/env python
"""
AY 250 - Scientific Research Computing with Python
Homework Assignment 5 Solutions
Author: Adam Morgan
"""
import os
import pylab
import sqlite3
import glob
import datetime
import numpy
import webbrowser

dbpath = './senate2010.sqlite'
img_url_base = './candidates/'
img_url_ext = '.gif'

def _CreateDB(path=dbpath):
    '''This function reads in all the polling data, candidate names, etc
    and puts them all into various tables within a database
    '''
    path = os.path.abspath('.')
    path = path.split('/')
    path[-1] = 'week5_sol'
    path = '/'.join(path)

    poll_array = pylab.csv2rec(os.path.join(path,'senate_polls.csv'))
    name_array = pylab.csv2rec(os.path.join(path,'candidate_names.txt'))
    cand_url_list = glob.glob(img_url_base + '*' + img_url_ext)
    cand_list=[]
    parties = ['Republican','Democrat','Independent']
    for party in parties:
        for state, name in name_array[[party.lower(),'state']]:
            if name.strip(): #ignore blank entries
                cand_list.append((name.strip(),party,state))

    state_lookup = _getStateLookupDict(os.path.join(path,'state_abbreviations.txt'))

    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    # Create the tables 
    sql_cmd = """
    CREATE TABLE races (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT, 
        rep_cand TEXT, 
        dem_cand TEXT, 
        ind_cand TEXT,
        incumbant_party TEXT);
        
    CREATE TABLE polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT, 
        poll_date DATE, 
        rep_pct INT, 
        dem_pct INT, 
        ind_pct INT,
        pollster TEXT);

    CREATE TABLE candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate TEXT,
        party TEXT, 
        state TEXT,
        image_url TEXT);"""
    cursor.executescript(sql_cmd)

    # Populate the races table
    for name_tuple in name_array:
        sql_cmd = """INSERT INTO races (state, dem_cand, rep_cand, 
            ind_cand, incumbant_party) VALUES %s""" % (str(name_tuple))
        cursor.execute(sql_cmd)
        
    # Populate the polls table
    for poll_val in poll_array:
        try:
            state_abbrev = state_lookup[poll_val['state'].upper()]
        except:
            errmsg = 'Cannot find %s in the lookup table' % (poll_val['state'])
            raise ValueError(errmsg)
        poll_date_str = poll_val['date'].strftime('%m/%d/%y')
        
        value_string = "('%s', '%s', '%i', '%i', '%i', '%s')" % (state_abbrev,\
            poll_date_str, poll_val['gop'], poll_val['dem'], poll_val['ind'],\
            poll_val['pollster'])
        
        sql_cmd = """INSERT INTO polls (state, poll_date, rep_pct, 
            dem_pct, ind_pct, pollster) VALUES %s""" % (value_string)
        cursor.execute(sql_cmd)
        
    # Populate the candidates table
    for cand in cand_list:
        cand_url = img_url_base + cand[0] + img_url_ext
        # assign default picture if we can't find the image
        if not cand_url in cand_url_list:
            print 'Cannot find %s' % (cand_url)
            cand_url = img_url_base + 'Unknown' + img_url_ext
        vals = '("%s", "%s", "%s", "%s")' % (cand[0], cand[1], cand[2], cand_url)
        sql_cmd = """INSERT INTO candidates (candidate, party, state, image_url)
            VALUES %s""" % (vals)
        cursor.execute(sql_cmd)
    
    # Commit the changes to the connection after dumping in the data
    conn.commit()
    return conn
    
def _LoadDB(path=dbpath):
    """Check if the database has been created; if not, create it; if it has, 
    load it"""
    if not os.path.exists(path):
        conn = _CreateDB(path)
    else:
        conn = sqlite3.connect(path)
    return conn 

def _getStateLookupDict(filename='state_abbreviations.txt'):
    '''Here we load a CSV file linking the two letter US State abbreviation
    to its full name with a dictionary.
    '''
    path = os.path.abspath('.')
    path = path.split('/')
    path[-1] = 'week5_sol'
    path = '/'.join(path)
    ff = file(os.path.join(path,'state_abbreviations.txt'))
    lines = ff.readlines()
    # Make a dictionary to look up state's abbreviation by its full name
    state_lookup = {}
    for line in lines:
        state_list = line.rstrip('\n').split(',')
        state_dict = {state_list[1].upper():state_list[0].upper()}
        state_lookup.update(state_dict)
    return state_lookup 

def _promptForState():
    prompt_string = 'Please enter a state or its 2-letter abbreviation: '
    state = raw_input(prompt_string).strip()
    return state

def _checkAndConvertState(state):
    '''Checks to see if the state is a legit US state, and convert it to
    its two-letter state abbreviation.
    '''
    state_lookup = _getStateLookupDict('state_abbreviations.txt')
    # If length == 2, then an abbreviation was provided.
    if len(state.strip()) == 2:
        if state.upper() in state_lookup.values():
            state_abbrev = state.upper()
        else:
            print "Cannot find state %s" % (state.upper())
            raise(ValueError)
    elif state.upper() in state_lookup.keys():
        state_abbrev = state_lookup[state.upper()]
    else:
        print "Cannot find state %s" % (state)
        raise(ValueError)
    return state_abbrev

def AddNewPoll(path=dbpath,state=None,poll_date=None,rep_pct=None,dem_pct=None,\
            ind_pct=-1,pollster=None):
    '''Allows the user to easily input a new poll into the database'''
    if not state:
        state=_promptForState()
    state_abbrev = _checkAndConvertState(state)
    if not poll_date:
        poll_date = raw_input('Provide date of poll in MM/DD/YY format: ')
    try:
        datetime.datetime.strptime(poll_date,'%m/%d/%y')
    except:
        raise ValueError("Cannot parse provided date.  Try again.")
    if not rep_pct:
        rep_pct = raw_input('Percent of poll going to the Republican: ')
    if not dem_pct:
        dem_pct = raw_input('Percent of poll going to the Democrat: ')
    try:
        rep_pct = int(rep_pct)
        dem_pct = int(dem_pct)
    except:
        raise ValueError("Could not convert poll numbers into integers. Try again.")
    if not pollster:
        pollster = raw_input('Name of Pollster: ')
    
    conn = _LoadDB(path)
    cursor = conn.cursor()
    value_string = "('%s', '%s', '%i', '%i', '%i', '%s')" % (state_abbrev,\
        poll_date, rep_pct, dem_pct, ind_pct, pollster)
    
    sql_cmd = """INSERT INTO polls (state, poll_date, rep_pct, 
        dem_pct, ind_pct, pollster) VALUES %s""" % (value_string)
    cursor.execute(sql_cmd)
    conn.commit()
    return conn

def DetermineSeatsLost(path=dbpath):
    ''' This handy sql command, adopted from http://tinyurl.com/37rdj5, 
    will return polling information only from the most recent poll for each 
    state. We are ignoring independents for this excersise.   
    '''
    conn = _LoadDB(path)
    cursor = conn.cursor()
    
    sql_cmd = '''SELECT polls.state, polls.poll_date, polls.rep_pct, 
        polls.dem_pct, races.incumbant_party
    FROM polls
    JOIN races
    ON polls.state=races.state
    WHERE (
       SELECT count(*) FROM polls AS f
       WHERE f.state = polls.state AND f.poll_date > polls.poll_date
    ) <= 0;
    '''
    cursor.execute(sql_cmd)
    db_info = cursor.fetchall()
    conn.close()
    db_trans = zip(*db_info)
    tttarr = numpy.array(db_trans)
    rep_lead_index = numpy.nonzero(tttarr[3] < tttarr[2])
    dem_lead_index = numpy.nonzero(tttarr[3] > tttarr[2])
    rep_curr_index = numpy.nonzero(tttarr[4]=='Republican')
    dem_curr_index = numpy.nonzero(tttarr[4]=='Democrat')
    rep_losses_ind = set(rep_curr_index[0]) & set(dem_lead_index[0])
    dem_losses_ind = set(dem_curr_index[0]) & set(rep_lead_index[0])
    rep_losses = tttarr[0][list(rep_losses_ind)]
    dem_losses = tttarr[0][list(dem_losses_ind)]
    outstr = '''
If the most recent predictions hold, Republicans are expected to lose %i seats 
(%s) 
and the Democrats are expected to lose %i seats 
(%s)
        ''' % (len(rep_losses),str(rep_losses),len(dem_losses),str(dem_losses))
    print outstr
    
def RetrievePollingInfo(path=dbpath,state=None,limit_one=False):
    '''Prompt the user for a state or state abbreviation and use it to 
    retrieve all the polling info, joined with races, for that state.
    Setting limit_one = True will have only the most recent poll be listed.
    '''
    if not state:
        state=_promptForState()
    state_abbrev = _checkAndConvertState(state)
    # Load the db and search it
    conn = _LoadDB(path)
    cursor = conn.cursor()
    sql_cmd = '''SELECT polls.poll_date, polls.rep_pct, polls.dem_pct,  
        polls.ind_pct, races.rep_cand, races.dem_cand,
        races.ind_cand, polls.pollster
        FROM polls
            JOIN races
            ON polls.state=races.state
        WHERE polls.state = %s 
        ORDER BY polls.poll_date DESC''' % ("'"+state_abbrev+"'")
    if limit_one:
        sql_cmd += ' LIMIT 1'
    cursor.execute(sql_cmd)
    db_info = cursor.fetchall()
    conn.close()
    return db_info

def RetrieveCandidateInfo(path=dbpath,state=None):
    '''Prompt the user for a state or state abbreviation and use it to 
    retrieve the most  info, joined with races, for that state.
    '''
    if not state:
        state=_promptForState()
    state_abbrev = _checkAndConvertState(state)
    # Load the db and search it
    conn = _LoadDB(path)
    cursor = conn.cursor()
    # DESC orders by descending order; LIMIT 3 returns only the 3 most recent entries
    sql_cmd = '''SELECT polls.poll_date, candidates.candidate, candidates.party,
        candidates.image_url, races.incumbant_party, polls.rep_pct, 
        polls.dem_pct, polls.ind_pct, polls.pollster
        FROM candidates
            JOIN races
                ON candidates.candidate = races.rep_cand 
                OR candidates.candidate = races.dem_cand
                OR candidates.candidate = races.ind_cand
            JOIN polls
            ON races.state = polls.state
        WHERE candidates.state = %s
        ORDER BY polls.poll_date DESC LIMIT 3''' % ("'"+state_abbrev+"'")
    cursor.execute(sql_cmd)
    db_info = cursor.fetchall()
    conn.close()
    return db_info

def PlotPollingData(path=dbpath,state=None):
    '''Plot all available polling data for a given state; saves to the folder
    ./plots/ with the filename [state].png
    '''
    if not state:
        state=_promptForState()
    state_abbrev = _checkAndConvertState(state)
    db_info=RetrievePollingInfo(path=path,state=state_abbrev,limit_one=False)
    # Transpose info with zip(*info)
    db_info_trans = zip(*db_info)
    timelist=db_info_trans[0]
    rep_array = numpy.array(db_info_trans[1])
    dem_array = numpy.array(db_info_trans[2])
    ind_array = numpy.array(db_info_trans[3])
    rep_label = db_info_trans[4][0]
    dem_label = db_info_trans[5][0]
    ind_label = db_info_trans[6][0]    
    datetimelist=[]
    width = 15
    height = 5
    fig = pylab.plt.figure(figsize=(width, height), dpi=72.0)
    # Convert the times into datetime objects
    for time in timelist:
        datetimelist.append(datetime.datetime.strptime(time,'%m/%d/%y'))
    if len(numpy.nonzero(rep_array > 0)[0]) > 0:
        pylab.scatter(datetimelist,rep_array,c='r',label=rep_label)
    if len(numpy.nonzero(dem_array > 0)[0]) > 0:
        pylab.scatter(datetimelist,dem_array,c='b',label=dem_label)
    if len(numpy.nonzero(ind_array > 0)[0]) > 0:
        pylab.scatter(datetimelist,ind_array,c='g',label=ind_label)
    pylab.ylim(0,80)
    pylab.title('Polling data for '+state.upper())
    pylab.ylabel('% of Vote')
    pylab.legend()
    test_path = os.path.join(os.path.abspath('.'),'plots')
    if not os.path.exists(test_path):os.makedirs(test_path)
    figname = os.path.join(test_path,state + '.png')
    pylab.savefig(figname)
    return figname

def PrintMostRecentData(path=dbpath,state=None,incl_plot=True):
    if not state:
        state=_promptForState()
    state_abbrev = _checkAndConvertState(state)
    db_info=RetrieveCandidateInfo(path=path,state=state_abbrev)

    iii = 5  
    rep_cand,rep_party,rep_img,rep_pct,rep_str = None,None,None,None,'' 
    dem_cand,dem_party,dem_img,dem_pct,dem_str = None,None,None,None,'' 
    ind_cand,ind_party,ind_img,ind_pct,ind_str = None,None,None,None,''  
    lead_flag = 0
    lead_pct = 0
    for entry in db_info:
        if entry[iii] > 0:
            if entry[2] == "Republican":
                rep_cand = entry[1]
                rep_party = entry[2]
                rep_img = entry[3]
                rep_pct = entry[iii]
            if entry[2] == "Democrat":
                dem_cand = entry[1]
                dem_party = entry[2]
                dem_img = entry[3]
                dem_pct = entry[iii]
            if entry[2] == "Independent":
                ind_cand = entry[1]
                ind_party = entry[2]
                ind_img = entry[3]  
                ind_pct = entry[iii]
            if entry[iii] > lead_pct:
                lead_pct = entry[iii]
                lead_cand = entry[1]
                lead_party = entry[2]
                lead_img = entry[3] 
        iii+=1
    # Adjust the name of the party
    if db_info[0][4] == 'Democrat':
        incumbant_party = 'Democratic'
    else:
        incumbant_party = db_info[0][4]
    pollster = db_info[0][8].split('-')[0]
    # Check if we have a tie
    if dem_pct == rep_pct == lead_pct or dem_pct == ind_pct == lead_pct  \
            or ind_pct == rep_pct == lead_pct:
        tie = True
    else:
        tie = False
    # See if there is a party switch
    if lead_party == db_info[0][4]:
        partyswitchstring = 'would NOT'
    else:
        partyswitchstring = 'WOULD'
        
    mydict = {"state":state.upper(),
              "rep_cand":rep_cand, "rep_party":rep_party, "rep_img":rep_img,
              "dem_cand":dem_cand, "dem_party":dem_party, "dem_img":dem_img,
              "ind_cand":ind_cand, "ind_party":ind_party, "ind_img":ind_img,
              "rep_pct": rep_pct, "dem_pct": dem_pct, 
              "ind_pct": ind_pct, "pollster": pollster, 
              "incumbant_party":incumbant_party, "date":db_info[0][0]}
    if rep_cand:
        rep_str = '''<td class="senator" width="112" valign="center" align="center"> 
    		<img src="%(rep_img)s" alt="%(rep_cand)s" width="100" height="125">
    		<br> %(rep_cand)s <br> (%(rep_party)s) <br> %(rep_pct)i%%
            </td>''' % mydict
    if dem_cand:
        dem_str = '''<td class="senator" width="112" valign="center" align="center"> 
    		<img src="%(dem_img)s" alt="%(dem_cand)s" width="100" height="125">
    		<br> %(dem_cand)s <br> (%(dem_party)s) <br> %(dem_pct)i%%
            </td>''' % mydict
    if ind_cand:
        ind_str = '''<td class="senator" width="112" valign="center" align="center"> 
    		<img src="%(ind_img)s" alt="%(ind_cand)s" width="100" height="125">
    		<br> %(ind_cand)s <br> (%(ind_party)s) <br> %(dem_pct)i%%
            </td>''' % mydict
    
    html_head = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html><head>
    <title>Latest Senate Polling from %(state)s</title>
    </head><body bgcolor="#FFFFFF" text="#000066">
    <center>
    <h1>Polling from %(state)s on %(date)s</h1>
    """ % mydict
    
    if tie:
        html_body2='''
        <td class="general-1" valign="top"> 
        General information about the candidate can go here, if you choose to
        put it in the database.  Here we simply some polling information.<br><br>
        From the latest %s poll taken on %s, there is a statistical tie between the
        two top senate candidates with %i%% of the vote each.  It will be a \
        very close race in the state of %s!
        </td>
        ''' % (pollster,db_info[0][0],lead_pct, state.upper())
    else:
        html_body2='''
        <td class="general-1" valign="top"> 
        General information about the candidate can go here, if you choose to
        put it in the database.  Here we simply list some polling information<br><br>
        From the latest %s poll taken on %s, the %s %s is in the lead with %i%% of the 
        vote.  If this were the outcome in November, there %s be a party switch from
        the current %s party in the state of %s. <br><br> Note that these polls 
        typically have an uncertainty of +/- 3 percentage points.
        </td>
        ''' % (pollster,db_info[0][0],lead_party,
            lead_cand, lead_pct, partyswitchstring, incumbant_party, state.upper())
    html_body='''
    <table border="1" cellspacing="0" Summary="candidate" bgcolor="white"> 
     <tr> 
        %s
        %s
        %s
        %s
      </tr> 
    </table>
    
    '''  % (rep_str,dem_str,ind_str,html_body2)
    
    if incl_plot:
        figpath = PlotPollingData(path=path,state=state)
        fig_html = '<center><br><br><img src="%s" alt="Current Polls" width="800"><br><br>' % figpath
    else: 
        fig_html = ''
    
    html_foot= '</body></html>'
    html_path = './polls_'+state+'.html'
    f = file(html_path,'w')
    f.write(html_head + html_body +fig_html + html_foot)
    f.close()
    fullpath = os.path.abspath(html_path)
    url = 'file:///'+fullpath
    webbrowser.open_new(url)

def test():
    '''Run through the various routines to demonstrate the features of the 
    code.
    '''
#    AddNewPoll(path=dbpath,state='fl',poll_date='10/07/10',dem_pct=19,\
#        rep_pct=50, ind_pct=25, pollster='Rasmussen')
    PrintMostRecentData(path=dbpath,state='fl',incl_plot=True)
    DetermineSeatsLost(path=dbpath)

if __name__ == "__main__":
    test()
