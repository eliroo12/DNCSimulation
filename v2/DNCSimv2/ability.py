import math
import random

#Need to define charged, charges and maxCD for charges abilities
class ability:

    def __init__(self, name, abiltype, targtype, cooldown, potency, nextuse, combopotency):
        self.name = name
        self.abiltype = abiltype
        self.targtype = targtype
        self.cooldown = cooldown
        self.potency = potency
        self.nextuse = nextuse
        self.combopotency = combopotency
        self.charged = False
        self.charges = 0
        self.maxcooldown = self.charges * self.cooldown

    #Calculated damage and creates log if needed
    def getpotency(self, time, cdhstats, potmod, stats, combo):
        Auto = False
        if self.name == 'Auto Attack':
            Auto = True

        pot = 0
        string = str(time) + ' : You use ' + str(self.name)
        if combo and self.combopotency > 0:
            pot = int(self.combopotency)
        else:
            pot = int(self.potency)

        pot = self.returndamage(pot, Auto, stats)

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

        pot = round(pot,4)
        string = string+' - '+str(pot)+ ' damage'
        self.nextuse = round(time + self.cooldown,2)
        return [pot, string]

    #puts ability on CD
    def putonCD(self,time):
        if not self.charged:
            self.nextuse = round(time + self.cooldown, 2)
        else:
            if time - self.nextuse < 90:
                self.nextuse = self.nextuse + self.cooldown
            else:
                self.nextuse = time + self.cooldown

    #Checks if ability is vailable
    def available(self,time):
        if not self.charged:
            return time >= self.nextuse
        else:
            return math.floor(self.charges - (self.nextuse - time) / self.cooldown) > 0

    #check the recast time
    def getrecast(self,time):
        if time >= self.nextuse:
            return 0
        else:
            return self.nextuse - time

    #put ability on CD
    def setCD(self, newCD):
        self.cooldown = newCD

    # reset values
    def reset(self):
        self.nextuse = 0

    def returndamage(self, pot, auto, stats):
        JobMod = 115
        WD = stats[0]
        wepdelay = stats[1]
        dex = stats[2]
        det = stats [3]
        ss = stats [4]
        dexstat = math.floor(dex * 1.05)
        Damage = 0
        if auto:
            Damage = math.floor(pot * ((WD + math.floor(340 * JobMod / 1000)) * (wepdelay / 3)) * (
                        100 + math.floor((dexstat - 340) * 1000 / 2336)) / 100)
            Damage = math.floor(Damage * (1000 + math.floor(130 * (det - 340) / 3300)) / 1000)
            Damage = math.floor(Damage * (1000 + math.floor(130 * (ss - 380) / 3300)) / 1000)
            Damage = math.floor(Damage * (1000 + math.floor(100 * (380 - 380) / 3300)) / 1000 / 100)
        else:
            Damage = math.floor(
                pot * (WD + math.floor(340 * JobMod / 1000)) * (100 + math.floor((dexstat - 340) * 1000 / 2336)) / 100)
            Damage = math.floor(Damage * (1000 + math.floor(130 * (det - 340) / 3300)) / 1000)
            Damage = math.floor(Damage * (1000 + math.floor(100 * (380 - 380) / 3300)) / 1000 / 100)

        return Damage * (random.randrange(95, 105) / 100)