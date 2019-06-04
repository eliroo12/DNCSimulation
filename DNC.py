import random
import math
import logging

logging.basicConfig(filename='Dnc_Sim_Results.log', filemode='w', format='%(message)s', level=logging.INFO)
logging.info('---------- THE DAMAGE NUMBERS IN THIS LOG ARE BASED OF STORMSBLOOD BARDs FORMULA AND ARE NO WAY AN ACTUAL REPRESENTATION OF DAMAGE DONE. PLEASE TAKE THEM WITH A GRAIN OF SALT --------------------')

# Init Values
dex = 2820
basedex = 2820
WD = 109
JobMod = 115
gcd = 0
gcdtime = 0
feathers = 0
superfeathers = 0
espritfromself = 0
espritfromparty = 0
espritattempt = 0
espritcap = 0
espritattemptparty = 0
combodrops = 0
comboscreated = 0
feathersdropped = 0
feathertry = 0
featherattempt = 0
totalprocs = 0
procdrop = 0
det = 1587
ss = 364
crit = 2174
dh = 1224
wepdelay = 3.04
GCDrecast = 2.43
abilitydelay = .70
basecritchance = 25
basecritbonus = 1.5
basedirectchance = 35
basedirectbonus = 1.25
createlog = False

SStiers = [364,381,448,515,581,648,715,782,849,915,982,1049,1116]

techdrift = 0
standdrift = 0
techhold = 0
standhold = 0
trickstands = 0


threepercent = 0
sixpercent = 0

def determinecrit():
    global crit
    global basecritchance
    global basecritbonus

    basecritchance = math.floor(200*(crit-364)/2170+50)/10
    basecritbonus = math.floor(200*(crit-364)/2170+1400)/1000

def determinedh():
    global dh
    global basedirectchance
    basedirectchance = math.floor(550*(dh-364)/2170)/10

def determinegcd():
    global GCDrecast
    global ss
    GCDm = math.floor((1000 - math.floor(130*(ss-364)/2170))*2500/1000)
    A = math.floor(math.floor(math.floor(math.floor((100-0)*(100-0)/100)*(100-0)/100))-0)
    B = (100 - 0) / 100
    GCDc = math.floor(math.floor(math.floor(math.ceil(A*B)*GCDm/100)*100/1000)*100/100)

    GCDrecast = GCDc / 100

def returndamage(pot, auto):
    global dex
    global WD
    global JobMod
    global det
    global ss

    dexstat = math.floor(dex * 1.03)
    Damage = 0
    if auto:
        Damage = math.floor(pot * ((WD + math.floor(292 * JobMod / 1000))* (wepdelay /3)) * (100 + math.floor((dexstat - 292) * 1000 / 2336)) / 100)
        Damage = math.floor(Damage * (1000 + math.floor(130 * (det - 292) / 2170)) / 1000)
        Damage = math.floor(Damage * (1000 + math.floor(130 * (ss - 364) / 2170)) / 1000)
        Damage = math.floor(Damage * (1000 + math.floor(100 * (364 - 364) / 2170)) / 1000 / 100)
    else:
        Damage = math.floor(pot * (WD + math.floor(292 * JobMod / 1000)) * (100 + math.floor((dexstat - 292) * 1000 / 2336)) / 100)
        Damage = math.floor(Damage * (1000 + math.floor(130 * (det - 292) / 2170)) / 1000)
        Damage = math.floor(Damage * (1000 + math.floor(100 * (364 - 364) / 2170)) / 1000 / 100)

    return Damage * (random.randrange(95,105)/100)

#Specific Jobs for Buffs

astpriority = False
drgtether = False

determinecrit()
determinedh()
determinegcd()



class job:

    def __init__(self, name, role, active, gcd, nextgcd, espritrate, partner):
        self.name = name
        self.role = role
        self.active = active
        self.gcd = gcd
        self.nextgcd = nextgcd
        self.firstgcd = nextgcd
        self.espritrate = espritrate
        self.partner = partner


    def switch(self):
        self.active = not self.active

    def reset(self):
        self.nextgcd = self.firstgcd


nin = job('NIN','DPS',True, 2.4, .7, .15, True)
drg = job('DRG','DPS',True, 2.4, .7, .15, False)
mnk = job('MNK', 'DPS', False, 2.4, .7, .15, False)
sam = job('SAM', 'DPS', False, 2.4, .7, .15, False)

brd = job('BRD','DPS', False, 2.4, 0, .15, False)
mch = job('MCH', 'DPS', False, 2.4, 0, .15, False)

rdm = job('RDM', 'DPS', True, 2.4, 0, .15, False)
smn = job('SMN', 'DPS', False, 2.4, 0, .15, False)
blm = job('BLM', 'DPS', False, 2.4, 0, .15, False)

sch = job('SCH', 'HEAL', True, 2.4, 0, .15, False)
ast = job('AST', 'HEAL', True, 2.4, 0, .15, False)
whm = job('WHM', 'HEAL', False, 2.4, 0, .15, False)

gnb = job('GNB', 'TANK', False, 2.4, 0, .15, False)
war = job('WAR', 'TANK', True, 2.4, 0, .15, False)
drk = job('DRK', 'TANK', False, 2.4, 0, .15, False)
pld = job('PLD', 'TANK', True, 2.4, 0, .15, False)

jobs = [nin,drg,mnk,sam,brd,mch,rdm,smn,blm,sch,ast,whm,gnb,war,drk,pld]
party = [nin,drg,rdm,sch,ast,pld,war]

class card:

    def __init__(self, name, seal, buff):

        self.name = name
        self.seal = seal
        self.buff = buff

class ability:

    def __init__(self, name, abiltype, targtype, cooldown, potency, nextuse, combopotency, cost):
        self.name = name
        self.abiltype = abiltype
        self.targtype = targtype
        self.cooldown = cooldown
        self.potency = potency
        self.nextuse = nextuse
        self.combopotency = combopotency
        self.cost = cost

    def getpotency(self, time, needscombo, iscomboed, cdhstats, potmod):
        Auto = False
        global feathertry
        global comboscreated
        if self.name == 'Cascade':
            comboscreated = comboscreated + 1
        if self.name == 'Fountainfall' or self.name == 'Bloodshower' or self.name == 'Reverse Cascade' or self.name == 'Rising Windmill':
            feathertry = feathertry + 1
        if self.name == 'Auto':
            Auto = True
        pot = 0
        string = str(time) + ' : You use ' + str(self.name)
        if needscombo and iscomboed:
            pot = int(self.combopotency)
        else:
            pot = int(self.potency)

        pot = returndamage(pot, Auto)

        try:
            for i in potmod:
                pot = math.floor(pot*i)
        except:
            pot = pot

        if (random.randint(1, 10001) > ((10000 * (100 - cdhstats[0]))/100)): #Check Crit
            pot = pot * cdhstats[1]
            string = string + '!'
        if (random.randint(1, 10001) > ((10000 * (100 - cdhstats[2]))/100)): #Check DH
            pot = pot * cdhstats[3]
            string = string + '@'
        #pot = round(pot * potmod, 4)
        pot = round(pot,4)
        if createlog:
            logging.info(string+' - '+str(pot)+ ' damage')
        # logging.info(str(time) + ' : It hits for ' + str(pot) + ' potency')
        self.nextuse = time + self.cooldown
        return pot

    def putonCD(self,time):
        self.nextuse = round(time + self.cooldown, 2)

    def available(self,time):
        if time >= self.nextuse:
            return True
        else:
            return False
    def getrecast(self,time):
        if time >= self.nextuse:
            return 0
        else:
            return self.nextuse - time

    def setCD(self, newCD):
        self.cooldown = newCD

    def reset(self):
        self.nextuse = 0

class chargedability:

    def __init__(self, name, abiltype, targtype, cooldown, potency, nextuse, combopotency, cost, charges):
        self.name = name
        self.abiltype = abiltype
        self.targtype = targtype
        self.cooldown = cooldown
        self.potency = potency
        self.nextuse = nextuse
        self.combopotency = combopotency
        self.cost = cost
        self.charges = charges
        self.maxcooldown = charges * cooldown

    def getpotency(self, time, needscombo, iscomboed, cdhstats, potmod):
        Auto = False
        if self.name == 'Auto':
            Auto = True
        pot = 0
        string = str(time) + ' : You use ' + str(self.name)
        if needscombo and iscomboed:
            pot = int(self.combopotency)
        else:
            pot = int(self.potency)

        pot = returndamage(pot, Auto)

        try:
            for i in potmod:
                pot = math.trunc(pot*i)
        except:
            pot = pot

        if (random.randint(1, 10001) > (10000 * (100 - cdhstats[0])/100)): #Check Crit
            pot = pot * cdhstats[1]
            string = string + '@'
        if (random.randint(1, 10001) > (10000 * (100 - cdhstats[2])/100)): #Check DH
            pot = pot * cdhstats[3]
            string = string + '!'
        #pot = round(pot * potmod, 4)
        pot = round(pot,4)
        if createlog:
            logging.info(string+' - '+str(pot)+ ' damage')
        # logging.info(str(time) + ' : It hits for ' + str(pot) + ' potency')
        self.nextuse = time + self.cooldown
        return pot

    def putonCD(self,time):
        if time - self.nextuse < 90:
            self.nextuse = self.nextuse + self.cooldown
        else:
            self.nextuse = time + self.cooldown



    def available(self,time):
        if math.floor(self.charges-(self.nextuse-time)/self.cooldown) > 0:
            return True
        else:
            return False

    def getrecast(self,time):
        if time >= self.nextuse:
            return 0
        else:
            return self.nextuse - time

    def reset(self):
        self.nextuse = 0

class buff:

    def __init__(self, name, duration, starttime, potency, cooldown):

        self.name = name
        self.duration = duration
        self.starttime = starttime
        self.active = False
        self.potency = round(potency, 2)
        self.falloff = False
        self.cooldown = cooldown
        self.available = False
        self.endtime = 0
        self.default = starttime
        self.ready = False
        self.activation = 0
        self.activationdelay = .5

    def getactive(self, time):
        if self.active and (time > self.endtime):
            return False
        elif self.active:
            return True

    def activate(self, time):
        global totalprocs
        if self.active:
            return
        if self.name.split()[0] == 'Flourishing':
            totalprocs = totalprocs + 1
        if self.name == 'Combo' or self.name == 'Not my Card' or self.name =='Sleeve Draw':
            self.endtime = round(time + self.duration,2)
            self.starttime = round(time + self.cooldown,2)
            self.active = True
        else:
            self.ready = True
            self.activation = round(time + self.activationdelay, 2)


    def switchon(self,time):
        self.endtime = round(time + self.duration, 2)
        self.starttime = round(time + self.cooldown-self.activationdelay, 2)
        self.active = True
        self.ready = False
        if createlog:
            logging.info(str(time) + ": Buff / Debuff Up : " + self.name)

    def closetodrop(self, time, gcd):
        if self.active and (time > self.endtime):
            return False
        elif (time + gcd - .01) > self.endtime:
            return True
        else:
            return False

    def dropbuff(self, clock):
        if self.active:
            if createlog and not self.name == 'Combo' and not self.name == 'Not my Card' and not self.name == 'Sleeve Draw':
                logging.info(str(clock)+ ' : '+self.name+' has fallen off.')
            self.active = False

    def getpotency(self, clock):
        if not self.active:
            return 0
        elif self.falloff:
            remainingtime = self.endtime - clock
            return 1+(round(2 * math.ceil(remainingtime/4), 2)/100)
        else:
            return round(self.potency, 2)

    def returnduration(self,clock):
        if not self.active:
            return 0
        else:
            return self.endtime - clock

    def reset(self):
        self.starttime = self.default
        self.activation = 0
        self.active = False
        self.available = False
        self.ready = False

    def specialactivate(self, time, check):
        if check:
            self.potency = 1.06
        else:
            self.potency = 1.03
        self.ready = True
        self.activation = time + self.activationdelay
        if createlog and not self.name == 'Combo':
            logging.info(str(time) + ": Buff / Debuff Up : " + self.name)

class action:

    def __init__(self, id, name, actiontime):
        self.id = id
        self.name = name
        self.actiontime = actiontime

    def actionable(self, time):
        if time == self.actiontime:
            return True
        else:
            return False

autoattack = ability('Auto Attack', 'Auto', 'ST', 2.8, 100, 0, 'None', 0)
cascade = ability('Cascade', 'GCD', 'ST', GCDrecast, 250, 0, "None", 0)
fountain = ability('Fountain', 'GCD', 'ST', GCDrecast, 100, 0, 300, 0)
reversecascade = ability('Reverse Cascade', 'GCD', 'ST', GCDrecast, 350, 0, "None", 0)
fountainfall = ability('Fountainfall', 'GCD', 'ST', GCDrecast, 400, 0, "None", 0)


windmill = ability('Windmill', 'GCD', 'AE', GCDrecast, 250, 0, "None", 0)
bladeshower = ability('Bladeshower', 'GCD', 'AE', GCDrecast, 100, 0, 200, 0)
risingwindmill = ability('Rising Windmill', 'GCD', 'AE', GCDrecast, 250, 0, "None", 0)
bloodshower = ability('Bloodshower', 'GCD', 'AE', GCDrecast, 300, 0, "None", 0)


fandance1 = ability('Fan Dance I', 'OGCD', 'ST', 1, 150, 0, "None", 1)
fandance2 = ability('Fan Dance II', 'OGCD', 'AE', 1, 100, 0, "None", 1)
fandance3 = ability('Fan Dance III', 'OGCD', 'AE', 1, 200, 0, "None", 0)

devilment = ability('Devilment', 'GCD', 'AE', GCDrecast, 600, 0, "None", 50)

technicalstep = ability('Technical Step', 'GCD', 'ST', 120, 0, 0, "None", 0)
standardstep = ability('Standard Step', 'GCD', 'ST', 30, 0, 0, "None", 0)
step = ability('Step', 'GCD', 'ST', 1, 0, 0, "None", 0)
technicalfinish = ability('Technical Finish', 'GCD', 'AE', 1, 1500, 0, "None", 0)
standardfinish = ability('Standard Finish', 'GCD', 'AE', 1, 1000, 0, "None", 0)

saberdance = ability('Saber Dance', 'OGCD', 'ST', 120, 0, 0, "None", 0)
flourish = ability('Flourish', 'OGCD', 'ST', 60, 0, 0, "None", 0)
improv = ability('Improvisation', 'OGCD', 'ST', 180, 0,0,'None',0)

potion = ability('Potion of Dexterity','OGCD','ST',270, 0, 0, 'None', 0)

noaction = ability('No  Action', 'None', 'ST', 0, 0, 0, "None", 0)

abilities = [ technicalfinish , technicalstep , standardfinish , standardstep , step , cascade, fountain, reversecascade, fountainfall, windmill, bladeshower, risingwindmill, bloodshower, fandance1, fandance2, fandance3, devilment,  saberdance, flourish, noaction]

redraw = chargedability('Redraw', 'OGCD', 'ST', 30, 0, 0, "None", 0, 3)
draw = ability('Draw', 'OGCD', 'ST', 30, 0, 0, "None", 0)


flourishcascade = buff('Flourishing Cascade', 15, 0, 0, 0)
flourishfountain = buff('Flourishing Fountain', 15, 0, 0, 0)
flourishwindmill = buff('Flourishing Windmill', 15, 0, 0, 0)
flourishbloodshower = buff('Flourishing Bloodshower', 15, 0, 0, 0)
flourishfan = buff('Flourishing Fan', 15, 0, 0, 0)

potionbuff = buff('Potion of Dexterity',30, 0, .1,0)

saber = buff('Saber Dance', 15, 0, 30, 0)
technical = buff('Technical Finish', 15, 0, 1.05, 0)
combo = buff('Combo',15,0,0,0)
improvbuff = buff('Improvisation',15,0,3,0)

buffs = [flourishbloodshower, flourishcascade, flourishfan, flourishfountain, flourishwindmill, saber, technical,improvbuff, combo]

balance = card('Balance','Solar', False)
bole = card('Bole','Solar',True)
arrow = card('Arrow','Lunar',False)
ewer = card('Ewer','Lunar',True)
spear = card('Spear','Celestial',False)
spire = card('Spire','Celestial', True)
dummy = card('LordLady','Nope', True)

