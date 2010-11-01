import sys, os, argparse
#Adding module path to SenatePolls to sys.path
currentdir = os.path.abspath('..')
week5code = os.path.join(currentdir, 'week5_sol')
sys.path.append(week5code)
import SenatePolls

parser = argparse.ArgumentParser(description= 'Polls Parser')

#Adding options for argparse
parser.add_argument('--a', action='store_true', dest='add_database',
help='Add new poll(s) to the database. Need state, poll_date, rep_pct, dem_pct, ind_pct, pollster \n \
      see -s -p -e -r -i -o')
parser.add_argument('-d', action='store', dest='database',
help='Choose which database to work with')
parser.add_argument('-s', action='store', dest='state',
help='Choose which state we are interested in')
parser.add_argument('--p', action='store_true', dest='plot_state',
help='Plot updated polls for a given state')
parser.add_argument('-p', action='store', dest='poll_date',
help='Poll date')
parser.add_argument('-e', action='store', dest='dem_pct',
help='Democratic Poll Percent')
parser.add_argument('-r', action='store', dest='rep_pct',
help='Republican Poll Pct')
parser.add_argument('-i', action='store', dest='ind_pct',
help='Independent Poll Pct')
parser.add_argument('-o', action='store', dest='pollster',
help='Pollster')



results = parser.parse_args()
if not dbpath:
    dbpath = os.path.join(week5code,'senate2010.sqlite')
#Add new poll to database
if results.add_database:
    try:
        SenatePolls.AddNewPoll(path=dbpath,state=results.state,poll_date=results.poll_date,rep_pct=results.rep_pct,\
                   dem_pct=results.dem_pct,ind_pct=results.ind_pct,pollster=results.pollster)
    except ValueError,e:
        print 'Incorrectly Formatted Input'
#Plot State race
if results.plot_state:
    print dbpath
    SenatePolls.PlotPollingData(path=dbpath, state=results.state)

