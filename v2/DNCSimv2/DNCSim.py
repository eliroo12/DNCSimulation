import simdictionary
from ability import ability
from buff import buff
from job import job
from sim import sim
import stats

import simdictionary as build


def main():

    dex = 3662
    WD = 114
    det = 1462
    ss = 1283
    crit = 1967
    dh = 1806
    wepdelay = 3.12
    critchance, critbonus = stats.determinecrit(crit)
    gcd = 2.38
    dhrate = stats.determinedh(dh)

    # stat table build out = WD,Wepdelay,Dex,Critrate,Critdamage,Directrate,Det,skillspeed,gcd
    stattable = [WD, wepdelay, dex, critchance, critbonus, dhrate, det, ss, gcd]
    jobs = build.genjobs()
    party = build.genparty(jobs)
    pbuffs = build.genpbuffs(party)
    buffs = build.genbuffs()
    abilities = build.genabil(wepdelay,gcd)
    settings = build.settings()
    openers = settings[0]
    fights = settings[1]
    #while gcd > 2.2:
        #print(gcd)
    stattable = [WD, wepdelay, dex, critchance, critbonus, dhrate, det, ss, gcd]
    sim(1,600,openers['Late Trick'],fights['Default'],stattable,abilities,party,pbuffs,buffs,True,True).sim()
    gcd = round(gcd - .01,2)
        #if gcd == 2.21:
            #gcd = 2.5






main()

