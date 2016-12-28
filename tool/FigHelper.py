# -*- encoding:utf-8 -*-
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from Log import Log
import matplotlib.dates as mdate
from matplotlib.pyplot import savefig

class FigHelper:
    def __init__(self):
        return


    def draw_bar_fig(self, data, x = None, color='g', xLabel = "", yLabel = "", title = "", label = ""):

        if x == None:
            x = np.arange(len(data))
        plt.bar(x, data, color=color, label = label, width = 0.0005)
        if xLabel!="" or yLabel != "" or title!= "":
            self.__set_param(xLabel, yLabel, title)
        return

    def draw_plot_fig(self, data, x = None, color='r', xLabel = "", yLabel = "", title = "", label = "", linestyle = "-", strXLabel = None, strXLabelNumber = None, rotation = False):
        
        if x == None:
            x = np.arange(len(data))
        plotTmp = plt.plot(x, data, color = color, label = label, linestyle = linestyle)
        ax=plt.gca()  
        if strXLabel != None and strXLabelNumber != None:
            ax.set_xticks(np.linspace(0,strXLabelNumber - 1,strXLabelNumber))
            ax.set_xticklabels(strXLabel)  
        if rotation:
            plt.xticks(rotation=90)
        if isinstance(x[0], datetime.datetime):
            ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))

        self.__set_param(xLabel, yLabel, title)
        return plotTmp

    def draw_point_fig(self, data, x = None, color='b', xLabel = "", yLabel = "", title = "", label = ""):
        if x == None:
            x = np.arange(len(data))
        plotTmp = plt.plot(x, data, color + 'o', label = label)
        self.__set_param(xLabel, yLabel, title)
        #pl.legend([plot1, plot2], (’red line’, ’green circles’), ’best’, numpoints=1)
        return plotTmp

    def finish(self):
        plt.legend(loc = 'best', numpoints=1)
        plt.show()
        return

    def set_save(self):
        mpl.use('Agg')
    def save(self):
        savefig('../tradePercentage.jpg') 
        plt.legend(loc = 'best', numpoints=1)

    def __set_param(self, xLabel = "", yLabel = "", title = ""):
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        return
