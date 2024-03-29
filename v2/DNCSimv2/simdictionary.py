from ability import ability
from buff import buff
from card import card
from job import job

def genabil(wepdelay, GCDrecast):

    autoattack = ability('Auto Attack', 'Auto', 'ST', wepdelay, 100, 0, 0)
    cascade = ability('Cascade', 'GCD', 'ST', GCDrecast, 250, 0,  0)
    fountain = ability('Fountain', 'GCD', 'ST', GCDrecast, 100, 0, 300)
    reversecascade = ability('Reverse Cascade', 'GCD', 'ST', GCDrecast, 350, 0, 0)
    fountainfall = ability('Fountainfall', 'GCD', 'ST', GCDrecast, 400, 0, 0)

    windmill = ability('Windmill', 'GCD', 'AE', GCDrecast, 250, 0,  0)
    bladeshower = ability('Bladeshower', 'GCD', 'AE', GCDrecast, 100, 0, 200)
    risingwindmill = ability('Rising Windmill', 'GCD', 'AE', GCDrecast, 250, 0, 0)
    bloodshower = ability('Bloodshower', 'GCD', 'AE', GCDrecast, 300, 0, 0)

    fandance1 = ability('Fan Dance I', 'OGCD', 'ST', 1, 150, 0, 0)
    fandance2 = ability('Fan Dance II', 'OGCD', 'AE', 1, 100, 0, 0)
    fandance3 = ability('Fan Dance III', 'OGCD', 'AE', 1, 200, 0, 0)

    devilment = ability('Devilment', 'GCD', 'AE', GCDrecast, 600, 0, 0)
    devilment.cost = 50

    technicalstep = ability('Technical Step', 'GCD', 'ST', 120, 0, 0, 0)
    standardstep = ability('Standard Step', 'GCD', 'ST', 30, 0, 0, 0)
    step = ability('Step', 'GCD', 'ST', 1, 0, 0, 0)
    technicalfinish = ability('Technical Finish', 'GCD', 'AE', 1, 1500, 0, 0)
    standardfinish = ability('Standard Finish', 'GCD', 'AE', 1, 1000, 0, 0)

    saberdance = ability('Saber Dance', 'OGCD', 'ST', 120, 0, 0,  0)
    flourish = ability('Flourish', 'OGCD', 'ST', 60, 0, 0, 0)
    improv = ability('Improvisation', 'OGCD', 'ST', 180, 0, 0, 0)

    potion = ability('Potion', 'OGCD', 'ST', 270, 0, 0, 0)

    table = [autoattack,cascade,fountain,reversecascade,fountainfall,windmill,bladeshower,risingwindmill,bloodshower,fandance1,fandance2,fandance3,devilment,technicalstep,standardstep,
             step,technicalfinish,standardfinish,saberdance,flourish,improv,potion]

    dict = {}
    for i in table:
        dict[i.name]=i

    return dict

def genjobs():
    nin = job('NIN', 'DPS', True, 2.4, .7, .15, True)
    drg = job('DRG', 'DPS', True, 2.4, .7, .15, False)
    mnk = job('MNK', 'DPS', False, 2.4, .7, .15, False)
    sam = job('SAM', 'DPS', False, 2.4, .7, .15, False)

    brd = job('BRD', 'DPS', False, 2.4, 0, .15, False)
    mch = job('MCH', 'DPS', False, 2.4, 0, .15, False)

    rdm = job('RDM', 'DPS', True, 2.4, 0, .15, False)
    smn = job('SMN', 'DPS', False, 2.4, 0, .15, False)
    blm = job('BLM', 'DPS', False, 2.4, 0, .15, False)

    sch = job('SCH', 'HEAL', True, 2.4, 0, .15, False)
    ast = job('AST', 'HEAL', True, 2.4, 0, .15, False)
    whm = job('WHM', 'HEAL', False, 2.4, 0, .15, False)

    gnb = job('GNB', 'TANK', True, 2.4, 0, .15, False)
    war = job('WAR', 'TANK', True, 2.4, 0, .15, False)
    drk = job('DRK', 'TANK', False, 2.4, 0, .15, False)
    pld = job('PLD', 'TANK', False, 2.4, 0, .15, False)


    table = [nin,drg,mnk,sam,brd,mch,rdm,smn,blm,sch,ast,whm,gnb,war,drk,pld]

    dict ={}
    for i in table:
        dict[i.name] = i

    return dict

