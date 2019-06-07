import PySimpleGUI as sg
import DNC as sim
import math
import statistics
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import tkinter as Tk
import matplotlib.pyplot as plt

openers = sim.returnopeners()
fights = sim.returnfights()
layout = [[sg.Text("DNC Simulator")],
          [sg.Text("Sim One Stats"), sg.Text(''),sg.Text('',size=(20,1)),sg.Text('Sim Two Stats')],
          [sg.Text("Weapon Damage",size=(14,1)), sg.Input(default_text='114',size=(8,1),key='wd1',do_not_clear=True), sg.Text('',size=(10,1)),sg.Text("Weapon Damage",size=(14,1)), sg.Input(default_text='114',size=(8,1),key='wd2',do_not_clear=True)],
          [sg.Text("Weapon Delay",size=(14,1)), sg.Input(default_text='3.12',size=(8,1),key='del1',do_not_clear=True),sg.Text('',size=(10,1)),sg.Text("Weapon Delay",size=(14,1)), sg.Input(default_text='3.12',size=(8,1),key='del2',do_not_clear=True)],
          [sg.Text("Dexterity",size=(14,1)), sg.Input(default_text='3662',size=(8,1),key='dex1',do_not_clear=True),sg.Text('',size=(10,1)),sg.Text("Dexterity",size=(14,1)), sg.Input(size=(8,1),key='dex2',do_not_clear=True)],
          [sg.Text("Critical Hit Rate",size=(14,1)), sg.Input(default_text='1967',size=(8,1),key='crit1',do_not_clear=True),sg.Text('',size=(10,1),key='crate1'),sg.Text("Critical Hit Rate",size=(14,1)), sg.Input(default_text='1967',size=(8,1),key='crit2',do_not_clear=True),sg.Text('',key='crate2',size=(10,1))],
          [sg.Text("Direct Hit",size=(14,1)), sg.Input(default_text='1806',size=(8,1),key='dh1',do_not_clear=True),sg.Text('',size=(10,1),key='direct1'),sg.Text("Direct Hit",size=(14,1)), sg.Input(default_text='1806',size=(8,1),key='dh2',do_not_clear=True),sg.Text('',key='direct2',size=(10,1))],
          [sg.Text("Determination",size=(14,1)), sg.Input(default_text='1462',size=(8,1),key='det1',do_not_clear=True),sg.Text('',size=(10,1),key='deter1'),sg.Text("Determination",size=(14,1)), sg.Input(default_text='1462',size=(8,1),key='det2',do_not_clear=True),sg.Text('',key='deter2',size=(10,1))],
          [sg.Text("Skill Speed",size=(14,1)), sg.Input(default_text='1283',size=(8,1),key='sks1',do_not_clear=True),sg.Text('',size=(10,1),key='skill1'),sg.Text("Skill Speed",size=(14,1)), sg.Input(default_text='1283',size=(8,1),key='sks2',do_not_clear=True),sg.Text('',key='skill2',size=(10,1))],
          [sg.Text("Opener", size=(14,1)), sg.InputCombo(openers, key='open1'), sg.Text('',size=(5,1)), sg.Text("Opener", size=(14,1)), sg.InputCombo(openers, key='open2')],
          [sg.Text("Fight", size=(14,1)), sg.InputCombo(fights,key='fights'), sg.Text('',size=(1,1)),sg.Text('Create Log'),sg.Radio('Yes','LOGS',size=(3,1),key="logon"),sg.Radio('No','LOGS',size=(3,1),default=True,key='logoff')],
          [sg.Text("Length of Fight", size=(16,1)),sg.Input(default_text='300',size=(8,1),key='length')],
          [sg.Text("Run How many Times", size=(16,1)),sg.Input(default_text='200',size=(8,1),key='runtime')],
          [sg.Button('Run Sim',key='sim'),sg.Text('',size=(20,1)),sg.Button('Set Party',key='party')]]
sim1 =['wd1','del1','dex1','crit1','dh1','det1','sks1']
sim2 =['wd2','del2','dex2','crit2','dh2','det2','sks2']


def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas
    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = Tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
    canvas.create_image(loc[0] + figure_w / 2, loc[1] + figure_h / 2, image=photo)
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
    return photo



