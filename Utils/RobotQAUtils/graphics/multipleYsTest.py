import matplotlib.pyplot as plt
import sys
import os
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
from Utils.RobotQAUtils.plateReader import *
from Utils.RobotQAUtils.classes import *
width = 0.35

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)
def printMultipleYs(ds = None):
    fig = plt.figure()
    fig.subplots_adjust(right=0.75)

    host = fig.add_subplot(111)
    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()
    par4 = host.twinx()
    par5 = host.twinx()
    par6 = host.twinx()
    par7 = host.twinx()
    # Offset the right spine of par2.  The ticks and label have already been
    # placed on the right by twinx above.
    par1.spines["right"].set_position(("axes", float(1.0/7.0)))
    par2.spines["right"].set_position(("axes",float(2.0/7.0)))
    par3.spines["right"].set_position(("axes", float(3.0/7.0)))
    par4.spines["right"].set_position(("axes", float(4.0/7.0)))
    par5.spines["right"].set_position(("axes", float(5.0/7.0)))
    par6.spines["right"].set_position(("axes", float(6.0/7.0)))
    par7.spines["right"].set_position(("axes", float(7.0/7.0)))
# Having been created by twinx, par2 has its frame off, so the line of its
    # detached spine is invisible.  First, activate the frame but make the patch
    # and spines invisible.
    make_patch_spines_invisible(par1)
    make_patch_spines_invisible(par2)
    make_patch_spines_invisible(par3)
    make_patch_spines_invisible(par4)
    make_patch_spines_invisible(par5)
    make_patch_spines_invisible(par6)
    make_patch_spines_invisible(par7)

# Second, show the right spine.
    par1.spines["right"].set_visible(True)
    par2.spines["right"].set_visible(True)
    par3.spines["right"].set_visible(True)
    par4.spines["right"].set_visible(True)
    par5.spines["right"].set_visible(True)
    par6.spines["right"].set_visible(True)
    par7.spines["right"].set_visible(True)
    for idx,d in enumerate(ds):
            manualDeviationPercent,robotdeviationPercents= d.getManualAndRobotDeviationPercent()
            manualDeviationPercent*=10#enlarging the scale of the robot
            manualMean = d.getManualMean()*100
            robotMean = d.getRobotMean()*100
            manualUniqueWellsPercent = d.getUniqueWellsCompareToOutsideMeanPercent(outsideMean = d.getManualMean(),rob=False)
            robotUniqueWellsPercent = d.getUniqueWellsCompareToOutsideMeanPercent(outsideMean = d.getRobotMean(),rob=True)
            if not idx%7:
                color = 'r-'
            elif not idx%6:
                color = 'b-'
            elif not idx%5:
                color ='g-'
            elif not idx%4:
                color = 'y-'
            elif not idx%3:
                color = 'y-'
            elif not idx%2:
                color = 'b-'
            else:
                color = 'g-'
            host.plot([0, 1, 2,3,4,5,6,7], [idx,d.getManualColorVolume(), manualDeviationPercent, robotdeviationPercents,manualMean,robotMean,manualUniqueWellsPercent,robotUniqueWellsPercent],color)
    host.set_xlim(0, 7)
    host.set_ylim(0, 100)
    par1.set_ylim(0, 100)
    par2.set_ylim([0, 10])
    par3.set_ylim(0, 100)
    par4.set_ylim([0, 1])
    par5.set_ylim([0,1])
    par6.set_ylim([0, 1])
    par7.set_ylim(0, 100)
    host.set_xlabel("a 4 axis graph")
    host.set_ylabel("expiriment index")
    par1.set_ylabel("volume")
    par2.set_ylabel("manual deviation percent")
    par3.set_ylabel("robot deviation percent")
    par4.set_ylabel("manual mean")
    par5.set_ylabel("robot mean")
    par6.set_ylabel("manual unique wells percent")
    par7.set_ylabel("robot unique wells percent")
# host.yaxis.label.set_color(p1.get_color())
    #par1.yaxis.label.set_color(p2.get_color())
    #par2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=5, width=1.5)
    host.tick_params(axis='y', **tkw)
    par1.tick_params(axis='y',  **tkw)
    par2.tick_params(axis='y',  **tkw)
    par3.tick_params(axis='y',  **tkw)
    host.tick_params(axis='x', **tkw)

    #lines = [p1, p2, p3]

    #host.legend(lines, [l.get_label() for l in lines])

    plt.show()

