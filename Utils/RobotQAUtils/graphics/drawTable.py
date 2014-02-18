# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def printLegend(rowLabels,colLabels,params):
    fig = plt.figure()
    col_labels=colLabels
    row_labels=rowLabels
    table_vals=params
    the_table = plt.table(cellText=table_vals,
    colWidths = [0.2]*4,
    rowLabels=row_labels,
    colLabels=col_labels,
    loc='center')
    plt.text(12,3.4,'Table Title',size=8)
    plt.title('Legend for expiriments')
    plt.show()