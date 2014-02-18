import textwrap
import sys
import os
import matplotlib.pyplot as plt
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
import plateReader
tinyNum =  0.000001

def print3DGraph(listOfaxisLists = None,Xlabel = None,Ylable = None,Zlabel = None,title = None):
    '''for each expiriment prints a rectangle  of percent of wells deviating 20 percent  or more  then the mean.
    the mean is calculated for robot and manual seperatly'''
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #iterating throguh axisList and print them
    for axisList in listOfaxisLists:
        for axis in axisList:
            bar =   ax.bar(axis.xs, axis.ys, zs=axis.zs, zdir='y', color=axis.color,width=width,align='center')
    if not Xlabel:
        ax.set_xlabel('X')
    else:
        ax.set_xlabel(Xlabel)
    if not Ylable:
        ax.set_ylabel('Y')
    else:
        ax.set_ylabel(Ylable)
    if not Zlabel:
        ax.set_zlabel('Z')
    else:
        ax.set_xlabel(Zlabel)
    ax.set_zlabel('Z - unique wells percent')
    plt.show()