deck = [balance,bole,arrow,ewer,spear,spire]

goodcard = buff('Bole',15,0,1.06,0)
badcard = buff('Balance',15,0,1.03,0)
notmycard = buff('Not my Card', 15, 0, 1.00, 0)
bigcard = buff('Lady',15,0,1.08,0)

divination = buff('Divination',15,0,1.06,180)
sleeve = ability('Sleeve Draw', 'OGCD', 'ST', 180, 0, 0, "None", 0)
sleevebuff = buff('Sleeve Draw', 15, 0, 0, 0)

trick = buff('Trick Attack',10, 9.82, 1.1, 60)
trick.activationdelay = .8
tether = buff("Dragon Sight", 20, 1.4, 1.05, 120)
devotion = buff("Devotion", 15, 15.0, 1.05, 180)
brotherhood = buff("Brotherhood", 14, 10.5, 1.05, 90)
embolden = buff("Embolden", 20, 10, 1.1, 120)
embolden.falloff = True

battlevoice = buff('Battle Voice', 20, 3.1, 20, 180)

litany = buff("Battle Litany", 20, 3.1, 10, 180)
chain = buff("Chain Stratagem", 15, 3.1, 10, 120)

potencybuffs = [trick, tether, devotion, brotherhood, embolden, goodcard, badcard, bigcard, divination]
astbuffs = [goodcard, badcard, bigcard, divination]
critbuffs = [litany, chain]
dhbuffs = [battlevoice]

def reset():

    for i in party:
        i.reset()

    for i in abilities:
        i.reset()

    for i in potencybuffs:
        i.reset()

    for i in critbuffs:
        i.reset()

    for i in dhbuffs:
        i.reset()

    for i in buffs:
        i.reset()

    autoattack.reset()
    combo.reset()
    redraw.reset()
    sleeve.reset()
    sleevebuff.reset()
    draw.cooldown = 30
    draw.reset()
    potion.reset()
    global dex
    global basedex
    dex = basedex

def buildparty():
    global jobs
    global party
    party = []
    for i in jobs:
        if i.active:
            party.append(i)

    tanks = 0
    healers = 0
    dps = 0

    if len(party)==0:
        return True

    for i in party:
        if i.role == 'DPS':
            dps = dps + 1
        elif i.role == 'HEAL':
            healers = healers + 1
        elif i.role =='TANK':
            tanks = tanks + 1
        yesno = ['1: Yes', '2: No']
        if i.name == 'DRG':
            global drgtether
            try:
                for up in yesno:
                    print(up)
                choice = int(input('Will the DRG Tether be on you? '))
                if choice == 1:
                    drgtether = True
                else:
                    drgtether = False
            except:
                drgtether = False
        if i.name == 'AST':
            global astpriority
            try:
                for up in yesno:
                    print(up)
                choice = int(input('Will you be the ASTs Priority? '))
                if choice == 1:
                    astpriority = True
                else:
                    astpriority = False
            except:
                astpriority = False

    if tanks > 2:
        return False
    if healers > 2:
        return False
    if dps > 3:
        return False
    if tanks + healers + dps > 7:
        return False

    return True

def makebuffsavailable():
    global drgtether
    for i in potencybuffs:
        i.available = False
    for i in critbuffs:
        i.available = False
    for i in dhbuffs:
        i.available = False

    if nin.active:
        trick.available = True
    if drg.active:
        litany.available = True
        if drgtether:
            tether.available = True
    if smn.active:
        devotion.available = True
    if mnk.active:
        brotherhood.available = True
    if rdm.active:
        embolden.available = True
    if brd.active:
        battlevoice.available = True
    if sch.active:
        chain.available = True

    potionbuff.available = True

def cascadecombo(iterations):
    i = 0
    iterations = int(iterations)
    potency = 0
    gcd = 0
    feathers = 0
    superfeathers = 0
    esprit = 0
    while i < iterations:
        potency = potency + cascade.potency + fountain.combopotency
        gcd = gcd + 2
        esprit = esprit + buildesprit(0, esprit)
        esprit = esprit + buildesprit(0, esprit)
        # Cascade RNG
        if (random.randint(1, 10001) > 10000 * .5):
            potency = potency + reversecascade.potency
            esprit = esprit + buildesprit(0,esprit)
            gcd = gcd + 1
            if (random.randint(1, 10001) > 10000 * .5):
                potency = potency + fandance1.potency
                feathers = feathers + 1
                if (random.randint(1, 10001) > 10000 * .5):
                    potency = potency + fandance3.potency
                    superfeathers = superfeathers + 1

        # Fountain RNG
        if (random.randint(1, 10001) > 10000 * .5):
            potency = potency + fountainfall.potency
            esprit = esprit + buildesprit(0, esprit)
            gcd = gcd + 1
            if (random.randint(1, 10001) > 10000 * .5):
                potency = potency + fandance1.potency
                feathers = feathers + 1
                if (random.randint(1, 10001) > 10000 * .5):
                    potency = potency + fandance3.potency
                    superfeathers = superfeathers + 1

        if esprit >= 50:
            gcd = gcd + 1
            potency = potency + 600
            esprit = esprit - 50
            esprit = esprit + buildesprit(0,esprit)

        i = i + 1
        #if (i > iterations):
         #   break
    potency = potency + (esprit/10*50)
    if createlog:
        logging.info('Total Potency: ' + str(potency))
    if createlog:
        logging.info('Total GCDs: ' + str(gcd))
    if createlog:
        logging.info('Potency per GCD: ' + str(potency / gcd))
    if createlog:
        logging.info('Feathers: ' + str(feathers))
    if createlog:
        logging.info('Flourished Fans: ' + str(superfeathers))
    if createlog:
        logging.info('Feathers per GCD: ' + str(feathers / gcd))
    if createlog:
        logging.info('Fan Dance III per GCD: ' + str(superfeathers / gcd))
    if createlog:
        logging.info('Left Over Esprit: ' + str(esprit))

def AoEcombos(iterations,mobs):
    i = 0
    stpot = 0
    stgcds = 0
    aoepot = 0
    aoegcds = 0
    justaepot = 0
    justaegcds = 0
    ffpotcalc = 0
    rcpotcalc = 0

    caspot = 250
    founpot = 300
    ffpot = 400
    rcpot = 350
    wmpot = 150
    bspot = 200
    bloodpot = 300 # 50% after first
    rmpot = 250 #50% after first
    fdIIpot = 100
    fdIIIpot = 200 #50% after first

    while i < iterations:

    #st AoE calcs:
        stpot = stpot + caspot + founpot
        stgcds = stgcds + 2
        if checkproc(): #RC Proc
            stpot = stpot + rcpot
            stgcds = stgcds + 1
            if checkproc():
                stpot = stpot + (fdIIpot * mobs)
                if checkproc():
                    stpot = stpot + fdIIIpot
                    x = 1
                    while x < mobs:
                        stpot = stpot + (fdIIIpot*.5)
                        x = x + 1

        if checkproc(): # FF Proc
            stpot = stpot + ffpot
            stgcds = stgcds + 1
            if checkproc():
                stpot = stpot +(fdIIpot * mobs)
                if checkproc():
                    stpot = stpot + fdIIIpot
                    x = 1
                    while x < mobs:
                        stpot = stpot + (fdIIIpot*.5)
                        x = x + 1

    # AoE calcs:
        aoepot = aoepot + (wmpot*mobs) + (bspot*mobs)
        justaepot = justaepot + (wmpot*mobs) + (bspot*mobs)
        aoegcds = aoegcds + 2
        justaegcds = justaegcds + 2

        if checkproc(): #RM proc
            aoepot = aoepot + rmpot
            aoegcds = aoegcds + 1
            x = 1
            while x < mobs:
                aoepot = aoepot + (rmpot * .5)
                x = x + 1
            if checkproc():
                aoepot = aoepot + (fdIIpot * mobs)
                if checkproc():
                    aoepot = aoepot + fdIIIpot
                    x = 1
                    while x < mobs:
                        aoepot = aoepot + (fdIIIpot * .5)
                        x = x + 1

        if checkproc():  # Bloodproc
            aoepot = aoepot + bloodpot
            aoegcds = aoegcds + 1
            x = 1
            while x < mobs:
                aoepot = aoepot + (bloodpot * .5)
                x = x + 1
            if checkproc():
                aoepot = aoepot + (fdIIpot * mobs)
                if checkproc():
                    aoepot = aoepot + fdIIIpot
                    x = 1
                    while x < mobs:
                        aoepot = aoepot + (fdIIIpot * .5)
                        x = x + 1


        #just FC and RC pot Cals
        rcpotcalc = rcpotcalc + rcpot
        ffpotcalc = ffpotcalc + ffpot
        if checkproc():
            rcpotcalc = rcpotcalc + (fdIIpot*mobs)
            ffpotcalc = ffpotcalc + (fdIIpot*mobs)
            if checkproc():
                rcpotcalc = rcpotcalc + fdIIIpot
                ffpotcalc = ffpotcalc + fdIIIpot
                x = 1
                while x < mobs:
                    rcpotcalc = rcpotcalc + (fdIIIpot * .5)
                    ffpotcalc = ffpotcalc + (fdIIIpot * .5)
                    x = x + 1


        i = i + 1

    stpot = round(stpot / stgcds, 4)
    aoepot = round(aoepot / aoegcds, 4)
    justaepot = round(justaepot / justaegcds, 4)
    ffpotcalc = round(ffpotcalc / iterations, 4)
    rcpotcalc = round(rcpotcalc / iterations, 4)

    return [stpot,aoepot,ffpotcalc,rcpotcalc]


def getfeathers(clock, feathers):
    global featherattempt
    global feathersdropped
    featherattempt = featherattempt + 1
    if feathers >= 4:
        feathersdropped = feathersdropped + 1
        if createlog:
            logging.info(str(clock)+ ' : You cannot get anymore Feathers')
        return 0
    if (random.randint(1, 10001) > 10000 * .5):
        #if createlog: logging.info(str(clock)+ ' : You get one feather')
        return 1
    else:
        return 0

def buildesprit(clock,esprit):
    global espritfromself
    global espritattempt
    global espritcap
    espritattempt = espritattempt + 1
    if (random.randint(1, 10001) > 10000 * .85):
        if esprit >= 100:
            espritcap = espritcap + 1
            if createlog:
                logging.info(str(clock) + ': You cannot build more Esprit')
            return 0
        espritfromself = espritfromself + 10
        return 10
    else:
        return 0

def partybuildesprit(clock,esprit, rate):
    global espritfromparty
    global espritattemptparty
    global espritcap
    espritattemptparty = espritattemptparty + 1
    if (random.randint(1, 10001) > 10000 * (1-rate)):
        if esprit >= 100:
            espritcap = espritcap + 1
            if createlog:
                logging.info(str(clock) + ': You cannot build more Esprit')
            return 0
        espritfromparty = espritfromparty + 10
        return 10
    else:
        return 0

def drawcard(currentseals, allseals, clock):
    drawing = True
    card= 0
    oldcard = 'None'
    #print(currentseals)
    redrawnumber = 0
    if allseals:
        cardnumber = random.randrange(0, 6)
        card = deck[cardnumber]
        if card.buff == False:
            return ['Lord', card, .7]
        else:
            return ['Lady', card, .7]
    while(drawing):
        clocktime = .7
        if redrawnumber == 1:
            clocktime = 3.1
        elif redrawnumber == 2:
            clocktime = 3.8
        elif redrawnumber > 2:
            clocktime = 5.2
        cardnumber = random.randrange(0,6)
        card = deck[cardnumber]
        if card.name == oldcard:
            while card.name == oldcard:
                cardnumber = random.randrange(0, 6)
                card = deck[cardnumber]
        foundseal = False
        for i in currentseals:
            if i == card.seal:
                foundseal = True
        if not foundseal:
            drawing = False
        if foundseal and redraw.available(round(clock+redrawnumber,2)):
            redraw.putonCD(round(clock+redrawnumber,2))
            redrawnumber = redrawnumber + 1
        elif foundseal:
            if card.buff == False:
                return ['Lord', card, clocktime]
            else:
                return ['Lady', card, clocktime]
    return [card.name,card,clocktime]

def justdraw(currentseals, allseals, clock):
    cardnumber = random.randrange(0, 6)
    card = deck[cardnumber]
    return [card.name, card, 0]

def checkseals(currentseals):
    Lunar = False
    Solar = False
    Celestial = False
    for i in currentseals:
        if i == 'Lunar':
            Lunar = True
        if i == 'Solar':
            Solar = True
        if i == 'Celestial':
            Celestial = True

    if Lunar and Solar and Celestial:
        return True
    else:
        return False

def checkproc():
    if (random.randint(1, 10001) > 10000 * .50):
        return True
    else:
        return False

def countprocs(clock):

    procounter = 0
    if flourishbloodshower.getactive(clock):
        procounter = procounter + 1
    if flourishwindmill.getactive(clock):
        procounter = procounter + 1
    if flourishcascade.getactive(clock):
        procounter = procounter + 1
    if flourishfountain.getactive(clock):
        procounter = procounter + 1

    return procounter

def buildopentable(opener):
   # opener = ['Hold 1','Standard Finish', 'Flourish', 'Rising Windmill', 'Bloodshower', 'Hold 1.70', 'Saber Dance', 'Technical Step', 'AutoOGCD 1',
    #          'AutoGCD', 'AutoOGCD 2','Standard Step','AutoOGCD 2', 'AutoGCD']
    actiontable = []
    clock = 0
    nextgcd = 0
    nextaction = 0
    global GCDrecast
    global abilitydelay
    for i in opener:
        clock = round(clock, 2)
        if i.split()[0]== 'Hold':
            actiontable.append(action(19, 'Hold', clock))
            clock = clock + float(i.split()[1])
        elif i.split()[0] == 'Technical':
            if nextgcd > clock:
                clock = round(nextgcd, 2)
            if nextaction > clock:
                clock = round(nextaction,2)
            if i.split()[1] == 'Step':
                actiontable.append(action(1, 'Technical Step', clock))
                clock = round(clock + 1.5, 2)
                counter = 0
                while counter < 4:
                    counter = counter + 1
                    actiontable.append(action(4, 'Step', clock))
                    clock = round(clock + 1, 2)
                actiontable.append(action(0, 'Technical Finish', clock))
                nextgcd = round(clock + 1.5, 2)
                nextaction = round(clock + abilitydelay, 2)
                clock = round(clock + abilitydelay, 2)
            elif i.split()[1] == 'Finish':
                actiontable.append(action(0, 'Technical Finish', clock))
                nextgcd = round(clock + 1.5, 2)
                nextaction = round(clock + abilitydelay,2)
                clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Standard':
            if nextgcd > clock:
                clock = round(nextgcd,2)
            if nextaction > clock:
                clock = round(nextaction,2)
            if i.split()[1] == 'Step':
                actiontable.append(action(3, 'Standard Step', clock))
                clock = round(clock + 1.5 , 2)
                counter = 0
                while counter < 2:
                    counter = counter + 1
                    actiontable.append(action(4, 'Step', clock))
                    clock = round(clock + 1.0, 2)
                actiontable.append(action(2, 'Standard Finish', clock))
                nextgcd = round(clock + 1.5, 2)
                nextaction = round(clock + abilitydelay, 2)
                clock = round(clock + abilitydelay, 2)
            elif i.split()[1] == 'Finish':
                actiontable.append(action(2, 'Standard Finish', clock))
                nextgcd = round(clock + 1.5, 2)
                nextaction = round(clock + abilitydelay, 2)
                clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Potion':
            actiontable.append(action(19,'Potion',clock))
            nextaction = round(clock + 1.5, 2)
            clock = round(clock + 1.5, 2)
        elif i.split()[0] == 'AutoGCD':
            if nextgcd > clock:
                clock = round(nextgcd, 2)
            if nextaction > clock:
                clock = round(nextaction, 2)
            actiontable.append(action(19, 'AutoGCD', clock))
            nextgcd = round(clock + GCDrecast, 2)
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'ReverseProc': # Special selection for opener to drop combo for proc if obtained
            if nextgcd > clock:
                clock = round(nextgcd, 2)
            if nextaction > clock:
                clock = round(nextaction, 2)
            actiontable.append(action(19, 'ReverseProc', clock))
            nextgcd = round(clock + GCDrecast, 2)
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'AutoOGCD':
            limit = int(i.split()[1])
            counter = 0
            while limit > counter:
                counter = counter + 1
                if nextaction > clock:
                    clock = round(nextaction,2)
                actiontable.append(action(19, 'AutoOGCD', clock))
                nextaction = round(clock + abilitydelay, 2)
        else:
            identify = 0
            for u in abilities:
                if u.name == i:
                    if u.abiltype == 'GCD':
                        if nextgcd > clock:
                            clock = round(nextgcd, 2)
                        if nextaction > clock:
                            clock = round(nextaction, 2)
                        actiontable.append(action(identify, u.name, clock))
                        nextgcd = round(clock + GCDrecast, 2)
                        nextaction = round(clock + abilitydelay, 2)
                        clock = round(clock + abilitydelay, 2)
                    else:
                        if nextaction > clock:
                            clock = round(nextaction, 2)
                        actiontable.append(action(identify,u.name, clock))
                        nextaction = round(clock + abilitydelay, 2)
                        clock = round(clock + abilitydelay, 2)
                identify = identify + 1
    return actiontable

