import matplotlib.pyplot as plt
import sys
import os
import textwrap
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
from Utils.RobotQAUtils.plateReader import *
from  Utils.RobotQAUtils.classes import *
width = 0.35

def printVolumeAbs(dilutionStatistics):
    volumes = []
    absorbences = []
    for d in dilutionStatistics:
        volumes.append(d.manualColumn.getColorVolume())
        absorbences.append(d.getManualMean())
    plt.plot(volumes,absorbences, 'ro')
    plt.show()