if __name__ == '__main__':
    window = sg.Window("DNC Simulator").Layout(layout)

    win2_active = False
    win3_active = False

    while True:
        button, values = window.Read(timeout=100)

        if button is None:
            break
        #Update window elements
        try:
            window.FindElement('crate1').Update(sim.returncrit(int(values['crit1'])))
        except:
            window.FindElement('crate1').Update('')
        try:
            window.FindElement('direct1').Update(sim.returndh(int(values['dh1'])))
        except:
            window.FindElement('direct1').Update('')
        try:
            window.FindElement('deter1').Update(sim.returndet(int(values['det1'])))
        except:
            window.FindElement('deter1').Update('')
        try:
            window.FindElement('skill1').Update(sim.returngcd(int(values['sks1'])))
        except:
            window.FindElement('skill1').Update('')
        try:
            window.FindElement('crate2').Update(sim.returncrit(int(values['crit2'])))
        except:
            window.FindElement('crate2').Update('')
        try:
            window.FindElement('direct2').Update(sim.returndh(int(values['dh2'])))
        except:
            window.FindElement('direct2').Update('')
        try:
            window.FindElement('deter2').Update(sim.returndet(int(values['det2'])))
        except:
            window.FindElement('deter2').Update('')
        try:
            window.FindElement('skill2').Update(sim.returngcd(int(values['sks2'])))
        except:
            window.FindElement('skill2').Update('')

        #Process window generation when we want to change party UI
        if not win2_active and button == 'party':
            window.Hide()
            win2_active = True
            nin = sim.getactivejob('NIN')
            layout2 = [[sg.Text('Job', size=(8,1)),sg.Text('Member',size=(8,1)),sg.Text('Partner',size=(8,1)), sg.Text('Buff Priority',size=(8,1))],
                       [sg.Text('NIN',size=(8,1)), sg.Checkbox('', default=sim.getactivejob('NIN'),size=(8,1),key='NIN'), sg.Radio('','partner',default=sim.ispartner('NIN'),size=(8,1),key='NINpart')],
                       [sg.Text('DRG', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('DRG'), size=(8, 1), key='DRG'),
                        sg.Radio('', 'partner', default=sim.ispartner('DRG'), size=(8, 1), key='DRGpart'), sg.Checkbox('Tether',size=(10,1),default=sim.priority("DRG"),key='DRGprio')],
                       [sg.Text('MNK', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('MNK'), size=(8, 1), key='MNK'),
                        sg.Radio('', 'partner', default=sim.ispartner('MNK'), size=(8, 1), key='MNKpart')],
                       [sg.Text('SAM', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('SAM'), size=(8, 1), key='SAM'),
                        sg.Radio('', 'partner', default=sim.ispartner('SAM'), size=(8, 1), key='SAMpart')],
                       [sg.Text('BRD', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('BRD'), size=(8, 1), key='BRD'),
                        sg.Radio('', 'partner', default=sim.ispartner('BRD'), size=(8, 1), key='BRDpart')],
                       [sg.Text('MCH', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('MCH'), size=(8, 1), key='MCH'),
                        sg.Radio('', 'partner', default=sim.ispartner('MCH'), size=(8, 1), key='MCHpart')],
                       [sg.Text('RDM', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('RDM'), size=(8, 1), key='RDM'),
                        sg.Radio('', 'partner', default=sim.ispartner('RDM'), size=(8, 1), key='RDMpart')],
                       [sg.Text('SMN', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('SMN'), size=(8, 1), key='SMN'),
                        sg.Radio('', 'partner', default=sim.ispartner('SMN'), size=(8, 1), key='SMNpart')],
                       [sg.Text('BLM', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('BLM'), size=(8, 1), key='BLM'),
                        sg.Radio('', 'partner', default=sim.ispartner('BLM'), size=(8, 1), key='BLMpart')],
                       [sg.Text('WHM', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('WHM'), size=(8, 1), key='WHM'),
                        sg.Radio('', 'partner', default=sim.ispartner('WHM'), size=(8, 1), key='WHMpart')],
                       [sg.Text('SCH', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('SCH'), size=(8, 1), key='SCH'),
                        sg.Radio('', 'partner', default=sim.ispartner('SCH'), size=(8, 1), key='SCHpart')],
                       [sg.Text('AST', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('AST'), size=(8, 1), key='AST'),
                        sg.Radio('', 'partner', default=sim.ispartner('AST'), size=(8, 1), key='ASTpart'), sg.Checkbox('Priority', size =(10,1), default=sim.priority('AST'), key="ASTprio")],
                       [sg.Text('GNB', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('GNB'), size=(8, 1), key='GNB'),
                        sg.Radio('', 'partner', default=sim.ispartner('GNB'), size=(8, 1), key='GNBpart')],
                       [sg.Text('WAR', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('WAR'), size=(8, 1), key='WAR'),
                        sg.Radio('', 'partner', default=sim.ispartner('WAR'), size=(8, 1), key='WARpart')],
                       [sg.Text('DRK', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('DRK'), size=(8, 1), key='DRK'),
                        sg.Radio('', 'partner', default=sim.ispartner('DRK'), size=(8, 1), key='DRKpart')],
                       [sg.Text('PLD', size=(8, 1)),
                        sg.Checkbox('', default=sim.getactivejob('PLD'), size=(8, 1), key='PLD'),
                        sg.Radio('', 'partner', default=sim.ispartner('PLD'), size=(8, 1), key='PLDpart')],

                       [sg.Button('Done')]]

            win2 = sg.Window('Party Screen').Layout(layout2)
        #Process information when Sim its clicked
        if not win3_active and button == 'sim':
            simoneaction = True
            simtwoaction = True
            simonetable = []
            simtwotable = []
            fight = values['fights']
            if values['logon']:
                logging = True
            else:
                logging = False
            #try:
            for i in sim1:
                if values[i] == '':
                    simoneaction = False
                else:
                        simonetable.append(float(values[i]))
            if not simoneaction:
                sg.PopupOK('Please enter in Values for Sim One')
            else:
                for i in sim2:
                    if values[i] == '':
                        simtwoaction = False
                    else:
                        simtwotable.append(float(values[i]))
                if simtwoaction:
                    runtimes = int(values['runtime'])
                    runlength = int(values['length'])

                    opener1 = values['open1']
                    opener2 = values['open2']
                    potency1 = []
                    potency2 = []
                    layoutprog = [[sg.Text('Running Sim', key='progtext')],
                                  [sg.ProgressBar(runtimes, orientation='h', size=(20, 20), key='progbar')],
                                  [sg.Button('Cancel')]]
                    progwin = sg.Window('Running Sim One', layoutprog)
                    bar = progwin.FindElement('progbar')
                    sim.setstats(simonetable)
                    for i in range(runtimes):
                        progevent, progvals = progwin.Read(timeout=100)
                        if progevent == 'Cancel' or progevent is None:
                            break
                        results = sim.runsim(logging, opener1, fight, runlength)
                        value = round(results[0], 4)
                        potency1.append(value)
                        bar.UpdateBar(i + 1)
                    progwin.TKroot.title('Running Sim Two')
                    sim.setstats(simtwotable)
                    for i in range(runtimes):
                        progevent, progvals = progwin.Read(timeout=100)
                        if progevent == 'Cancel' or progevent is None:
                            break
                        results = sim.runsim(logging, opener2, fight, runlength)
                        value = round(results[0], 4)
                        potency2.append(value)
                        bar.UpdateBar(i + 1)
                    progwin.Close()
                    sg.PopupAnimated('loading.gif','Finalizing your results',time_between_frames =1)

                    maxval = max(potency1)
                    minval = min(potency1)
                    if runtimes > 1:
                        aveval = statistics.mean(potency1)
                        deviation = round(statistics.stdev(potency1),3)
                    else:
                        aveval = potency1[0]
                        deviation = potency1[0]

                    maxval2 = max(potency2)
                    minval2 = min(potency2)
                    if runtimes > 1:
                        aveval2 = statistics.mean(potency2)
                        deviation2 = round(statistics.stdev(potency2),3)
                    else:
                        aveval2 = potency2[0]
                        deviation = potency2[0]

                    if aveval > aveval2:
                        color1 ='#3CB371'
                        color2 ='#B22222'
                    else:
                        color2 = '#3CB371'
                        color1 = '#B22222'

                    #plt.hist(potency1,
                    #         color='blue',
                    #         edgecolor='black',
                    #         bins=int((maxval - minval)/(runtimes/50)))
                    #fig = plt.gcf()
                    #figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds

                    #plt.hist(potency2,
                    #         color='blue',
                    #         edgecolor='black',
                    #         bins=int((maxval - minval) / (runtimes / 50)))
                    #fig2 = plt.gcf()
                    #figure2_x, figure2_y, figure2_w, figure2_h = fig2.bbox.bounds

                    results_layout = [[sg.Text('Sim One'), sg.Text('', size=(16, 1)),
                                       sg.Text(str(round(aveval, 3)), size=(8, 1), font=('Helvetica', 20),text_color=color1),sg.Text('',size=(2,1)), sg.Text('Sim Two',size=(22,1)), sg.Text(str(round(aveval2, 3)), size=(8, 1), font=('Helvetica', 20),text_color=color2)],
                                      [sg.Text('Weapon Damage: ', size=(14, 1)),
                                       sg.Text(str(int(simonetable[0])), size=(8, 1)), sg.Text('Max', size=(8, 1)),
                                       sg.Text(maxval,size=(10,1)),sg.Text('Weapon Damage: ', size=(14, 1)),
                                       sg.Text(str(int(simtwotable[0])), size=(8, 1)), sg.Text('Max', size=(8, 1)),
                                       sg.Text(maxval2)],
                                      [sg.Text('Weapon Delay: ', size=(14, 1)),
                                       sg.Text(str(simonetable[1]), size=(8, 1)), sg.Text('Min', size=(8, 1)),
                                       sg.Text(minval,size=(10,1)),sg.Text('Weapon Delay: ', size=(14, 1)),
                                       sg.Text(str(simtwotable[1]), size=(8, 1)), sg.Text('Min', size=(8, 1)),
                                       sg.Text(minval2)],
                                      [sg.Text('Dexterity: ', size=(14, 1)),
                                       sg.Text(str(int(simonetable[2])), size=(8, 1)),
                                       sg.Text('Deviation', size=(8, 1)), sg.Text(deviation,size=(10,1)),sg.Text('Dexterity: ', size=(14, 1)),
                                       sg.Text(str(int(simtwotable[2])), size=(8, 1)),
                                       sg.Text('Deviation', size=(8, 1)), sg.Text(deviation2)],
                                      [sg.Text('Critical Hit Rate: ', size=(14, 1)),
                                       sg.Text(str(int(simonetable[3])),size=(8,1)),sg.Text('',size=(20,1)),sg.Text('Critical Hit Rate: ', size=(14, 1)),
                                       sg.Text(str(int(simtwotable[3])))],
                                      [sg.Text('Direct Hit: ', size=(14, 1)), sg.Text(str(int(simonetable[4])),size=(8,1)),sg.Text('',size=(20,1)),sg.Text('Direct Hit: ', size=(14, 1)), sg.Text(str(int(simtwotable[4])))],
                                      [sg.Text('Determination: ', size=(14, 1)), sg.Text(str(int(simonetable[5])),size=(8,1)),sg.Text('',size=(20,1)),sg.Text('Determination: ', size=(14, 1)), sg.Text(str(int(simtwotable[5])))],
                                      [sg.Text('Skillspeed: ', size=(14, 1)), sg.Text(str(int(simonetable[6])),size=(8,1)),sg.Text('',size=(20,1)),sg.Text('Skillspeed: ', size=(14, 1)), sg.Text(str(int(simtwotable[6])))],
                                      [sg.Text('Opener: ', size=(14,1)),sg.Text(opener1,size=(30,1)),sg.Text('Opener: ',size=(14,1)),sg.Text(opener2)],
                                      #[sg.Canvas(size=(figure_w, figure_h), key='canvas'),sg.Canvas(size=(figure_w, figure_h), key='canvas2')],
                                      [sg.Text(sim.returnpartystring())]
                                      [sg.Button('Close')]]
                    if logging:
                        results_layout[10].append(sg.Button('View Logs',key='logview'))
                    resultwindow = sg.Window("Sim Results", force_toplevel=True).Layout(results_layout).Finalize()
                    window.Hide()
                    #fig_photo = draw_figure(resultwindow.FindElement('canvas').TKCanvas, fig)
                    #fig2_photo = draw_figure(resultwindow.FindElement('canvas2').TKCanvas, fig2)
                    sg.PopupAnimated(image_source=None)
                    win3_active = True


                else:
                    runtimes = int(values['runtime'])
                    runlength = int(values['length'])
                    opener1 = values['open1']

                    fight = values['fights']
                    if values['logon']:
                        logging = True
                    else:
                        logging = False
                    potency1 = []
                    layoutprog = [[sg.Text('Running Sim',key='progtext')], [sg.ProgressBar(runtimes, orientation = 'h', size =(20,20),key='progbar')], [sg.Button('Cancel')]]
                    progwin = sg.Window('Running Sim',layoutprog)
                    bar = progwin.FindElement('progbar')
                    for i in range(runtimes):
                        progevent, progvals = progwin.Read(timeout=100)
                        if progevent == 'Cancel' or progevent is None:
                            break

                        results = sim.runsim(logging, opener1, fight, runlength)
                        value = round(results[0],4)
                        potency1.append(value)
                        bar.UpdateBar(i + 1)

                    progwin.Close()
                    sg.PopupAnimated('loading.gif','Finalizing your results',time_between_frames =1)
                    maxval = max(potency1)
                    minval = min(potency1)

                    if runtimes > 1:
                        aveval = statistics.mean(potency1)
                        deviation = round(statistics.stdev(potency1),3)
                    else:
                        aveval = potency1[0]
                        deviation = potency1[0]
                    if runtimes > 1 :
                        plt.hist(potency1,
                                 color='blue',
                                 edgecolor='black',
                                 bins=int((maxval - minval)/(runtimes/50)))
                        fig = plt.gcf()
                        figure_x, figure_y, figure_w, figure_h = fig.bbox.bounds
                    else:
                        figure_w = 8
                        figure_h = 1
                    results_layout =[[sg.Text('Stats Used'),sg.Text('',size=(16,1)),sg.Text(str(round(aveval,3)),size=(8,1),font=('Helvetica',20))],
                                     [sg.Text('Weapon Damage: ',size=(14,1)), sg.Text(str(int(simonetable[0])),size=(8,1)),sg.Text('Max',size=(8,1)),sg.Text(maxval)],
                                     [sg.Text('Weapon Delay: ',size=(14,1)), sg.Text(str(simonetable[1]),size=(8,1)),sg.Text('Min',size=(8,1)),sg.Text(minval)],
                                     [sg.Text('Dexterity: ',size=(14,1)), sg.Text(str(int(simonetable[2])),size=(8,1)),sg.Text('Deviation',size=(8,1)),sg.Text(deviation)],
                                     [sg.Text('Critical Hit Rate: ',size=(14,1)), sg.Text(str(int((simonetable[3]))))],
                                     [sg.Text('Direct Hit: ',size=(14,1)), sg.Text(str(int(simonetable[4])))],
                                     [sg.Text('Determination: ',size=(14,1)), sg.Text(str(int(simonetable[5])))],
                                     [sg.Text('Skillspeed: ',size=(14,1)), sg.Text(str(int(simonetable[6])))],
                                     [sg.Text('Opener: ', size=(14, 1)), sg.Text(opener1, size=(30, 1))],
                                     [sg.Canvas(size=(figure_w, figure_h), key='canvas')],
                                     [sg.Text(sim.returnpartystring())],
                                     [sg.Button('Close')]]
                    if logging:
                        results_layout[11].append(sg.Button('View Logs',key='logview'))
                    resultwindow = sg.Window("Sim Results", force_toplevel=True).Layout(results_layout).Finalize()
                    window.Hide()
                    if runtimes > 1:
                        fig_photo = draw_figure(resultwindow.FindElement('canvas').TKCanvas,fig)
                    sg.PopupAnimated(image_source=None)
                    win3_active = True





            #except:
             #   sg.PopupOK('Please Enter Valid Numbers')





        if win2_active:
            button2, values2 = win2.Read(timeout=100)
            if button2 is None:
                win2_active = False
                win2.Close()
                window.UnHide()
            elif button2 is 'Done':
                partyset = []
                jobs = ['NIN','DRG','MNK','SAM','BRD','MCH','RDM','SMN','BLM','WHM','SCH','AST','GNB','WAR','DRK','PLD']
                membernumber = 0
                for i in jobs:
                    partyset.append([i,values2[i]])
                    if values2[i]:
                        membernumber = membernumber + 1
                if membernumber > 7:
                    sg.PopupOK('You have to many members')
                else:
                    foundpart = False
                    partner = 'None'
                    for i in partyset:
                        if i[1]:
                            if values2[i[0]+'part']:
                                foundpart = True
                                partner = i[0]

                    if not foundpart:
                        sg.PopupOK('You need to select a valid partner')
                    else:
                        sim.setparty(partyset,partner,values2['DRGprio'],values2['ASTprio'])
                        win2_active = False
                        win2.Close()
                        window.UnHide()


        if win3_active:

            resevents, resvalus = resultwindow.Read(timeout=100)

            if resevents is None or resevents == 'Close':
                win3_active = False
                resultwindow.Close()
                window.UnHide()
            elif resevents is 'logview':
                logfile = open('Dnc_Sim_Results.log','r')
                sg.PopupScrolled(logfile.read(),size=(80,None))



