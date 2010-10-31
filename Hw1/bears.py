import random, urllib2, csv, copy
import matplotlib.pyplot as plt
import networkx as nx

def bearLife():
    return random.gauss(35,5)
def whichSex(param):
    rndm = random.random()
    percMale = 1-param
    if rndm>=percMale:
        return True
    else:
        return False

def matingProb():
#probability of procreating given that the bear is able to
    return 1

def simulateBears(m_names, f_names, c_names, func, param, verbose=False):
    #(name, bool(Male), deathage identifier)
    starters = [('Adam',True,0),('Eve',False,1),('Mary',False,2)]
    identifier = 2
    bearpool = set()
    totalPool = set()
    for starter in starters:
        bearpool.add(starter)
        totalPool.add(starter)
   #The key is the identifier, the value is a set
    parentDct = {0:set(['11']),1:set(['00']),2:set(['1100'])}
    childrenDct = {0:set(),1:set(),2:set()}
    ageDct = {0:0,1:0,2:0}
    deathDct = {0:bearLife(),1:bearLife(),2:bearLife()}
    cooldownDct = {0:0,1:0,2:0}
    pop_vec = []
    virilepool = set()
    for year in range(0,151):
        pop_vec.append(len(totalPool)) 
    #Check to see if any can reproduce
    #Kill bears that ask the wrong questions
        deadNow = set()
        for bear in ageDct:
            if ageDct[bear]>deathDct[bear]:
                deadNow.add(bear)
        dead = set()
        for bear in bearpool:
            if bear[-1] in deadNow:
                dead.add(bear)
        for bear in dead:
            bearpool.remove(bear)
        for bear in bearpool :
                age = ageDct[bear[-1]]
                if bear[-1] in cooldownDct:
                    cooldown = cooldownDct[bear[-1]]
                else:
                    cooldown =0
                if age>5 and cooldown==0:
                    virilepool.add(bear)
        alreadyMated = set()
        sittingOut = set()
        for sexybear in virilepool:
            if sexybear not in alreadyMated and sexybear not in sittingOut:
                tendency = matingProb()
                willMate = False
                if tendency > .5:
                    willMate = True
                #Find the bear a mate
                if not willMate:
                    sittingOut.add(sexybear)
                    continue
                gender = sexybear[1]
                for mate in virilepool:
                    if mate[1] !=gender and mate not in alreadyMated and mate not in sittingOut:
                        if not parentDct[mate[-1]]==parentDct[sexybear[-1]] and abs(ageDct[mate[-1]]-ageDct[sexybear[-1]])<=10:
        #they will mate!
        #(name, bool(Male), identifier)                
                            sex = whichSex(param)
                            try:
                                if sex:
                                    name = m_names[random.randrange(0,len(m_names))]
                                    m_names.remove(name)
                                else:
                                    name = f_names[random.randrange(0,len(f_names))]
                                    f_names.remove(name)
                            except ValueError:
                                    name = c_names[random.randrange(0,len(c_names))]
                                    c_names.remove(name)
                            identifier+=1
                            babybear = (name, sex,identifier)
                            deathDct[identifier] = bearLife()
                            ageDct[identifier] = 0
                            parentDct[identifier] = set()
                            parentDct[identifier].add(mate[-1])
                            parentDct[identifier].add( sexybear[-1])
                            if mate[-1] in childrenDct:
                                childrenDct[mate[-1]].add(identifier)
                            else:
                                childrenDct[mate[-1]]=set()
                                childrenDct[mate[-1]].add(identifier)
                            if sexybear[-1] in childrenDct:
                                childrenDct[sexybear[-1]].add(identifier)
                            else:
                                childrenDct[sexybear[-1]]=set()
                                childrenDct[sexybear[-1]].add(identifier)
                            cooldownDct[mate[-1]] = 5
                            cooldownDct[sexybear[-1]] = 5
                            bearpool.add(babybear)
                            totalPool.add(babybear)
                        break
                alreadyMated.add(sexybear)
                alreadyMated.add(mate)
        for bear in alreadyMated:
            virilepool.remove(bear)
        for bear in ageDct:
            ageDct[bear]+=1
        for bear in cooldownDct:
            if cooldownDct[bear] !=0:
                cooldownDct[bear]-=1
    if not verbose:
        return (pop_vec, bearpool)
    else:
        return (pop_vec, bearpool,totalPool, childrenDct, parentDct)