def genparty(jobs):

    party = []
    for i in jobs.values():
        if i.active:
            party.append(i)

    dict = {}
    for i in party:
        dict[i.name] = i

    return dict

def genpbuffs(party):

    goodcard = buff('Bole', 15, 0, 1.06, 0,'pot')
    badcard = buff('Balance', 15, 0, 1.03, 0, 'pot')
    notmycard = buff('Not my Card', 15, 0, 1.00, 0, 'pot')
    bigcard = buff('Lady', 15, 0, 1.08, 0, 'pot')
    divination = buff('Divination', 15, 0, 1.06, 180,'pot')
    trick = buff('Trick Attack', 10, 9.82, 1.1, 60,'pot')
    trick.activationdelay = .8
    tether = buff("Dragon Sight", 20, 1.4, 1.05, 120,'pot')
    devotion = buff("Devotion", 15, 15.0, 1.05, 180,'pot')
    brotherhood = buff("Brotherhood", 14, 10.5, 1.05, 90,'pot')
    embolden = buff("Embolden", 20, 10, 1.1, 120,'pot')
    embolden.falloff = True

    battlevoice = buff('Battle Voice', 20, 3.1, 20, 180,'dh')

    litany = buff("Battle Litany", 20, 3.1, 10, 180,'ch')
    chain = buff("Chain Stratagem", 15, 3.1, 10, 120,'ch')
    chain.activationdelay = .8
    buffs = []
    for i in party.keys():
        if i == 'NIN':
            buffs.append(trick)
        if i == 'DRG':
            buffs.append(tether)
            buffs.append(litany)
        if i == 'MNK':
            buffs.append(brotherhood)
        if i == 'RDM':
            buffs.append(embolden)
        if i == 'SMN':
            buffs.append(devotion)
        if i == 'BRD':
            buffs.append(battlevoice)
        if i == 'SCH':
            buffs.append(chain)



    dict = {}
    for i in buffs:
        dict[i.name] = i

    return dict

def genbuffs():

    flourishcascade = buff('Flourishing Cascade', 15, 0, 0, 0,'None')
    flourishfountain = buff('Flourishing Fountain', 15, 0, 0, 0,'None')
    flourishwindmill = buff('Flourishing Windmill', 15, 0, 0, 0,'None')
    flourishbloodshower = buff('Flourishing Bladeshower', 15, 0, 0, 0,'None')
    flourishfan = buff('Flourishing Fan', 15, 0, 0, 0,'None')

    potionbuff = buff('Potion', 30, 0, .1, 0,'None')

    saber = buff('Saber Dance', 15, 0, 30, 0,'cdh')
    technical = buff('Technical Finish', 15, 0, 1.05, 0,'pot')
    combo = buff('Combo', 15, 0, 0, 0,'None')
    improvbuff = buff('Improvisation', 15, 0, 3, 0,'None')

    table = [flourishcascade,flourishfountain,flourishwindmill,flourishbloodshower,flourishfan,
             potionbuff,saber,technical,combo,improvbuff]

    dict = {}
    for i in table:
        dict[i.name] = i
    return dict

def settings():
    openers = {}
    fight = {}
    with open('settings.txt', 'r') as f:
        for line in f:
            type = line.split(':')
            if type[0].lower() == 'opener':
                try:
                    type2 = type[1].split(';')
                    key = type2[0]
                    openlist = type2[1].split(',')
                    opentable = []
                    for i in openlist:
                        opentable.append(i.rstrip('\n'))
                    openers[key]= opentable
                except:
                    pass
            elif type[0].lower() == 'fight':
                try:
                    type2 = type[1].split(';')
                    key = type2[0]
                    holdlist = type2[1].split(',')
                    fighttable = []
                    for i in holdlist:
                        holdtime = []
                        parsetimes = i.split('-')
                        holdtime.append(int(parsetimes[0]))
                        holdtime.append(int(parsetimes[1]))
                        holdtime.append(bool(parsetimes[2].rstrip('/n')))
                        fighttable.append(holdtime)
                    fight[key] = fighttable
                except:
                    pass


    return [openers,fight]