def buildasttable():
    #opener = ['Hold .7','GCD','Play', 'oGCD', 'GCD', 'Draw', 'Sleeve Draw', 'GCD', 'Play', 'Draw', 'GCD', 'Redraw','Play','GCD', 'Divination']
    #opener = ['Hold .7', 'GCD', 'Play', 'oGCD', 'GCD', 'Draw', 'Sleeve Draw','GCD', 'Play', 'Draw', 'GCD', 'Play', 'Divination']
    opener = ['Hold .7', 'GCD','Play', 'oGCD','GCD','Draw','Sleeve Draw', 'GCD', 'Play','Draw','Redraw', 'GCD','Redraw','Redraw','Play', 'GCD','Divination']
    #opener = ['Hold .7', 'GCD', 'Play', 'oGCD', 'GCD', 'Draw', 'Sleeve Draw', 'GCD', 'Redraw', 'Play', 'Draw', 'Redraw','Redraw','Play', 'Divination', 'GCD']

    actiontable = []
    clock = 0
    nextgcd = 0
    nextaction = 0
    astrecast = 2.4
    global GCDrecast
    global abilitydelay
    for i in opener:
        clock = round(clock, 2)
        if i.split()[0] == 'Hold':
            actiontable.append(action(19, 'Hold', clock))
            clock = clock + float(i.split()[1])
        elif i.split()[0] == 'GCD':
            if nextgcd > clock:
                clock = round(nextgcd, 2)
            if nextaction > clock:
                clock = round(nextaction, 2)
            actiontable.append(action(100,'GCD',clock))
            nextgcd = round(clock + astrecast, 2)
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Play':
            actiontable.append(action(100,'Play',clock))
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'oGCD':
            actiontable.append(action(100,'oGCD',clock))
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Draw':
            actiontable.append(action(100, 'Draw', clock))
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Sleeve':
            actiontable.append(action(100, 'Sleeve Draw', clock))
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Redraw':
            actiontable.append(action(100, 'Redraw', clock))
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Divination':
            actiontable.append(action(100, 'Divination', clock))
            nextaction = round(clock + abilitydelay, 2)
            clock = round(clock + abilitydelay, 2)
        elif i.split()[0] == 'Minor':
            actiontable.append(action(100,'Minor Arcana', clock))

    return actiontable


def sim(openset, timetorun):
    reset()
    global GCDrecast
    global abilitydelay
    global basecritchance
    global basecritbonus
    global basedirectchance
    global basedirectbonus
    global dex
    global party
    global espritfromparty
    global espritfromself
    global combodrops
    global procdrop
    global techdrift
    global standdrift
    global standhold
    global techhold
    global trickstands

    basedex = dex
    clock = 0
    timerfinish = timetorun
    partygcd = GCDrecast
    potency = 0
    modGCDrecast = GCDrecast
    critchance = basecritchance
    critbonus = basecritbonus
    directchance = basedirectchance
    directbonus = basedirectbonus

    buffwindow = True
    buffwindowend = 0
    makebuffsavailable()
    opener = buildopentable(openset)
    stillinopener = True
    posinopen = 0
    lastbuffwindow = 0

    nextgcd = 0
    nextaction = 0
    standarddancing = False
    technicaldancing = False
    stepsneeded = 0
    nextpartygcd = .7
    esprit = 0
    feathers = 0
    saberfirst = False
    technicalfirst = False
    ignoreabilitydelay = False
    technicalhold = False
    standardhold = False

    technicalholdlist=[2.50,2.49,2.48,2.44,2.43,2.38]
    standardholdlist = [2.5,2.49,2.48]

    for i in technicalholdlist:
        if i == GCDrecast:
            technicalhold = True

    for i in standardholdlist:
        if i == GCDrecast:
            standardhold = True

    partnerloc = 0
    partyindex = 0

# Auto Information
    nextauto = 1

# AST Stuff
#clock,currentseals,allseals,nextaction,sleevestacks,nextgcd,card,cardheld,arcana,astopen,astopener,inastopen
    astinformation = [[], False, 0, 0, 0, justdraw([],False,0), True, False, True, buildasttable(), 0, astpriority,[],[],False,0]