############END OF DEFINITIONS###############
#############################################
#############################################
#############################################
#############################################
#############################################
#Names
female_names = open("female.txt","r")
cat_names = open("cat.txt")
male_names = open("male.txt","r")
f_reader = csv.reader(female_names, delimiter=' ')
m_reader = csv.reader(male_names, delimiter=' ')

m_names = []
f_names = []
c_names = []

for row in m_reader:
    m_names.append(row[0])
for row in f_reader:
    f_names.append(row[0])
for name in cat_names:
    c_names.append(name)
#############################################
#Question 1. let's make 1000 simulations
#############################################
#############################################

#Code to find number of bears born in the first 100 years
#How many bears are alive
#1000 trials, takes 12 minutes
"""
avg_hundred = 0
avg_alive = 0
numb  = 1000
perc = .5
print 'Starting Simulations'
for i in range(numb):
    if i%10==0:
        print '%d simulations run' %i
    vec, alive = simulateBears(m_names[:], f_names[:], c_names[:], whichSex,perc)
#In the code, on vec[1] is the total number born in the first year
#Therefore vec[i] is the total number born in the 100th year + before
    hundred = vec[100]
#bearpool is how many bears are left after the entire process
    alive = len(alive)
    avg_hundred+=float(hundred)/numb
    avg_alive += float(alive)/numb
print avg_hundred
print avg_alive
"""
#For numb = 1000
# P(Male) = .5
#125.484-3 = 122.484 born in the first 100 years
#1459.557 alive at the end of 150 years

#############################################
#Question 2.
#Iterate over 1%-50%, 50 trials each (later trials take most of the work)
#############################################
"""
perc_vec = []
for perc in range(0,51):
    print 'p=%de^-2 simulating' %(perc)
    avg_alive = 0
    numb  = 50
    perc = float(perc)/100
    for i in range(numb):
        vec, alive = simulateBears(m_names[:], f_names[:], c_names[:], whichSex,perc)
    #In the code, on vec[1] is the total number born in the first year
    #Therefore vec[i] is the total number born in the 100th year + before
        hundred = vec[100]
    #bearpool is how many bears are left after the entire process
        alive = len(alive)
#        avg_hundred+=float(hundred)/numb
        avg_alive += float(alive)/numb
    perc_vec.append(avg_alive)

print perc_vec
plt.plot(range(0,51),perc_vec) 
for i in range( len(perc_vec)):
    avg = perc_vec[i]
    if avg>1:
        print (range(0,51)[i], avg)
        break
"""

#At 21%, we pass the 1 bear alive threshold (1.26 bears)

#############################################
#Question 3
#Let's draw a family tree
#############################################
perc = .5
# (pop_vec, bearpool,totalPool, childrenDct, parentDct)
starters = [('Adam',True,0),('Eve',False,1),('Mary',False,2)]
pop_vec, bearpool,totalPool, childrenDct, parentDct = simulateBears(m_names[:], f_names[:], c_names[:], whichSex,perc, verbose=True)
nameDct = {}
for bear in totalPool:
    nameDct[bear[-1]]=bear[0]
nameDct['11'] = 'God'
nameDct['00'] = 'Yahweh'
nameDct['1100'] = 'Allah'
G = nx.DiGraph()
#The Chosen One
random_bear = random.choice(childrenDct.keys())
children = childrenDct[random_bear]


def draw_edges(graph, dct, start):
    if len(start)==0:
        pass
    else:
        for item in start:
            try:
                connections = dct[item]
            except KeyError:
                continue
            for connect in connections:
                graph.add_edge(nameDct[connect],nameDct[item])
                draw_edges(graph, dct, connections)
    return G

G =draw_edges(G, parentDct, [random_bear])

masterSet =  parentDct[random_bear]
temp = parentDct[random_bear]
while len(temp)>0:
    parentSet = set()
    parentSet.update(temp)
    temp = set()
    for parent in parentSet:
        try:
            ancestors = parentDct[parent]
        except KeyError:
            continue
        for anc in ancestors:
            masterSet.add(anc)
            temp.add(anc)
#masterset consists of all direct ancestors, so we'll draw edges to their children
for anc in masterSet:
    try:
        children = childrenDct[anc]
        for child in children:
            G.add_edge(nameDct[anc], nameDct[child]) 
    except KeyError:
        continue

#nx.draw(G, node_size=1)
pos=nx.graphviz_layout(G,prog='twopi',args='')
plt.figure(figsize=(8,8))
nx.draw(G,pos,node_size=20,node_color="blue", with_labels=False)
plt.axis('equal')