# Values to keep track and help print updates

    oldpot = 0
    oldfeathers = 0
    oldesprit = 0
    gcd = 0
    feathersused = 0
    flourishedfans = 0
    useddevilments = 0

    fandance1.nextuse = 1
    fandance3.nextuse = 1


    while clock < timerfinish:

        totalbuffs = 0
     #   if trick and trickend == clock:
     #       if createlog: logging.info(str(clock) +' : Trick Attack wears off')
     #       trick = False
     #   elif not trick and tricktime == clock and nin:
     #       if createlog: logging.info(str(clock) + ' : Trick Attack is Up')
     #       trick = True
     #       trickend = tricktime + trickduration
     #       tricktime = tricktime + trickrecast


        potmod = [1.20, 1.05]
        dex = basedex
        modGCDrecast = GCDrecast
        critchance = basecritchance
        critbonus = basecritbonus
        directchance = basedirectchance
        directbonus = basedirectbonus
        postcombo = combo.getactive(clock)
        usedfountain = False

        if potionbuff.available:
            if potionbuff.ready and potionbuff.activation == clock:
                potionbuff.switchon(clock)
            if potionbuff.getactive(clock):
                if dex * potionbuff.potency > 225:
                    dex = dex + 225
                else:
                    dex = dex + (dex*potionbuff.potency)
            elif potionbuff.active:
                potionbuff.dropbuff(clock)
                dex = basedex

        if ast.active:
            astinformation = astmodule(clock,astinformation)
            for i in astbuffs:
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if i.getactive(clock):
                    potmod.append(i.getpotency(clock))
                elif not i.getactive(clock) and i.active:
                    i.dropbuff(clock)

        for i in potencybuffs:
            if i.available:
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if not i.ready and i.starttime == clock:
                    i.activate(clock)
                if i.getactive(clock):
                    potmod.append(i.getpotency(clock))
                    totalbuffs = totalbuffs + 1
                elif i.available and not i.getactive(clock) and i.active:
                    i.dropbuff(clock)
        for i in dhbuffs:
            if i.available:
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if not i.ready and i.starttime == clock:
                    i.activate(clock)
                if i.getactive(clock):
                    directchance = round(directchance + i.getpotency(clock), 2)
                    totalbuffs = totalbuffs + 1
                elif i.available and not i.getactive(clock) and i.active:
                    i.dropbuff(clock)
        for i in critbuffs:
            if i.available:
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if not i.ready and i.starttime == clock:
                    i.activate(clock)
                if i.getactive(clock):
                    critchance = round(critchance + i.getpotency(clock), 2)
                    totalbuffs = totalbuffs + 1
                elif i.available and not i.getactive(clock) and i.active:
                    i.dropbuff(clock)

        for i in buffs:
            if i.ready and i.activation == clock:
                i.switchon(clock)

        if technical.getactive(clock):
            potmod.append(1.05)
            totalbuffs = totalbuffs + 1
        elif technical.active:
            technical.dropbuff(clock)

        if saber.getactive(clock):
            critchance = round(critchance + saber.getpotency(clock), 2)
            directchance = round(directchance + saber.getpotency(clock), 2)
            totalbuffs = totalbuffs + 1
        elif saber.active:
            saber.dropbuff(clock)

        for i in buffs:
            if i.active and (not i.getactive(clock)):
                if not i.name == 'Combo':
                    if createlog:
                        procdrop = procdrop + 1
                        logging.info(str(clock)+' : You lost the proc '+ i.name)
                else:
                    combodrops = combodrops + 1
                    if createlog:
                        logging.info(str(clock) + ' : You lost a combo')
                i.dropbuff(clock)


        if nin.active and trick.getactive(clock):
            buffwindow = True
            lastbuffwindow = clock
        elif saber.getactive(clock):
            buffwindow = True
            lastbuffwindow = clock
        elif drg.active and brd.active and battlevoice.getactive(clock) and litany.getactive(clock):
            buffwindow = True
            lastbuffwindow = clock
        else:
            buffwindow = False

        # Let's Jump through time to figure out our next buff window
        foundnextbuffwindow = False
        nextbuffwindow = clock
        nextdance = clock
        nextdancetype = 'None'
        dancenumber = 0
        standardtimer = 0
        technicaltimer = 0
        actualnextdance = 0 #Because I don't want to change the code, Next dance is sometimes a lie!!!

        standardrecast = round(standardstep.getrecast(clock),2)
        technicalrecast = round(technicalstep.getrecast(clock),2)
        if standardrecast - 15 <= 0:
            nextdancetype = 'Standard'
            nextdance = round(clock + standardrecast, 2)
            dancenumber = dancenumber + 1
            standardtimer = round(clock + standardrecast, 2)
        if technicalrecast - 15 <= 0:
            nextdancetype = 'Technical'
            nextdance = round(clock + technicalrecast, 2)
            dancenumber = dancenumber + 1
            technicaltimer = round(clock + standardrecast, 2)
        ## Lots of fun dancing logic used to figure out if I'm dancing soon or not and what dances are coming and when technical is coming
        # Could consolidate this to less code if ever needed, some redundancy here
        if technicaltimer == 0:
            standardtimer = actualnextdance
        elif standardtimer == 0:
            technicaltimer = actualnextdance
        elif technicaltimer > standardtimer:
            standardtimer = actualnextdance
        else:
            technicaltimer = actualnextdance

        if (nextgcd == clock or (nextaction == clock and (flourishfan.getactive(clock)))) and clock - lastbuffwindow > 30 :
            while(not foundnextbuffwindow):
                nextbuffwindow = round(nextbuffwindow + .01, 2)
                if nin.active and trick.starttime == nextbuffwindow:
                    foundnextbuffwindow = True
                elif saber.starttime == nextbuffwindow:
                    foundnextbuffwindow = True
                elif drg and brd and battlevoice.starttime == nextbuffwindow:
                    foundnextbuffwindow = True
                elif nextbuffwindow > (clock + 15): # I don't really care if the buffwindow is greater than 20s away
                    foundnextbuffwindow = True

        CDHStats = [critchance, critbonus, directchance, directbonus]
        # Handle Esprit

        for i in party:
            if i.nextgcd == clock:
                i.nextgcd = round(clock + i.gcd, 2)
                if technical.getactive(clock):
                    esprit = esprit + partybuildesprit(clock,esprit,i.espritrate)
                elif i.partner:
                    esprit = esprit + partybuildesprit(clock, esprit, i.espritrate)
        # Handle Auto
        if clock == nextauto:
            potency = potency + autoattack.getpotency(clock,False,False,CDHStats,potmod)
            nextauto = round(clock + autoattack.cooldown,2)


        #Handle Opener if available

        if stillinopener:
            if opener[posinopen].actionable(clock):
                currentaction = opener[posinopen]
                if abilities[currentaction.id].name == 'Technical Finish':
                    potency = potency + technicalfinish.getpotency(clock, False, False, CDHStats, potmod)
                    technical.activate(clock)
                    nextgcd = round(clock + 1.5,2)
                elif abilities[currentaction.id].name == 'Standard Finish':
                    potency = potency + standardfinish.getpotency(clock,False,False,CDHStats,potmod)
                    nextgcd = round(clock + 1.5,2)
                elif abilities[currentaction.id].name == 'Saber Dance':
                    if createlog:
                        logging.info(str(clock)+' : You use Saber Dance!')
                    if not technicalfirst:
                        saberfirst = True
                    saber.activate(clock)
                    abilities[currentaction.id].putonCD(clock)
                elif abilities[currentaction.id].name == 'Flourish':
                    if createlog:
                        logging.info(str(clock)+' : You use Flourish!')
                    flourishcascade.activate(clock)
                    flourishwindmill.activate(clock)
                    flourishfountain.activate(clock)
                    flourishbloodshower.activate(clock)
                    flourishfan.activate(clock)
                    abilities[currentaction.id].putonCD(clock)
                elif currentaction.name == 'Potion':
                    if createlog:
                        logging.info(str(clock)+' : You use a Potion!')
                    potion.putonCD(clock)
                    potionbuff.activate(clock)
                elif currentaction.name == 'ReverseProc' and flourishcascade.getactive(clock):
                    potency = potency + reversecascade.getpotency(clock,False,False,CDHStats, potmod)
                    gcd = gcd + 1
                    flourishcascade.dropbuff(clock)
                    feathers = feathers + getfeathers(clock,feathers)
                    esprit = esprit + buildesprit(clock,esprit)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'AutoGCD' or currentaction.name =='ReverseProc':
                    #Auto GCD in the opener
                    # If technical is active and Esprit > 80 - Use Devilment
                    # If we are to lose any procs do them in the following order Fountfall > Cascade > bloodshower > windmill
                    # If we are in a buffwindo and esprit is great than or equal to 50 then use Devilment
                    # If we are in a combo and flourishfountain is not active and our combo will drop - Use Fountain
                    # Use Flourishes in this order : Fountainfall >  Reverse Cascade > Blood > Rising
                    # If esprit is 90 or above use Devilment
                    # If combo use Fountain
                    # Else use Cascade
                    proccount = countprocs(clock)
                    procgcd = proccount * modGCDrecast
                    nextgcd = round(clock + modGCDrecast, 2)
                    if technical.getactive(clock) and esprit > 80 : #If we Technical is out and we have 90+ Esprit, Go now
                        potency = potency + devilment.getpotency(clock,False,False,CDHStats,potmod)
                        useddevilments = useddevilments + 1
                        esprit = esprit - devilment.cost
                        gcd = gcd + 1
                    elif flourishfountain.getactive(clock) and flourishfountain.closetodrop(clock, procgcd): #Check to see if Flourish Fountain is close to dropping
                        potency = potency + fountainfall.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishcascade.getactive(clock) and flourishcascade.closetodrop(clock, procgcd): #Check if Reverse Cascade is close to dropping
                        potency = potency + reversecascade.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishbloodshower.getactive(clock) and flourishbloodshower.closetodrop(clock, procgcd): #Check if Bloodshower is close to fall
                        potency = potency + bloodshower.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishwindmill.getactive(clock) and flourishwindmill.closetodrop(clock, procgcd): # Check if Windmill is close to fall
                        potency = potency + risingwindmill.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif buffwindow and esprit >= 50:   # I want to use devilment in the buff window
                        potency = potency + devilment.getpotency(clock,False,False,CDHStats,potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                    elif combo.getactive(clock) and not flourishfountain.getactive(clock) and combo.closetodrop(clock,modGCDrecast): #First We check to see if we are in combo and don't have Flourished Fountain
                        potency = potency + fountain.getpotency(clock, True, True, CDHStats, potmod)
                        combo.dropbuff(clock)
                        usedfountain = True
                        gcd = gcd + 1
                        if checkproc():
                            flourishfountain.activate(clock)
                    elif flourishfountain.getactive(clock):  # Check to see if Flourish Fountain is up
                        potency = potency + fountainfall.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishcascade.getactive(clock):  # Check if Reverse Cascade is up
                        potency = potency + reversecascade.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishbloodshower.getactive(clock):  # Check if Bloodshower is up
                        potency = potency + bloodshower.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishwindmill.getactive(clock):  # Check if Windmill is up
                        potency = potency + risingwindmill.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif esprit > 80:
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                    elif combo.getactive(clock): # If we are in combo we are doing fountain here
                        potency = potency + fountain.getpotency(clock,True,True,CDHStats,potmod)
                        gcd = gcd + 1
                        usedfountain = True
                        combo.dropbuff(clock)
                        if checkproc():
                            flourishfountain.activate(clock)
                    else:  # If all else fails we go into Cascade combo
                        potency = potency + cascade.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        combo.activate(clock)
                        if checkproc():
                            flourishcascade.activate(clock)
                    esprit = esprit + buildesprit(clock,esprit) #Check if we get Esprit from this GCD
                elif currentaction.name == 'AutoOGCD':
                # AutoOGCD in the opener
                # If flourish is up, we have no procs - Use it
                # If flourish fan is up use FD3
                # if we are in the buffwindow and have feathers and can use FD1 use FD1
                #If we have 4 feathers and FD1 is up use FD1
                #push the oGCD further if we have more feathers. at a 2.4 gcd we can get two in
                    if flourish.available(clock) and countprocs(clock) == 0 and not flourishfan.getactive(clock):
                        if createlog:
                            logging.info(str(clock) + ' : You use Flourish!')
                        flourishcascade.activate(clock)
                        flourishwindmill.activate(clock)
                        flourishfountain.activate(clock)
                        flourishbloodshower.activate(clock)
                        flourishfan.activate(clock)
                        flourish.putonCD(clock)
                    elif flourishfan.getactive(clock) and fandance3.available(clock):
                        potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                        flourishedfans = flourishedfans + 1
                        flourishfan.dropbuff(clock)
                    elif buffwindow and feathers > 0 and fandance1.available(clock):
                        potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                        feathers = feathers - 1
                        feathersused = feathersused + 1
                        if checkproc():
                            flourishfan.activate(clock)
                    elif feathers > 3 and fandance1.available(clock):
                        potency = potency + fandance1.getpotency(clock,False,False,CDHStats, potmod)
                        feathersused = feathersused + 1
                        feathers = feathers - 1
                        if checkproc():
                            flourishfan.activate(clock)
                    elif currentaction.actiontime + .7 < nextgcd and feathers > 0:
                        currentaction.actiontime = round(clock + .01, 2)
                        posinopen = posinopen - 1
                elif currentaction.name == 'Hold':
                    if createlog:
                        logging.info(str(clock)+' : Waiting')
                elif currentaction.name == 'Technical Step':
                    if createlog:
                        logging.info(str(clock)+' : You begin Technical Step')
                    if not saberfirst:
                        technicalfirst = True
                    abilities[currentaction.id].putonCD(clock)
                elif currentaction.name == 'Standard Step':
                    if createlog:
                        logging.info(str(clock)+' : You begin Standard Step')
                    abilities[currentaction.id].putonCD(clock)
                elif currentaction.name == 'Fountain':
                    potency = potency + fountain.getpotency(clock,True,True,CDHStats,potmod)
                    gcd = gcd + 1
                    usedfountain = True
                    combo.dropbuff(clock)
                    if checkproc():
                        flourishfountain.activate(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                elif currentaction.name == 'Cascade':
                    potency = potency + cascade.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    combo.activate(clock)
                    if checkproc():
                        flourishcascade.activate(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                elif currentaction.name == 'Fan Dance I':
                    if feathers > 0:
                        potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                        feathersused = feathersused + 1
                        feathers = feathers - 1
                    if checkproc():
                        flourishfountain.activate(clock)
                elif currentaction.name == 'Fan Dance III':
                    if flourishfan.getactive(clock):
                        potency = potency + fandance3.getpotency(clock,False,False,CDHStats,potmod)
                        flourishedfans = flourishedfans + 1
                        flourishfan.dropbuff(clock)
                elif currentaction.name == 'Fountainfall':
                    potency = potency + fountainfall.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    flourishfountain.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'Reverse Cascade':
                    potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                    gcd = gcd + 1
                    flourishcascade.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'Bloodshower':
                    potency = potency + bloodshower.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    flourishbloodshower.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'Rising Windmill':
                    potency = potency + risingwindmill.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    flourishwindmill.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                posinopen = posinopen + 1
                if posinopen >= len(opener):
                    if createlog:
                        logging.info('Finished with Opener, commencing Sim')
                    #Let's figure out when our last GCD was
                    foundlastGCD = False
                    foundlastaction = False
                    while(not foundlastGCD):
                        currentaction = opener[posinopen-1]
                        if currentaction.name.split()[0] == 'Technical' or currentaction.name.split()[0] == 'Standard':
                            if not foundlastaction:
                                foundlastaction = True
                                nextaction = round(clock + abilitydelay, 2)
                            if currentaction.name.split()[1] == 'Finish':
                                foundlastGCD = True
                                nextgcd = round(clock + 1.5, 2)
                        elif currentaction.name == 'AutoGCD' or abilities[currentaction.id].abiltype == 'GCD':
                            if not foundlastaction:
                                foundlastaction = True
                                nextaction = round(clock + abilitydelay, 2)
                            foundlastGCD = True
                            nextgcd = round(clock + modGCDrecast, 2)
                        elif currentaction.name == 'AutoOGCD' or abilities[currentaction.id].abiltype == 'OGCD':
                            if not foundlastaction:
                                foundlastaction = True
                                nextaction = round(clock + abilitydelay, 2)
                        posinopen = posinopen - 1
                    stillinopener = False
        else:
            # GCD Priority List - Update this
            # First we check if we are dancing and finish the dance
            # We check the status on technical, If we used Saber first in our opener we also check to see if Saber Dance is up. Then we use Technical
            # Check if Standard Step is up - If so use it
            # next we check if 2 dances are coming and one is next GCD and if we have flourishfountain - Use Flourish Fountain
            # next we check if 2 dances are coming and one is next GCD and if we have flourishcascade - Use Flourish Cascade
            # If we have flourish fountain and we will lose a the proc next GCD - Use Fountainfall
            # If we have flourish cascade and we will lose a the proc next - Use Reverse Cascade
            # next we check if we are in combo and the combo is about to drop and we don't have Flourish Fountain - Use Fountain
            # If Cascade flourish is up and we will lose any flourish proc if we don't use one - Use Reverse Cascade
            # If Bladeshower flourish is up and we will lose any flourish proc if we don't use one - Use Bloodshower
            # If Windmill flourish up and we will lose any flourish proc if we don't use one - Use Rising Windmill
            # If we are in a buffwindow and esprit equal or greater than 50 - Use Devilment
            # If we are in a buffwindow and flourishfountain is up - Use Fountainfall
            # If we are in a buffwindow and flourishcascade is up - Use Reverse Cascade
            # If we are in a buff window and flourishbladeshower is up - Use Blood Shower
            # If we are in a buff window and flourishwindmill is up - Use Rising Windmill
            # If Esprit > 70 use Devilment
            # If flourishwindmill - Use Risingmill
            # if flourishbladeshower - Use Bloodshower
            # if flourishcascade - Use Reverse Cascade
            # if flourishfountain - Use Fountainfall
            # If we are in a combo use Fountain
            #  Else Use Cascade



            if nextgcd == clock:
                if standarddancing or technicaldancing:
                    if stepsneeded > 0:
                        if createlog:
                            logging.info(str(clock)+' : You use a Step')
                        stepsneeded = stepsneeded - 1
                        nextgcd = round(clock + 1, 2)
                    else:
                        if technicaldancing:
                            potency = potency + technicalfinish.getpotency(clock,False,False,CDHStats,potmod)
                            technicaldancing = False
                            technical.activate(clock)
                        else:
                            if trick.getactive(clock):
                                trickstands = trickstands + 1
                            potency = potency + standardfinish.getpotency(clock,False,False,CDHStats,potmod)
                            standarddancing = False
                        nextgcd = round(clock + 1.5, 2)
                        nextaction = round(clock + abilitydelay, 2)
                elif technicalstep.available(clock) and ((saberfirst and saber.getactive(clock)) or technicalfirst):
                    if createlog:
                        logging.info(str(clock)+' : You begin Technical Step')
                    ignoreabilitydelay = False
                    nextgcd = round(clock + 1.5, 2)
                    nextaction = round(clock + abilitydelay, 2)
                    techdrift = round(techdrift + clock - technicalstep.nextuse, 2)
                    technicalstep.putonCD(clock)
                    technicaldancing = True
                    stepsneeded = 4
                elif standardstep.available(clock) and technicalstep.nextuse > clock + 6.5:
                    if createlog:
                        logging.info(str(clock)+' : You begin Standard Step')
                    nextgcd = round(clock +1.5, 2)
                    standdrift = round(standdrift + clock - standardstep.nextuse, 2)
                    standardstep.putonCD(clock)
                    standarddancing = True
                    stepsneeded = 2
                else:
                    proccount = countprocs(clock)
                    procgcd = proccount * modGCDrecast
                    esprit = esprit + buildesprit(clock,esprit)
                    nextgcd = round(clock + modGCDrecast, 2)
                    nextaction = round(clock + abilitydelay, 2)
                    if (dancenumber >= 1 and flourishfountain.getactive(clock) and actualnextdance <= nextgcd) or (flourishfountain.getactive(clock) and nextdancetype == 'Technical' and actualnextdance <= nextgcd and flourishfountain.returnduration(clock) < modGCDrecast + 7):
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif (dancenumber >= 1 and flourishcascade.getactive(clock) and actualnextdance <= nextgcd) or (flourishcascade.getactive(clock) and nextdancetype == 'Technical' and actualnextdance <= nextgcd and flourishcascade.returnduration(clock) < modGCDrecast + 7):
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishfountain.getactive(clock) and flourishfountain.closetodrop(clock,  modGCDrecast):  # Check to see if Flourish Fountain is close to dropping
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishcascade.getactive(clock) and flourishcascade.closetodrop(clock, modGCDrecast):  # Check if Reverse Cascade is close to dropping
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif combo.getactive(clock) and not flourishfountain.getactive(clock) and combo.closetodrop(clock,modGCDrecast):  # First We check to see if we are in combo and don't have Flourished Fountain
                        potency = potency + fountain.getpotency(clock, True, True, CDHStats, potmod)
                        usedfountain = True
                        combo.dropbuff(clock)
                        gcd = gcd + 1
                        if checkproc():
                            flourishfountain.activate(clock)
                    elif flourishcascade.getactive(clock) and flourishcascade.closetodrop(clock, procgcd):  # Check if Bloodshower is close to fall
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishcascade.dropbuff(clock)
                    elif flourishbloodshower.getactive(clock) and flourishbloodshower.closetodrop(clock, procgcd):  # Check if Bloodshower is close to fall
                        potency = potency + bloodshower.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishwindmill.getactive(clock) and flourishwindmill.closetodrop(clock, procgcd):  # Check if Windmill is close to fall
                        potency = potency + risingwindmill.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif buffwindow and esprit >= 50 :  # I want to use devilment in the buff window
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                    elif buffwindow and flourishfountain.getactive(clock):  # Check to see if Flourish Fountain is up
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif buffwindow and flourishcascade.getactive(clock):  # Check if Reverse Cascade is up
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif buffwindow and flourishbloodshower.getactive(clock):  # Check if Bloodshower is up
                        potency = potency + bloodshower.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif buffwindow and flourishwindmill.getactive(clock):  # Check if Windmill is up
                        potency = potency + risingwindmill.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif (not foundnextbuffwindow and esprit > 80) or (foundnextbuffwindow and esprit == 100):
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                    elif flourishwindmill.getactive(clock):  # Check if Windmill is up
                        potency = potency + risingwindmill.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif flourishbloodshower.getactive(clock):  # Check if Bloodshower is up
                        potency = potency + bloodshower.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishcascade.getactive(clock):  # Check if Reverse Cascade is up
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishfountain.getactive(clock):  # Check to see if Flourish Fountain is up
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif combo.getactive(clock):  # If we are in combo we are doing fountain here
                        potency = potency + fountain.getpotency(clock, True, True, CDHStats, potmod)
                        gcd = gcd + 1
                        usedfountain = True
                        combo.dropbuff(clock)
                        if checkproc():
                            flourishfountain.activate(clock)
                    else:  # If all else fails we go into Cascade combo
                        potency = potency + cascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        combo.activate(clock)
                        if checkproc():
                            flourishcascade.activate(clock)
            elif nextaction == clock:
                # oGCD Priority list
                # Ignore oGCDs if dancing
                # If saber dance is ready, and technical is the next GCD or we opened with Technical first and we are in the second oGCD slot - Use Saber
                # If Saber is ready and technical is the next GCD or we opened with Technical first and our next GCD is greater than 1.5 away, close the ogcd slot to ensure saber gets second slot
                # if saber dance is ready, our opener used Saber First and technicalstep is the next gcd and nextgcd is 1.7 away, wait. To ensure second oGCD slot
                # if flourish is available, we have 0 flourish procs, and technical dance isn't less than 4* our Current GCD seconds away and we aren't dancing twice in the next 15, and we aren't in a buff window with 50 or more Esprit - use flourish
                # if our potion is ready and the next saber dance is less than 15 seconds away - use potion
                # if we have a flourished fan and are double dancing in the next 15 seconds or flourish is up, use Fan Dance III
                # if we have a flourished fan and the fan is close to dropping, use Fan Dance III
                # If we have a flourished fan and the next buff window is more than 13.5 seconds away, use Fan Dance III
                # if we have a flourished fan and we have 4 feathers, use Fan Dance III
                # If we are in a buffwindow and have a flourished fan, use Fan Dance III
                # If we are in a buffwindow and have feathers use Fan Dance I
                # IF we have 4 feathers and some other flourish proc - Use Fan Dance I
                abilityused = False

                if technicaldancing or standarddancing:
                    abilityused = False
                elif saberdance.available(clock) and (technicalstep.nextuse <= nextgcd or technicalfirst) and round(nextgcd - abilitydelay, 2) >= clock:
                    if createlog:
                        logging.info(str(clock)+ " : You use Saber Dance!")
                    saber.activate(clock)
                    saberdance.putonCD(clock)
                    abilityused = True
                    ignoreabilitydelay = True
                    nextaction = technicalstep.nextuse
                elif saberdance.available(clock) and (technicalstep.nextuse <= nextgcd or technicalfirst) and (round(nextgcd - 1.5 ,2) < clock or not technicalstep.nextuse == nextgcd): #Wait for Second oGCD window for Saber dance
                    abilityused = False
                elif flourish.available(clock) and (countprocs(clock) == 0) and not (flourishfan.getactive(clock)) and not (nextdancetype == 'Technical' and round(nextgcd + (modGCDrecast*4), 2) > nextdance) and dancenumber < 2 and not(buffwindow and esprit >= 50):
                    if createlog:
                        logging.info(str(clock)+ ' : You use Flourish!')
                    flourishcascade.activate(clock)
                    flourishbloodshower.activate(clock)
                    flourishwindmill.activate(clock)
                    flourishfountain.activate(clock)
                    flourishfan.activate(clock)
                    flourish.putonCD(clock)
                    abilityused = True
                elif potion.available(clock) and (nextgcd - nextaction) > 1.5 and (saberdance.getrecast(clock) < 15) and potionbuff.available :
                    if createlog:
                        logging.info(str(clock)+' : You use a potion!')
                    potionbuff.activate(clock)
                    potion.putonCD(clock)
                    nextaction = round(clock + .7,2)
                    abilityused = True
                elif flourishfan.getactive(clock)and fandance3.available(clock) and (dancenumber > 1 or flourish.available(clock)): # Use it right away so we don't risk losing proc
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif flourishfan.getactive(clock) and fandance3.available(clock) and flourishfan.closetodrop(clock , modGCDrecast): # Use it if it drops in a GCD
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif flourishfan.getactive(clock) and fandance3.available(clock) and nextbuffwindow > 13.5: # Use it if there isn't a buff window coming
                    potency = potency + fandance3.getpotency(clock,False,False,CDHStats,potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif flourishfan.getactive(clock) and feathers > 3: # Use it if we have 4 feathers
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif buffwindow and flourishfan.getactive(clock):
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif buffwindow and feathers > 0 and fandance1.available(clock):
                    potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                    feathersused = feathersused + 1
                    feathers = feathers - 1
                    abilityused = True
                    if checkproc():
                        flourishfan.activate(clock)
                elif feathers > 3 and not (flourishfan.getactive(clock)) and fandance1.available(clock):
                    potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                    feathersused = feathersused + 1
                    feathers = feathers - 1
                    abilityused = True
                    if checkproc():
                        flourishfan.activate(clock)
               # elif feathers == 4 and fandance1.available(clock):
                #    potency = potency + fandance1.getpotency(clock, False, False, CDHStats, potmod)
                 #   feathersused = feathersused + 1
                  #  feathers = feathers - 1
                   # abilityused = True
                    #if checkproc():
                     #   flourishfan.activate(clock)
                if abilityused: #Process new action time
                    if not ignoreabilitydelay:
                        nextaction = round(clock + abilitydelay, 2)
                        if nextaction + abilitydelay > nextgcd and not saberdance.available(nextgcd):
                            nextaction = round(nextgcd, 2) #I want to avoid clipping
                else:
                    if not ignoreabilitydelay:
                        nextaction = round(clock + .01, 2)
                        if nextaction + abilitydelay > nextgcd and not saberdance.available(nextgcd):
                            nextaction = round(nextgcd, 2) #I want to avoid clipping

            if technicalstep.nextuse < round(clock + modGCDrecast,2) and not round(technicalstep.nextuse, 2) == nextgcd and not standarddancing and technicalhold:
                #print(str(clock)+' : Time Lost Technical: ' + str(round(technicalstep.nextuse - nextgcd,2)))
                techhold = round(techhold + (technicalstep.nextuse - nextgcd), 2)
                nextgcd = round(technicalstep.nextuse, 2)

            elif standardstep.nextuse < round(clock+(modGCDrecast),2) and (technicalstep.nextuse - clock) > (6.5 + modGCDrecast) and not technicaldancing and not round(standardstep.nextuse, 2) == nextgcd and standardhold:
                #print(str(clock)+' :Time Lost Standard: ' + str(round(standardstep.nextuse - nextgcd,2)))
                standhold = round(standhold + (standardstep.nextuse - nextgcd), 2)
                nextgcd = round(standardstep.nextuse, 2)

        potency = round(potency,3)
        if (oldpot != potency) or (oldesprit != esprit) or (oldfeathers != feathers):
            if createlog:
                logging.info(str(clock)+ ' : Potency: '+str(potency)+' || Dex: '+str(dex)+' || Feathers: '+str(feathers)+' || Esprit: '+str(esprit)+ ' || Buff window: '+str(buffwindow)+' '+str(potmod)+ ' || Crit Rate: '+str(CDHStats[0])+ ' || DH Rate: '+str(CDHStats[2]))
            oldpot = potency
            oldesprit = esprit
            oldfeathers = feathers
        clock = round(clock + .01, 2)

    print(gcd)
    if createlog:
        logging.info("------Results-----")
        logging.info("Time Ran : "+str(clock))
        logging.info("Potency : "+str(potency))
        logging.info("Potency per Second : "+str(potency/clock))
        logging.info("Feathers Remaining: "+str(feathers))
        logging.info("Esprit Remaining: "+str(esprit))
        logging.info("GCDs Used: "+str(gcd))
        logging.info("Feathers used: "+str(feathersused))
        logging.info("Flourished Fans: "+str(flourishedfans))
        logging.info("Devilments Used: "+str(useddevilments))

        global comboscreated
        global totalprocs
        global featherattempt
        global feathersdropped
        global espritcap
        global espritattempt
        global espritattemptparty

        logging.info('Combos Made: '+str(comboscreated))
        logging.info('Combos Dropped: ' + str(combodrops))
        logging.info('Percent Drop : ' + str(combodrops/comboscreated))
        logging.info('Flourish Procs Generated : ' + str(totalprocs))
        logging.info('Flourish Procs Dropped : ' + str(procdrop))
        logging.info('Percent Drop : ' + str(procdrop / totalprocs))
        logging.info('Feathers Attempt: ' + str(featherattempt))
        logging.info('Feathers Dropped : ' + str(feathersdropped))
        logging.info('Percent Drop : ' + str(feathersdropped / featherattempt))
        logging.info('Esprit Attempt: ' + str(espritattemptparty+espritattempt))
        logging.info('Esprit Cap : ' + str(espritcap))
        logging.info('Percent Drop : ' + str(espritcap / (espritattemptparty+espritattempt)))

    dex = basedex
    return potency

def simholds(openset, timetorun, delaytable):
    reset()
    global GCDrecast
    global abilitydelay
    global basecritchance
    global basecritbonus
    global basedirectchance
    global basedirectbonus
    global dex
    global party
    global espritfromparty
    global espritfromself
    global combodrops
    global procdrop
    global techdrift
    global standdrift
    global standhold
    global techhold
    global trickstands

    basedex = dex
    clock = 0
    timerfinish = timetorun
    partygcd = GCDrecast
    potency = 0
    modGCDrecast = GCDrecast
    critchance = basecritchance
    critbonus = basecritbonus
    directchance = basedirectchance
    directbonus = basedirectbonus
    delayedpos = 0
    delayeddance =0
    delay = False
    delaystart = 0
    delayend = 0
    buffdelay = 0

    buffwindow = True
    buffwindowend = 0
    makebuffsavailable()
    opener = buildopentable(openset)
    stillinopener = True
    posinopen = 0
    lastbuffwindow = 0

    nextgcd = 0
    nextaction = 0
    nexttick = 0
    standarddancing = False
    technicaldancing = False
    stepsneeded = 0
    nextpartygcd = .7
    esprit = 0
    feathers = 0
    saberfirst = False
    technicalfirst = False
    ignoreabilitydelay = False
    technicalhold = False
    standardhold = False

    technicalholdlist=[2.50,2.49,2.48,2.44,2.43,2.38]
    standardholdlist = [2.5,2.49,2.48]

    for i in technicalholdlist:
        if i == GCDrecast:
            technicalhold = True

    for i in standardholdlist:
        if i == GCDrecast:
            standardhold = True

    partnerloc = 0
    partyindex = 0

# Auto Information
    nextauto = 1

# AST Stuff
#clock,currentseals,allseals,nextaction,sleevestacks,nextgcd,card,cardheld,arcana,astopen,astopener,inastopen
    astinformation = [[], False, 0, 0, 0, justdraw([],False,0), True, False, True, buildasttable(), 0, astpriority,delaytable,delayedpos]

# Values to keep track and help print updates

    oldpot = 0
    oldfeathers = 0
    oldesprit = 0
    gcd = 0
    feathersused = 0
    flourishedfans = 0
    useddevilments = 0

    fandance1.nextuse = 1
    fandance3.nextuse = 1


    while clock < timerfinish:

        if delayedpos < len(delaytable):
            delaystart = round(delaytable[delayedpos][0], 2)
            delayend = round(delaytable[delayedpos][1], 2)
            buffdelay = delaytable[delayedpos][2]
            if clock == delaystart:
                nextgcd = round(delayend, 2)
                nextaction = round(delayend, 2)
                delayeddance = round(delayend-14,2)
                delay = True
                stillinopener = False # To avoid complications)
                if technicalstep.nextuse < delayend:
                    technicalstep.nextuse = round(delayend+1.5+GCDrecast*2,2)
                if saberdance.nextuse < delayend:
                    saberdance.nextuse = round(delayend+GCDrecast,2)
            elif clock == delayend:
                if improvbuff.getactive(clock):
                    improvbuff.dropbuff(clock)
                delay = False
                delayedpos = delayedpos + 1
        else:
            delaystart = 1000000000000
            delayend = 1000000000000

        totalbuffs = 0

        potmod = [1.20, 1.05]
        dex = basedex
        modGCDrecast = GCDrecast
        critchance = basecritchance
        critbonus = basecritbonus
        directchance = basedirectchance
        directbonus = basedirectbonus
        postcombo = combo.getactive(clock)
        usedfountain = False

        if potionbuff.available:
            if potionbuff.ready and potionbuff.activation == clock:
                potionbuff.switchon(clock)
            if potionbuff.getactive(clock):
                if dex * potionbuff.potency > 225:
                    dex = dex + 225
                else:
                    dex = dex + (dex*potionbuff.potency)
            elif potionbuff.active:
                potionbuff.dropbuff(clock)
                dex = basedex

        if ast.active:
            astinformation = astmodule(clock,astinformation)
            for i in astbuffs:
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if i.getactive(clock):
                    potmod.append(i.getpotency(clock))
                elif not i.getactive(clock) and i.active:
                    i.dropbuff(clock)

        for i in potencybuffs:
            if i.available:
                if delayedpos < len(delaytable):
                    if i.starttime + (i.duration-2) > delaystart or (delay and i.starttime < delayend) and i.starttime <= delayend+i.default:
                        if buffdelay:
                            i.starttime = round(delayend+i.default,2)
                        else:
                            i.starttime = round(delayend + 1, 2)
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if not i.ready and i.starttime == clock:
                    i.activate(clock)
                if i.getactive(clock):
                    potmod.append(i.getpotency(clock))
                    totalbuffs = totalbuffs + 1
                elif i.available and not i.getactive(clock) and i.active:
                    i.dropbuff(clock)
        for i in dhbuffs:
            if i.available:
                if delayedpos < len(delaytable):
                    if i.starttime + (i.duration-2) > delaystart or (delay and i.starttime < delayend) and i.starttime <= delayend+i.default:
                        if buffdelay:
                            i.starttime = round(delayend+i.default,2)
                        else:
                            i.starttime = round(delayend + 1, 2)
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if not i.ready and i.starttime == clock:
                    i.activate(clock)
                if i.getactive(clock):
                    directchance = round(directchance + i.getpotency(clock), 2)
                    totalbuffs = totalbuffs + 1
                elif i.available and not i.getactive(clock) and i.active:
                    i.dropbuff(clock)
        for i in critbuffs:
            if i.available:
                if delayedpos < len(delaytable):
                    if i.starttime + (i.duration-2) > delaystart or (delay and i.starttime < delayend) and i.starttime <= delayend+i.default:
                        if buffdelay:
                            i.starttime = round(delayend+i.default,2)
                        else:
                            i.starttime = round(delayend + 1, 2)
                if i.ready and i.activation == clock:
                    i.switchon(clock)
                if not i.ready and i.starttime == clock:
                    i.activate(clock)
                if i.getactive(clock):
                    critchance = round(critchance + i.getpotency(clock), 2)
                    totalbuffs = totalbuffs + 1
                elif i.available and not i.getactive(clock) and i.active:
                    i.dropbuff(clock)
        for i in buffs:
            if i.ready and i.activation == clock:
                i.switchon(clock)

        if technical.getactive(clock):
            potmod.append(1.05)
            totalbuffs = totalbuffs + 1
        elif technical.active:
            technical.dropbuff(clock)

        if saber.getactive(clock):
            critchance = round(critchance + saber.getpotency(clock), 2)
            directchance = round(directchance + saber.getpotency(clock), 2)
            totalbuffs = totalbuffs + 1
        elif saber.active:
            saber.dropbuff(clock)

        for i in buffs:
            if i.active and (not i.getactive(clock)):
                if not i.name == 'Combo':
                    if createlog:
                        procdrop = procdrop + 1
                        logging.info(str(clock)+' : You lost the proc '+ i.name)
                else:
                    combodrops = combodrops + 1
                    if createlog:
                        logging.info(str(clock) + ' : You lost a combo')
                i.dropbuff(clock)


        if nin.active and trick.getactive(clock):
            buffwindow = True
            lastbuffwindow = clock
        elif saber.getactive(clock):
            buffwindow = True
            lastbuffwindow = clock
        elif drg.active and brd.active and battlevoice.getactive(clock) and litany.getactive(clock):
            buffwindow = True
            lastbuffwindow = clock
        else:
            buffwindow = False

        # Let's Jump through time to figure out our next buff window
        foundnextbuffwindow = False
        nextbuffwindow = clock
        nextdance = clock
        nextdancetype = 'None'
        dancenumber = 0
        standardtimer = 0
        technicaltimer = 0
        actualnextdance = 0 #Because I don't want to change the code, Next dance is sometimes a lie!!!

        standardrecast = round(standardstep.getrecast(clock),2)
        technicalrecast = round(technicalstep.getrecast(clock),2)
        if standardrecast - 15 <= 0:
            nextdancetype = 'Standard'
            nextdance = round(clock + standardrecast, 2)
            dancenumber = dancenumber + 1
            standardtimer = round(clock + standardrecast, 2)
        if technicalrecast - 15 <= 0:
            nextdancetype = 'Technical'
            nextdance = round(clock + technicalrecast, 2)
            dancenumber = dancenumber + 1
            technicaltimer = round(clock + standardrecast, 2)
        ## Lots of fun dancing logic used to figure out if I'm dancing soon or not and what dances are coming and when technical is coming
        # Could consolidate this to less code if ever needed, some redundancy here
        if technicaltimer == 0:
            standardtimer = actualnextdance
        elif standardtimer == 0:
            technicaltimer = actualnextdance
        elif technicaltimer > standardtimer:
            standardtimer = actualnextdance
        else:
            technicaltimer = actualnextdance

        if (nextgcd == clock or (nextaction == clock and (flourishfan.getactive(clock)))) and clock - lastbuffwindow > 30 :
            while(not foundnextbuffwindow):
                nextbuffwindow = round(nextbuffwindow + .01, 2)
                if nin.active and trick.starttime == nextbuffwindow:
                    foundnextbuffwindow = True
                elif saber.starttime == nextbuffwindow:
                    foundnextbuffwindow = True
                elif drg and brd and battlevoice.starttime == nextbuffwindow:
                    foundnextbuffwindow = True
                elif nextbuffwindow > (clock + 15): # I don't really care if the buffwindow is greater than 20s away
                    foundnextbuffwindow = True

        CDHStats = [critchance, critbonus, directchance, directbonus]
        # Handle Esprit

        for i in party:
            if i.nextgcd == clock:
                i.nextgcd = round(clock + i.gcd, 2)
                if technical.getactive(clock) and not delay:
                    esprit = esprit + partybuildesprit(clock,esprit,i.espritrate)
                elif i.partner and not delay:
                    esprit = esprit + partybuildesprit(clock, esprit, i.espritrate)
        # Handle Auto
        if clock == nextauto:
            if not delay:
                potency = potency + autoattack.getpotency(clock,False,False,CDHStats,potmod)
            nextauto = round(clock + autoattack.cooldown,2)

        if clock == nexttick:
            if improvbuff.getactive(clock):
                esprit = esprit + len(party)*3
                if esprit > 100:
                    esprit = 100
                    improvbuff.dropbuff(clock)
            nexttick = round(clock + 3, 2)

        #Handle Delay Actions

        if delay:

            if (delayeddance - clock > 10 or (standardstep.nextuse > delayend and technicalstep.nextuse > delayend)) and improv.available(clock) and not improvbuff.getactive(clock) and not technicaldancing and not standarddancing and esprit < 60 :
                if createlog:
                    logging.info(str(clock)+ ' : You begin Improvisation')
                improv.putonCD(clock)
                improvbuff.activate(clock)
            elif standardstep.available(clock) and clock >= delayeddance and not technicaldancing and not standarddancing:
                if createlog:
                    logging.info(str(clock) + ' : You begin Standard Step')
                nextgcd = round(clock + 1.5, 2)
                standardstep.putonCD(clock)
                standarddancing = True
                stepsneeded = 2

        elif not delay and improvbuff.getactive(clock):
            improvbuff.dropbuff(clock)

        # Let's push the next GCD to technical or standard if its within range
        #Handle Opener if available

        if stillinopener:
            if opener[posinopen].actionable(clock):
                currentaction = opener[posinopen]
                if abilities[currentaction.id].name == 'Technical Finish':
                    potency = potency + technicalfinish.getpotency(clock, False, False, CDHStats, potmod)
                    technical.activate(clock)
                    nextgcd = round(clock + 1.5,2)
                elif abilities[currentaction.id].name == 'Standard Finish':
                    potency = potency + standardfinish.getpotency(clock,False,False,CDHStats,potmod)
                    nextgcd = round(clock + 1.5,2)
                elif abilities[currentaction.id].name == 'Saber Dance':
                    if createlog:
                        logging.info(str(clock)+' : You use Saber Dance!')
                    if not technicalfirst:
                        saberfirst = True
                    saber.activate(clock)
                    abilities[currentaction.id].putonCD(clock)
                elif abilities[currentaction.id].name == 'Flourish':
                    if createlog:
                        logging.info(str(clock)+' : You use Flourish!')
                    flourishcascade.activate(clock)
                    flourishwindmill.activate(clock)
                    flourishfountain.activate(clock)
                    flourishbloodshower.activate(clock)
                    flourishfan.activate(clock)
                    abilities[currentaction.id].putonCD(clock)
                elif currentaction.name == 'Potion':
                    if createlog:
                        logging.info(str(clock)+' : You use a Potion!')
                    potion.putonCD(clock)
                    potionbuff.activate(clock)
                elif currentaction.name == 'ReverseProc' and flourishcascade.getactive(clock):
                    potency = potency + reversecascade.getpotency(clock,False,False,CDHStats, potmod)
                    gcd = gcd + 1
                    flourishcascade.dropbuff(clock)
                    feathers = feathers + getfeathers(clock,feathers)
                    esprit = esprit + buildesprit(clock,esprit)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'AutoGCD' or currentaction.name =='ReverseProc':
                    #Auto GCD in the opener
                    # If technical is active and Esprit > 80 - Use Devilment
                    # If we are to lose any procs do them in the following order Fountfall > Cascade > bloodshower > windmill
                    # If we are in a buffwindo and esprit is great than or equal to 50 then use Devilment
                    # If we are in a combo and flourishfountain is not active and our combo will drop - Use Fountain
                    # Use Flourishes in this order : Fountainfall >  Reverse Cascade > Blood > Rising
                    # If esprit is 90 or above use Devilment
                    # If combo use Fountain
                    # Else use Cascade
                    proccount = countprocs(clock)
                    procgcd = proccount * modGCDrecast
                    nextgcd = round(clock + modGCDrecast, 2)
                    if technical.getactive(clock) and esprit > 80 : #If we Technical is out and we have 90+ Esprit, Go now
                        potency = potency + devilment.getpotency(clock,False,False,CDHStats,potmod)
                        useddevilments = useddevilments + 1
                        esprit = esprit - devilment.cost
                        gcd = gcd + 1
                    elif flourishfountain.getactive(clock) and flourishfountain.closetodrop(clock, procgcd): #Check to see if Flourish Fountain is close to dropping
                        potency = potency + fountainfall.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishcascade.getactive(clock) and flourishcascade.closetodrop(clock, procgcd): #Check if Reverse Cascade is close to dropping
                        potency = potency + reversecascade.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishbloodshower.getactive(clock) and flourishbloodshower.closetodrop(clock, procgcd): #Check if Bloodshower is close to fall
                        potency = potency + bloodshower.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishwindmill.getactive(clock) and flourishwindmill.closetodrop(clock, procgcd): # Check if Windmill is close to fall
                        potency = potency + risingwindmill.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif buffwindow and esprit >= 50:   # I want to use devilment in the buff window
                        potency = potency + devilment.getpotency(clock,False,False,CDHStats,potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                    elif combo.getactive(clock) and not flourishfountain.getactive(clock) and combo.closetodrop(clock,modGCDrecast): #First We check to see if we are in combo and don't have Flourished Fountain
                        potency = potency + fountain.getpotency(clock, True, True, CDHStats, potmod)
                        combo.dropbuff(clock)
                        usedfountain = True
                        gcd = gcd + 1
                        if checkproc():
                            flourishfountain.activate(clock)
                    elif flourishfountain.getactive(clock):  # Check to see if Flourish Fountain is up
                        potency = potency + fountainfall.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishcascade.getactive(clock):  # Check if Reverse Cascade is up
                        potency = potency + reversecascade.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishbloodshower.getactive(clock):  # Check if Bloodshower is up
                        potency = potency + bloodshower.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishwindmill.getactive(clock):  # Check if Windmill is up
                        potency = potency + risingwindmill.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif esprit > 80:
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                    elif combo.getactive(clock): # If we are in combo we are doing fountain here
                        potency = potency + fountain.getpotency(clock,True,True,CDHStats,potmod)
                        gcd = gcd + 1
                        usedfountain = True
                        combo.dropbuff(clock)
                        if checkproc():
                            flourishfountain.activate(clock)
                    else:  # If all else fails we go into Cascade combo
                        potency = potency + cascade.getpotency(clock,False,False,CDHStats,potmod)
                        gcd = gcd + 1
                        combo.activate(clock)
                        if checkproc():
                            flourishcascade.activate(clock)
                    esprit = esprit + buildesprit(clock,esprit) #Check if we get Esprit from this GCD
                elif currentaction.name == 'AutoOGCD':
                # AutoOGCD in the opener
                # If flourish is up, we have no procs - Use it
                # If flourish fan is up use FD3
                # if we are in the buffwindow and have feathers and can use FD1 use FD1
                #If we have 4 feathers and FD1 is up use FD1
                #push the oGCD further if we have more feathers. at a 2.4 gcd we can get two in
                    if flourish.available(clock) and countprocs(clock) == 0 and not flourishfan.getactive(clock):
                        if createlog:
                            logging.info(str(clock) + ' : You use Flourish!')
                        flourishcascade.activate(clock)
                        flourishwindmill.activate(clock)
                        flourishfountain.activate(clock)
                        flourishbloodshower.activate(clock)
                        flourishfan.activate(clock)
                        flourish.putonCD(clock)
                    elif flourishfan.getactive(clock) and fandance3.available(clock):
                        potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                        flourishedfans = flourishedfans + 1
                        flourishfan.dropbuff(clock)
                    elif buffwindow and feathers > 0 and fandance1.available(clock):
                        potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                        feathers = feathers - 1
                        feathersused = feathersused + 1
                        if checkproc():
                            flourishfan.activate(clock)
                    elif feathers > 3 and fandance1.available(clock):
                        potency = potency + fandance1.getpotency(clock,False,False,CDHStats, potmod)
                        feathersused = feathersused + 1
                        feathers = feathers - 1
                        if checkproc():
                            flourishfan.activate(clock)
                    elif currentaction.actiontime + .7 < nextgcd and feathers > 0:
                        currentaction.actiontime = round(clock + .01, 2)
                        posinopen = posinopen - 1
                elif currentaction.name == 'Hold':
                    if createlog:
                        logging.info(str(clock)+' : Waiting')
                elif currentaction.name == 'Technical Step':
                    if createlog:
                        logging.info(str(clock)+' : You begin Technical Step')
                    if not saberfirst:
                        technicalfirst = True
                    abilities[currentaction.id].putonCD(clock)
                elif currentaction.name == 'Standard Step':
                    if createlog:
                        logging.info(str(clock)+' : You begin Standard Step')
                    abilities[currentaction.id].putonCD(clock)
                elif currentaction.name == 'Fountain':
                    potency = potency + fountain.getpotency(clock,True,True,CDHStats,potmod)
                    gcd = gcd + 1
                    usedfountain = True
                    combo.dropbuff(clock)
                    if checkproc():
                        flourishfountain.activate(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                elif currentaction.name == 'Cascade':
                    potency = potency + cascade.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    combo.activate(clock)
                    if checkproc():
                        flourishcascade.activate(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                elif currentaction.name == 'Fan Dance I':
                    if feathers > 0:
                        potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                        feathersused = feathersused + 1
                        feathers = feathers - 1
                    if checkproc():
                        flourishfountain.activate(clock)
                elif currentaction.name == 'Fan Dance III':
                    if flourishfan.getactive(clock):
                        potency = potency + fandance3.getpotency(clock,False,False,CDHStats,potmod)
                        flourishedfans = flourishedfans + 1
                        flourishfan.dropbuff(clock)
                elif currentaction.name == 'Fountainfall':
                    potency = potency + fountainfall.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    flourishfountain.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'Reverse Cascade':
                    potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                    gcd = gcd + 1
                    flourishcascade.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'Bloodshower':
                    potency = potency + bloodshower.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    flourishbloodshower.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                elif currentaction.name == 'Rising Windmill':
                    potency = potency + risingwindmill.getpotency(clock,False,False,CDHStats,potmod)
                    gcd = gcd + 1
                    flourishwindmill.dropbuff(clock)
                    esprit = esprit + buildesprit(clock,esprit)
                    feathers = feathers + getfeathers(clock,feathers)
                    nextgcd = round(clock + modGCDrecast, 2)
                posinopen = posinopen + 1
                if posinopen >= len(opener):
                    if createlog:
                        logging.info('Finished with Opener, commencing Sim')
                    #Let's figure out when our last GCD was
                    foundlastGCD = False
                    foundlastaction = False
                    while(not foundlastGCD):
                        currentaction = opener[posinopen-1]
                        if currentaction.name.split()[0] == 'Technical' or currentaction.name.split()[0] == 'Standard':
                            if not foundlastaction:
                                foundlastaction = True
                                nextaction = round(clock + abilitydelay, 2)
                            if currentaction.name.split()[1] == 'Finish':
                                foundlastGCD = True
                                nextgcd = round(clock + 1.5, 2)
                        elif currentaction.name == 'AutoGCD' or abilities[currentaction.id].abiltype == 'GCD':
                            if not foundlastaction:
                                foundlastaction = True
                                nextaction = round(clock + abilitydelay, 2)
                            foundlastGCD = True
                            nextgcd = round(clock + modGCDrecast, 2)
                        elif currentaction.name == 'AutoOGCD' or abilities[currentaction.id].abiltype == 'OGCD':
                            if not foundlastaction:
                                foundlastaction = True
                                nextaction = round(clock + abilitydelay, 2)
                        posinopen = posinopen - 1
                    stillinopener = False
        else:
            # GCD Priority List - Update this
            # First we check if we are dancing and finish the dance
            # We check the status on technical, If we used Saber first in our opener we also check to see if Saber Dance is up. Then we use Technical
            # Check if Standard Step is up - If so use it
            # next we check if 2 dances are coming and one is next GCD and if we have flourishfountain - Use Flourish Fountain
            # next we check if 2 dances are coming and one is next GCD and if we have flourishcascade - Use Flourish Cascade
            # If we have flourish fountain and we will lose a the proc next GCD - Use Fountainfall
            # If we have flourish cascade and we will lose a the proc next - Use Reverse Cascade
            # next we check if we are in combo and the combo is about to drop and we don't have Flourish Fountain - Use Fountain
            # If Cascade flourish is up and we will lose any flourish proc if we don't use one - Use Reverse Cascade
            # If Bladeshower flourish is up and we will lose any flourish proc if we don't use one - Use Bloodshower
            # If Windmill flourish up and we will lose any flourish proc if we don't use one - Use Rising Windmill
            # If we are in a buffwindow and esprit equal or greater than 50 - Use Devilment
            # If we are in a buffwindow and flourishfountain is up - Use Fountainfall
            # If we are in a buffwindow and flourishcascade is up - Use Reverse Cascade
            # If we are in a buff window and flourishbladeshower is up - Use Blood Shower
            # If we are in a buff window and flourishwindmill is up - Use Rising Windmill
            # If Esprit > 70 use Devilment
            # If flourishwindmill - Use Risingmill
            # if flourishbladeshower - Use Bloodshower
            # if flourishcascade - Use Reverse Cascade
            # if flourishfountain - Use Fountainfall
            # If we are in a combo use Fountain
            #  Else Use Cascade



            if nextgcd == clock:
                if standarddancing or technicaldancing:
                    if stepsneeded > 0:
                        if createlog:
                            logging.info(str(clock)+' : You use a Step')
                        stepsneeded = stepsneeded - 1
                        nextgcd = round(clock + 1, 2)
                    elif not delay:
                        if technicaldancing:
                            potency = potency + technicalfinish.getpotency(clock,False,False,CDHStats,potmod)
                            technicaldancing = False
                            technical.activate(clock)
                        else:
                            if trick.getactive(clock):
                                trickstands = trickstands + 1
                            potency = potency + standardfinish.getpotency(clock,False,False,CDHStats,potmod)
                            standarddancing = False
                        nextgcd = round(clock + 1.5, 2)
                        nextaction = round(clock + abilitydelay, 2)
                    else:
                        if delayend - clock > 1.5:
                            nextgcd = delayend
                            nextaction = delayend
                        else:
                            nextgcd = round(clock + 1.5, 2)
                            nextaction = round(clock + 1.5, 2)
                elif technicalstep.available(clock) and ((saberfirst and saber.getactive(clock)) or technicalfirst) and delaystart - clock > 22:
                    if createlog:
                        logging.info(str(clock)+' : You begin Technical Step')
                    ignoreabilitydelay = False
                    nextgcd = round(clock + 1.5, 2)
                    nextaction = round(clock + abilitydelay, 2)
                    techdrift = round(techdrift + clock - technicalstep.nextuse, 2)
                    technicalstep.putonCD(clock)
                    technicaldancing = True
                    stepsneeded = 4
                elif standardstep.available(clock) and technicalstep.nextuse > clock + 6.5 and delaystart - clock > 5:
                    if createlog:
                        logging.info(str(clock)+' : You begin Standard Step')
                    nextgcd = round(clock +1.5, 2)
                    standdrift = round(standdrift + clock - standardstep.nextuse, 2)
                    standardstep.putonCD(clock)
                    standarddancing = True
                    stepsneeded = 2
                else:
                    proccount = countprocs(clock)
                    procgcd = proccount * modGCDrecast
                    esprit = esprit + buildesprit(clock,esprit)
                    nextgcd = round(clock + modGCDrecast, 2)
                    nextaction = round(clock + abilitydelay, 2)
                    if esprit > 40 and delayend - delaystart > 20 and delaystart < clock + modGCDrecast and improv.available(clock):
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                        esprit = esprit + buildesprit(clock,esprit)
                    elif (dancenumber >= 1 and flourishfountain.getactive(clock) and actualnextdance <= nextgcd) or (flourishfountain.getactive(clock) and nextdancetype == 'Technical' and actualnextdance <= nextgcd and flourishfountain.returnduration(clock) < modGCDrecast + 7):
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif (dancenumber >= 1 and flourishcascade.getactive(clock) and actualnextdance <= nextgcd) or (flourishcascade.getactive(clock) and nextdancetype == 'Technical' and actualnextdance <= nextgcd and flourishcascade.returnduration(clock) < modGCDrecast + 7):
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishfountain.getactive(clock) and flourishfountain.closetodrop(clock,  modGCDrecast):  # Check to see if Flourish Fountain is close to dropping
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishcascade.getactive(clock) and flourishcascade.closetodrop(clock, modGCDrecast):  # Check if Reverse Cascade is close to dropping
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif combo.getactive(clock) and not flourishfountain.getactive(clock) and combo.closetodrop(clock,modGCDrecast):  # First We check to see if we are in combo and don't have Flourished Fountain
                        potency = potency + fountain.getpotency(clock, True, True, CDHStats, potmod)
                        usedfountain = True
                        combo.dropbuff(clock)
                        gcd = gcd + 1
                        if checkproc():
                            flourishfountain.activate(clock)
                    elif flourishcascade.getactive(clock) and flourishcascade.closetodrop(clock, procgcd):  # Check if Bloodshower is close to fall
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishcascade.dropbuff(clock)
                    elif flourishbloodshower.getactive(clock) and flourishbloodshower.closetodrop(clock, procgcd):  # Check if Bloodshower is close to fall
                        potency = potency + bloodshower.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishwindmill.getactive(clock) and flourishwindmill.closetodrop(clock, procgcd):  # Check if Windmill is close to fall
                        potency = potency + risingwindmill.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif buffwindow and esprit >= 50 :  # I want to use devilment in the buff window
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                        esprit = esprit + buildesprit(clock, esprit)
                    elif buffwindow and flourishfountain.getactive(clock):  # Check to see if Flourish Fountain is up
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif buffwindow and flourishcascade.getactive(clock):  # Check if Reverse Cascade is up
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif buffwindow and flourishbloodshower.getactive(clock):  # Check if Bloodshower is up
                        potency = potency + bloodshower.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif buffwindow and flourishwindmill.getactive(clock):  # Check if Windmill is up
                        potency = potency + risingwindmill.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif (not foundnextbuffwindow and esprit > 80) or (foundnextbuffwindow and esprit == 100) :
                        potency = potency + devilment.getpotency(clock, False, False, CDHStats, potmod)
                        useddevilments = useddevilments + 1
                        gcd = gcd + 1
                        esprit = esprit - devilment.cost
                        esprit = esprit + buildesprit(clock, esprit)
                    elif flourishwindmill.getactive(clock):  # Check if Windmill is up
                        potency = potency + risingwindmill.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishwindmill.dropbuff(clock)
                    elif flourishbloodshower.getactive(clock):  # Check if Bloodshower is up
                        potency = potency + bloodshower.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        feathers = feathers + getfeathers(clock, feathers)
                        flourishbloodshower.dropbuff(clock)
                    elif flourishcascade.getactive(clock):  # Check if Reverse Cascade is up
                        potency = potency + reversecascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishcascade.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif flourishfountain.getactive(clock):  # Check to see if Flourish Fountain is up
                        potency = potency + fountainfall.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        flourishfountain.dropbuff(clock)
                        feathers = feathers + getfeathers(clock, feathers)
                    elif combo.getactive(clock):  # If we are in combo we are doing fountain here
                        potency = potency + fountain.getpotency(clock, True, True, CDHStats, potmod)
                        gcd = gcd + 1
                        usedfountain = True
                        combo.dropbuff(clock)
                        if checkproc():
                            flourishfountain.activate(clock)
                    else:  # If all else fails we go into Cascade combo
                        potency = potency + cascade.getpotency(clock, False, False, CDHStats, potmod)
                        gcd = gcd + 1
                        combo.activate(clock)
                        if checkproc():
                            flourishcascade.activate(clock)
            elif nextaction == clock:
                # oGCD Priority list
                # Ignore oGCDs if dancing
                # If saber dance is ready, and technical is the next GCD or we opened with Technical first and we are in the second oGCD slot - Use Saber
                # If Saber is ready and technical is the next GCD or we opened with Technical first and our next GCD is greater than 1.5 away, close the ogcd slot to ensure saber gets second slot
                # if saber dance is ready, our opener used Saber First and technicalstep is the next gcd and nextgcd is 1.7 away, wait. To ensure second oGCD slot
                # if flourish is available, we have 0 flourish procs, and technical dance isn't less than 4* our Current GCD seconds away and we aren't dancing twice in the next 15, and we aren't in a buff window with 50 or more Esprit - use flourish
                # if our potion is ready and the next saber dance is less than 15 seconds away - use potion
                # if we have a flourished fan and are double dancing in the next 15 seconds or flourish is up, use Fan Dance III
                # if we have a flourished fan and the fan is close to dropping, use Fan Dance III
                # If we have a flourished fan and the next buff window is more than 13.5 seconds away, use Fan Dance III
                # if we have a flourished fan and we have 4 feathers, use Fan Dance III
                # If we are in a buffwindow and have a flourished fan, use Fan Dance III
                # If we are in a buffwindow and have feathers use Fan Dance I
                # IF we have 4 feathers and some other flourish proc - Use Fan Dance I
                abilityused = False

                if technicaldancing or standarddancing:
                    abilityused = False
                elif saberdance.available(clock) and ((technicalstep.nextuse <= nextgcd and delaystart - technicalstep.nextuse > 23) or (technicalfirst and delaystart - clock > 16)) and nextgcd - abilitydelay >= clock:
                    if createlog:
                        logging.info(str(clock)+ " : You use Saber Dance!")
                    saber.activate(clock)
                    saberdance.putonCD(clock)
                    abilityused = True
                    ignoreabilitydelay = True
                    nextaction = technicalstep.nextuse
                elif saberdance.available(clock) and (technicalstep.nextuse <= nextgcd and delaystart - technicalstep.nextuse > 23) and (round(nextgcd - 1.5 ,2) < clock or not technicalstep.nextuse == nextgcd): #Wait for Second oGCD window for Saber dance
                    abilityused = False
                elif flourish.available(clock) and (countprocs(clock) == 0) and not (flourishfan.getactive(clock)) and not (nextdancetype == 'Technical' and round(nextgcd + (modGCDrecast*4), 2) > nextdance) and dancenumber < 2 and not(buffwindow and esprit >= 50):
                    if createlog:
                        logging.info(str(clock)+ ' : You use Flourish!')
                    flourishcascade.activate(clock)
                    flourishbloodshower.activate(clock)
                    flourishwindmill.activate(clock)
                    flourishfountain.activate(clock)
                    flourishfan.activate(clock)
                    flourish.putonCD(clock)
                    abilityused = True
                elif potion.available(clock) and (nextgcd - nextaction) > 1.5 and (saberdance.getrecast(clock) < 15) and potionbuff.available :
                    if createlog:
                        logging.info(str(clock)+' : You use a potion!')
                    potionbuff.activate(clock)
                    potion.putonCD(clock)
                    nextaction = round(clock + .7,2)
                    abilityused = True
                elif flourishfan.getactive(clock)and fandance3.available(clock) and (dancenumber > 1 or flourish.available(clock)): # Use it right away so we don't risk losing proc
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif flourishfan.getactive(clock) and fandance3.available(clock) and flourishfan.closetodrop(clock , modGCDrecast): # Use it if it drops in a GCD
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif flourishfan.getactive(clock) and fandance3.available(clock) and nextbuffwindow > 13.5: # Use it if there isn't a buff window coming
                    potency = potency + fandance3.getpotency(clock,False,False,CDHStats,potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif flourishfan.getactive(clock) and feathers > 3: # Use it if we have 4 feathers
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif buffwindow and flourishfan.getactive(clock):
                    potency = potency + fandance3.getpotency(clock, False, False, CDHStats, potmod)
                    flourishedfans = flourishedfans + 1
                    flourishfan.dropbuff(clock)
                    abilityused = True
                elif buffwindow and feathers > 0 and fandance1.available(clock):
                    potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                    feathersused = feathersused + 1
                    feathers = feathers - 1
                    abilityused = True
                    if checkproc():
                        flourishfan.activate(clock)
                elif feathers > 3 and not (flourishfan.getactive(clock)) and fandance1.available(clock):
                    potency = potency + fandance1.getpotency(clock,False,False,CDHStats,potmod)
                    feathersused = feathersused + 1
                    feathers = feathers - 1
                    abilityused = True
                    if checkproc():
                        flourishfan.activate(clock)
                if abilityused: #Process new action time
                    if not ignoreabilitydelay:
                        nextaction = round(clock + abilitydelay, 2)
                        if nextaction + abilitydelay > nextgcd and not saberdance.available(nextgcd):
                            nextaction = round(nextgcd, 2) #I want to avoid clipping
                else:
                    if not ignoreabilitydelay:
                        nextaction = round(clock + .01, 2)
                        if nextaction + abilitydelay > nextgcd and not saberdance.available(nextgcd):
                            nextaction = round(nextgcd, 2) #I want to avoid clipping



            #if technicalstep.nextuse < round(clock + modGCDrecast,2) and not round(technicalstep.nextuse, 2) == nextgcd and not standarddancing and technicalhold and not delay and delaystart < technicalstep.nextuse + 22:
            #    print(str(clock)+' : Time Lost Technical: ' + str(technicalstep.nextuse)+'   ' +str(nextgcd))
            #    techhold = round(techhold + (technicalstep.nextuse - nextgcd), 2)
            #    nextgcd = round(technicalstep.nextuse, 2)
            #elif standardstep.nextuse < round(clock+(modGCDrecast),2) and (technicalstep.nextuse - clock) > (6.5 + modGCDrecast) and not technicaldancing and not round(standardstep.nextuse, 2) == nextgcd and standardhold and not delay and delaystart < standardstep.nextuse + 5:
            #    #print(str(clock)+' :Time Lost Standard: ' + str(round(standardstep.nextuse - nextgcd,2)))
            #    standhold = round(standhold + (standardstep.nextuse - nextgcd), 2)
            #    nextgcd = round(standardstep.nextuse, 2)

            #check to see if its within any GCD use at my current clock position
            #check to make sure its not happening in the next GCD
            #make sure I'm not dancing
            # make sure its a technical hold
            # check if the delay start time - its next use is greater than 22 before enforcing the hold
            # Make sure I have enough time to saber dance? How do I check that
            if technicalstep.nextuse < round(clock + modGCDrecast, 2) and not (technicalstep.nextuse == nextgcd) and not standarddancing and technicalhold and delaystart - technicalstep.nextuse > 22: #
                techhold = round(techhold + (technicalstep.nextuse - nextgcd), 2)
                nextgcd = round(technicalstep.nextuse, 2)

            elif standardstep.nextuse < round(clock + (modGCDrecast), 2) and (technicalstep.nextuse - clock) > ( 6.5 + modGCDrecast) and not technicaldancing and not round(standardstep.nextuse,2) == nextgcd and standardhold and delaystart - standardstep.nextuse > 5.2:

                standhold = round(standhold + (standardstep.nextuse - nextgcd), 2)
                nextgcd = round(standardstep.nextuse, 2)

        potency = round(potency,3)
        if (oldpot != potency) or (oldesprit != esprit) or (oldfeathers != feathers):
            if createlog:
                logging.info(str(clock)+ ' : Potency: '+str(potency)+' || Dex: '+str(dex)+' || Feathers: '+str(feathers)+' || Esprit: '+str(esprit)+ ' || Buff window: '+str(buffwindow)+' '+str(potmod)+ ' || Crit Rate: '+str(CDHStats[0])+ ' || DH Rate: '+str(CDHStats[2]))
            oldpot = potency
            oldesprit = esprit
            oldfeathers = feathers
        clock = round(clock + .01, 2)

    if createlog:
        logging.info("------Results-----")
        logging.info("Time Ran : "+str(clock))
        logging.info("Potency : "+str(potency))
        logging.info("Potency per Second : "+str(potency/clock))
        logging.info("Feathers Remaining: "+str(feathers))
        logging.info("Esprit Remaining: "+str(esprit))
        logging.info("GCDs Used: "+str(gcd))
        logging.info("Feathers used: "+str(feathersused))
        logging.info("Flourished Fans: "+str(flourishedfans))
        logging.info("Devilments Used: "+str(useddevilments))

        global comboscreated
        global totalprocs
        global featherattempt
        global feathersdropped
        global espritcap
        global espritattempt
        global espritattemptparty

        logging.info('Combos Made: '+str(comboscreated))
        logging.info('Combos Dropped: ' + str(combodrops))
        logging.info('Percent Drop : ' + str(combodrops/comboscreated))
        logging.info('Flourish Procs Generated : ' + str(totalprocs))
        logging.info('Flourish Procs Dropped : ' + str(procdrop))
        logging.info('Percent Drop : ' + str(procdrop / totalprocs))
        logging.info('Feathers Attempt: ' + str(featherattempt))
        logging.info('Feathers Dropped : ' + str(feathersdropped))
        logging.info('Percent Drop : ' + str(feathersdropped / featherattempt))
        logging.info('Esprit Attempt: ' + str(espritattemptparty+espritattempt))
        logging.info('Esprit Cap : ' + str(espritcap))
        logging.info('Percent Drop : ' + str(espritcap / (espritattemptparty+espritattempt)))

    dex = basedex
    return potency

def astmodule(clock,table):

    astgcd = 2.4
    # currentseals,allseals,nextaction,sleevestacks,nextgcd,card,cardheld,arcana,astopen,astopener,inastopen
    currentseals = table[0]
    allseals = table[1]
    nextaction= table[2]
    sleevestacks = table[3]
    nextgcd = table[4]
    card = table[5]
    cardheld = table[6]
    arcana = table[7]
    astopen = table[8]
    astopener = table[9]
    inastopen = table[10]
    astpriority = table[11]
    delaytable = table[12]
    delayedpos = table[13]


    if astopen:
            if astopener[inastopen].actiontime == clock:
                currentaction = astopener[inastopen]
                if currentaction.name == 'Play':
                    if card[1].buff:
                        if not astpriority:
                            if not notmycard.getactive(clock):
                                notmycard.activate(clock)
                        elif not goodcard.getactive(clock):
                            goodcard.activate(clock)
                    currentseals.append(card[1].seal)
                    allseals = checkseals(currentseals)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                    cardheld = False
                elif currentaction.name == 'Draw':
                    card = justdraw(currentseals,allseals,clock)
                    draw.putonCD(clock)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                    if sleevebuff.getactive(clock):
                        sleevestacks = sleevestacks - 1
                    cardheld = True
                elif currentaction.name == 'Sleeve Draw':
                    sleevebuff.activate(clock)
                    sleevestacks = 2
                    sleeve.putonCD(clock)
                    draw.setCD(3)
                    draw.nextuse = round(clock, 2)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name == 'Divination':
                    divination.specialactivate(clock,allseals)
                    currentseals = []
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name == 'Redraw':
                    foundseal = False
                    for up in currentseals:
                        if up == card[1].seal:
                            foundseal = True
                    if foundseal:
                        card = justdraw(currentseals,allseals,clock)
                        redraw.putonCD(clock)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name =='GCD':
                    nextaction = round(clock + .7, 2)
                    nextgcd = round(clock + .7, 2)
                    inastopen = inastopen + 1
                elif currentaction.name =='oGCD':
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name=='Hold':
                    inastopen = inastopen + 1
            if inastopen >= len(astopener):
                astopen = False
                if nextaction > nextgcd:
                    nextgcd = round(nextaction, 2)

                if nextaction + .7 > nextgcd:
                    nextaction = round(nextgcd, 2)

    else:
            if sleevebuff.getactive(clock) and sleevestacks == 0:
                sleevebuff.dropbuff(clock)
                draw.setCD(30)
            elif not sleevebuff.getactive(clock) and sleevestacks > 0:
                draw.setCD(30)
                sleevestacks = 0
            elif sleevebuff.getactive(clock):
                draw.setCD(3)
            if clock == nextgcd:
                nextgcd = round(clock + astgcd, 2)
                nextaction = round(clock + .7, 2)
            elif nextaction == clock:
                allseals = checkseals(currentseals)
                if sleeve.available(clock) and not draw.available(clock) and len(currentseals)<2:
                    sleeve.putonCD(clock)
                    sleevebuff.activate(clock)
                    sleevestacks = 2
                    draw.nextuse = clock
                    nextaction = round(clock + .7, 2)
                elif sleeve.available(clock) and not draw.available(clock) and divination.starttime - clock < 5:
                    sleeve.putonCD(clock)
                    sleevebuff.activate(clock)
                    sleevestacks = 2
                    draw.nextuse = clock
                    nextaction = round(clock + .7, 2)
                elif divination.starttime == clock and len(currentseals) > 2:
                    divination.specialactivate(clock,checkseals(currentseals))
                    currentseals = []
                    nextaction = round(clock + .7, 2)
                elif not cardheld and draw.available(clock):
                    card = drawcard(currentseals,allseals,clock)
                    if sleevebuff.getactive:
                        sleevestacks = sleevestacks - 1
                    nextaction = round(clock + .7 +card[2], 2)
                    draw.putonCD(clock)
                    cardheld = True
                elif cardheld and divination.starttime - clock < 20 and not allseals:
                    if card[1].buff:
                        if not astpriority:
                            if not notmycard.getactive(clock) or goodcard.getactive(clock) or bigcard.getactive(clock):
                                notmycard.getactive(clock)
                            else:
                                goodcard.activate(clock)
                            currentseals.append(card[1].seal)
                        cardheld = False
                elif cardheld and not astpriority and not notmycard.getactive(clock):
                    if not (card[0] == 'Lord' or card[0] == 'Lady'):
                        if not notmycard.getactive(clock) and card[1].buff:
                            notmycard.activate(clock)
                        cardheld = False
                        currentseals.append(card[1].seal)
                    elif arcana:
                        if not notmycard.getactive(clock) and card[1].buff:
                            notmycard.activate(clock)
                        cardheld = False
                        arcana = False
                    else:
                        arcana = True
                    nextaction = round(clock + card[2], 2)
                elif cardheld and (not (goodcard.getactive(clock) or bigcard.getactive(clock)) or sleevebuff.getactive(clock)):
                    if not( card[0] == 'Lord' or card[0] == 'Lady'):
                        if (not goodcard.getactive(clock) or not bigcard.getactive(clock)) and card[1].buff:
                            goodcard.activate(clock)
                        cardheld = False
                        currentseals.append(card[1].seal)
                    elif arcana:
                        if (not goodcard.getactive(clock) or not bigcard.getactive(clock)) and card[1].buff:
                            bigcard.activate(clock)
                        cardheld = False
                        arcana = False
                    else:
                        arcana = True
                    nextaction = round(clock + card[2], 2)

                else:
                        nextaction = round(nextaction + .01, 2)

            if nextaction > nextgcd:
                    nextgcd = round(nextaction ,2)

            if nextaction + .7 > nextgcd:
                    nextaction = round(nextgcd, 2)

            if divination.starttime == clock:
                divination.starttime = round(clock + .01, 2)

    return [currentseals,checkseals(currentseals),nextaction,sleevestacks,nextgcd,card,cardheld,arcana,astopen,astopener,inastopen, astpriority, delaytable, delayedpos]

def settings():
    settingsmenu = ['1: Set Party Comp', '2: Set Stats', '3: Reset log', '4: Exit']
    for i in settingsmenu:
        print(i)
    choice = input('Please select a command: ')
    tomenu = True
    try:
        choice = int(choice)
    except:
        tomenu = False
        print('Please put a proper command')

    if tomenu:
        if choice == 1:
            number = 1
            stayin = True
            while(stayin):
                number = 1
                for i in jobs:
                    print(str(number)+' : '+i.name+ ': '+str(i.active))
                    number = number + 1
                print(str(number)+' : Exit')
                choice = input('Please pick what jobs to activate')
                try:
                    choice = int(choice)
                    if choice >= number:
                        if buildparty():
                            stayin = False
                        else:
                            print('Please Build a Valid party')
                    else:
                        jobs[choice-1].switch()
                except:
                    print('Please Enter a valid number')

def testdraws():
    reset()
    clock = 0
    currentseals = []
    allseals = False
    drawing = 0
    drawinglimit = 300
    #print(str(clock)+' : Played a '+card[0])
    #currentseals.append(card[1].seal)
    nextaction = 0
    sleevestacks = 0
    divination.starttime = 0.01
    astgcd = 2.4
    nextgcd = 0

    card = drawcard(currentseals,False,clock)
    firstcardset = True
    cardheld = True
    arcana = False
    astopen = True
    global createlog
    createlog = True
    astopener = buildasttable()
    inastopen = 0
    global threepercent
    global sixpercent
    #for i in astopener:
    #    print(str(i.actiontime)+' : '+i.name)
#opener = ['Hold .7','GCD','Play', 'oGCD', 'GCD', 'Draw', 'Sleeve Draw', 'GCD', 'Play', 'Draw', 'GCD', 'Redraw','Play','GCD', 'Divination']

    while(clock < 17):

        if astopen:
            if astopener[inastopen].actiontime == clock:
                currentaction = astopener[inastopen]
                if currentaction.name == 'Play':
                    if not arcana:
                        if card[1].buff:
                            if not goodcard.getactive(clock):
                                goodcard.activate(clock)
                    else:
                        arcana = False
                        if card[1].buff and not bigcard.getactive(clock):
                            bigcard.activate(clock)
                    currentseals.append(card[1].seal)
                    allseals = checkseals(currentseals)
                    #print(str(clock)+' : Played '+card[1].name)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name == 'Draw':
                    card = justdraw(currentseals,allseals,clock)
                    draw.putonCD(clock)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                    if sleevebuff.getactive(clock):
                        sleevestacks = sleevestacks - 1
                elif currentaction.name == 'Sleeve Draw':
                    #print(str(clock)+ ': Sleeve')
                    sleevebuff.activate(clock)
                    sleevestacks = 2
                    sleeve.putonCD(clock)
                    draw.setCD(3)
                    draw.nextuse = round(clock, 2)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name == 'Minor Arcana':
                    arcana = True
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name == 'Divination':
                    #print(currentseals)
                    if allseals:
                        sixpercent = sixpercent + 1
                    else:
                        threepercent = threepercent + 1
                    divination.specialactivate(clock,allseals)
                    currentseals = []
                    #print(str(clock)+' : ' +str(divination.getpotency(clock)))
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name == 'Redraw':
                    foundseal = False
                    for up in currentseals:
                        if up == card[1].seal:
                            foundseal = True
                    if foundseal:
                        oldcard = card[1].name
                        while oldcard == card[1].name:
                            card = justdraw(currentseals,allseals,clock)
                        redraw.putonCD(clock)
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name =='GCD':
                    nextaction = round(clock + .7, 2)
                    nextgcd = round(clock + .7, 2)
                    inastopen = inastopen + 1
                elif currentaction.name =='oGCD':
                    inastopen = inastopen + 1
                    nextaction = round(clock + .7, 2)
                elif currentaction.name=='Hold':
                    inastopen = inastopen + 1
            if inastopen >= len(astopener):
                astopen = False
                if nextaction > nextgcd:
                    nextgcd = round(nextaction, 2)

                if nextaction + .7 > nextgcd:
                    nextaction = round(nextgcd, 2)
                #print('Done with Opener')

        else:
            if sleevebuff.getactive(clock) and sleevestacks == 0:
                #print(sleevestacks)
                sleevebuff.dropbuff(clock)
                draw.setCD(30)
            elif not sleevebuff.getactive(clock) and sleevestacks > 0:
                draw.setCD(30)
                sleevestacks = 0
            elif sleevebuff.getactive(clock):
                draw.setCD(3)
            if clock == nextgcd:
                nextgcd = round(clock + astgcd, 2)
                #print(str(clock)+ ' : Some Star attack')
                nextaction = round(clock + .7, 2)
            elif nextaction == clock:
                allseals = checkseals(currentseals)
                if sleeve.available(clock) and not draw.available(clock) and len(currentseals)<2:
                    sleeve.putonCD(clock)
                    #print(str(clock)+ ' : You use Sleeve Draw')
                    sleevebuff.activate(clock)
                    sleevestacks = 2
                    draw.nextuse = clock
                    nextaction = round(clock + .7, 2)
                elif sleeve.available(clock) and not draw.available(clock) and divination.starttime - clock < 5:
                    sleeve.putonCD(clock)
                    print(str(clock) + ' : You use Sleeve Draw')
                    sleevebuff.activate(clock)
                    sleevestacks = 2
                    draw.nextuse = clock
                    nextaction = round(clock + .7, 2)
                elif firstcardset:
                    nextaction = nextaction + .7
                    #print(str(clock)+' : Played a ' + card[1].name)
                    if card[1].buff:
                        goodcard.activate(clock)
                        #print('You get small buff')
                    currentseals.append(card[1].seal)
                    firstcardset = False
                    cardheld = False
                elif divination.starttime == clock and len(currentseals) > 2:
                    #print(currentseals)
                    divination.activate(clock)
                    currentseals = []
                    nextaction = round(clock + .7, 2)
                    #if allseals:
                         #print(str(clock)+': 6% Potency')
                    #else:
                        #print(str(clock) + ': 3% Potency')
                elif not cardheld and draw.available(clock):
                    card = drawcard(currentseals,allseals,clock)
                    if sleevebuff.getactive:
                        sleevestacks = sleevestacks - 1
                    nextaction = round(clock + .7 +card[2], 2)
                    draw.putonCD(clock)
                    cardheld = True
                elif cardheld and divination.starttime - clock < 25 and not allseals:
                        #print(str(clock)+' : Played a '+card[1].name)
                        currentseals.append(card[1].seal)
                        cardheld = False
                elif cardheld and (not (goodcard.getactive(clock) or bigcard.getactive(clock)) or sleevebuff.getactive(clock)):
                        if not( card[0] == 'Lord' or card[0] == 'Lady'):
                            #print(str(clock) + ' : Played a ' + card[0])
                            if (not goodcard.getactive(clock) or not bigcard.getactive(clock)) and card[1].buff:
                                #print(card[1].buff)
                                goodcard.activate(clock)
                                #print('You get small buff')
                            cardheld = False
                            currentseals.append(card[1].seal)
                        elif arcana:
                            #print(str(clock) + ' : Played a ' + card[0])
                            if (not goodcard.getactive(clock) or not bigcard.getactive(clock)) and card[1].buff:
                                bigcard.activate(clock)
                                #print('You get big buff')
                            cardheld = False
                            arcana = False
                        else:
                            arcana = True
                            #print(str(clock) +' : Used Minor Arcana')
                        nextaction = round(clock + card[2], 2)

                else:
                        nextaction = round(nextaction + .01, 2)

            if nextaction > nextgcd:
                    nextgcd = round(nextaction ,2)

            if nextaction + .7 > nextgcd:
                    nextaction = round(nextgcd, 2)

            if divination.starttime == clock:
                divination.starttime = round(clock + .01, 2)

        clock = round(clock + .01, 2)

def main():
    # timestorun  = input('Number of times to run?')
    # cascadecombo(timestorun)
    # open()
    # buildopentable()
    global createlog
    createlog = False
    latetrick = ['Standard Finish', 'Flourish', 'Bloodshower','Potion','Reverse Cascade', 'Hold .70', 'Saber Dance',
               'Technical Step', 'AutoOGCD 1',
               'AutoGCD', 'AutoOGCD 2', 'Standard Step', 'AutoOGCD 1', 'AutoGCD']

    selflessopener = ['Standard Finish','Saber Dance', 'Technical Step','Potion', 'Cascade', 'Flourish', 'Reverse Cascade', 'AutoOGCD 2', 'AutoGCD']
    selflessopener2 = ['Standard Finish', 'Flourish', 'Technical Step', 'Saber Dance', 'Bloodshower','Potion','Reverse Cascade', 'AutoOGCD 2', 'Fountainfall', 'Standard Step', 'AutoOGCD 1', 'AutoGCD']
    earlytrick = ['Standard Finish', 'Flourish', 'Bloodshower', 'Potion', 'Saber Dance', 'Technical Step','Reverse Cascade', 'AutoOGCD 2', 'Fountainfall', 'Standard Step', 'AutoOGCD 1', 'AutoGCD']
    openers = [earlytrick, latetrick, selflessopener2 ]
    openernames = ['Early Trick',  'Late Trick', 'Selfless']
    print('---Dancer Sim V1.0---')
    print('---Author: Ellunavi---')
    print('Contributors: ')
    print(' ')
    print(' ')
    print(' ')
    exit = False
    while(not exit):
        print('----Menu----')
        print('1: Compare Openers')
        print('2: Log Sim')
        print('3: Settings')
        print('4: Compare Sims')
        print('5: Run Sim')
        print('6: Exit')
        print('7: Debug')
        createlog = False
        tomenu = True
        choice = input('Please Select: ')
        try:
            choice = int(choice)
        except:
            print('Please enter a valid command')
            tomenu = False
        if tomenu:
            if int(choice) == 1:
                index = 0
                while index < len(openernames):
                    print(str(index +1)+ ' : '+str(openernames[index]))
                    index = index + 1
                try:
                    firstone = int(input('Select one of the two openers to compare: '))
                    secondone = int(input('Select another opener to compare: '))
                    iterations = int(input('Please enter the number of times you want to compare: '))
                    runtime = int(input('How long do you want to run them: '))
                except:
                    break
                totaltimes = int(iterations)
                opener1potencies = []
                opener2potencies = []
                while(iterations > 0):
                    opener1potencies.append(sim(openers[firstone-1],runtime))
                    opener2potencies.append(sim(openers[secondone-1],runtime))
                    iterations = iterations - 1
                open1answer = 0
                open2answer = 0
                open1peak = opener1potencies[0]
                open1floor = opener1potencies[0]
                open2peak = opener2potencies[0]
                open2floor = opener2potencies[0]
                while iterations < totaltimes:
                    if open1peak < opener1potencies[iterations]:
                        open1peak = opener1potencies[iterations]
                    elif open1floor > opener1potencies[iterations]:
                        open1floor = opener1potencies[iterations]
                    if open2peak < opener2potencies[iterations]:
                            open2peak = opener2potencies[iterations]
                    elif open2floor > opener2potencies[iterations]:
                            open2floor = opener2potencies[iterations]
                    open1answer = open1answer + opener1potencies[iterations]
                    open2answer = open2answer + opener2potencies[iterations]
                    iterations = iterations + 1
                open1answer = round((open1answer / totaltimes)/runtime, 4)
                open1peak = round(open1peak/runtime, 4)
                open1floor = round(open1floor/runtime, 4)
                open2answer = round((open2answer / totaltimes)/runtime, 4)
                open2peak = round(open2peak / runtime, 4)
                open2floor = round(open2floor / runtime, 4)
                print(str(openernames[firstone - 1])+' Result: '+str(open1answer))
                print(str(openernames[firstone - 1]) + ' Peak: ' + str(open1peak))
                print(str(openernames[firstone - 1]) + ' Floor: ' + str(open1floor))
                print(str(openernames[secondone - 1]) + ' Result: ' + str(open2answer))
                print(str(openernames[secondone - 1]) + ' Peak: ' + str(open2peak))
                print(str(openernames[secondone - 1]) + ' Floor: ' + str(open2floor))
            if int(choice) == 2:
                index = 0
                while index < len(openernames):
                    print(str(index+1)+' : '+openernames[index])
                    index = index +1
                try:
                    selectopener = int(input('Please Select which opener to use: '))
                except:
                    break
                createlog = True
                runtimes = input('Run Sim how long: ')
                sim(openers[selectopener-1],int(runtimes))
                print('Please check log file for results')
            if int(choice) == 3:
                settings()
            if int(choice) == 4:
                iterations = input('Please enter the number of times you want to compare: ')
                totaltimes = int(iterations)
                iterations = int(iterations)
                opener1potencies = []
                opener2potencies = []
                while (iterations > 0):
                    opener1potencies.append(sim(earlytrick, 600))
                    opener2potencies.append(sim(earlytrick, 600))
                    iterations = iterations - 1
                open1answer = 0
                open2answer = 0
                while iterations < totaltimes:
                    open1answer = open1answer + opener1potencies[iterations]
                    open2answer = open2answer + opener2potencies[iterations]
                    iterations = iterations + 1
                open1answer = round((open1answer / totaltimes)/600, 4)
                open2answer = round((open2answer / totaltimes)/600, 4)
                print('Sim 1 Result: ' + str(open1answer))
                print('Sim 2 Result: ' + str(open2answer))
            if int(choice) == 5:
                iterations = input('Please enter the number of times you want to run: ')
                runningtime = int(input('Please enter the time to run the sim too: '))
                totaltimes = int(iterations)
                iterations = int(iterations)
                opener1potencies = []
                while (iterations > 0):
                    opener1potencies.append(sim(latetrick, runningtime))
                    iterations = iterations - 1
                open1answer = 0
                topparse = opener1potencies[0]
                bottomparse = opener1potencies[0]
                while iterations < totaltimes:
                    if topparse < opener1potencies[iterations]:
                        topparse = opener1potencies[iterations]
                    if bottomparse > opener1potencies[iterations]:
                        bottomparse = opener1potencies[iterations]
                    open1answer = open1answer + opener1potencies[iterations]
                    iterations = iterations + 1
                open1answer = round((open1answer / totaltimes) / runningtime, 4)
                print('Opener 1 Result: ' + str(open1answer))
                print('Top Result: ' + str(round(topparse/runningtime,4)))
                print('Bottom Result: ' + str(round(bottomparse/runningtime, 4)))
            if int(choice) == 6:
                exit = True
            if int(choice) == 7:
                runningtime = 600
                delaystart = [45]
                delayfinish = [80]
                buffdelay = True
                createlog = True
                delaytable = [[45,80,True], [128,140,True], [240,290, True]]
                simholds(latetrick,runningtime,delaytable)
            else:
                print('Please enter a valid command')








main()




