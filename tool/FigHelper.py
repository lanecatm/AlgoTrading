# -*- encoding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from Log import Log

class FigHelper:
    def __init__(self):
        return


    def draw_bar_fig(self, data, x = None, color='g', xLabel = "", yLabel = "", title = "", label = ""):
        if x == None:
            x = np.arange(len(data))
        plt.bar(x, data, color=color, label = label)
        self.__set_param(xLabel, yLabel, title)
        return

    def draw_plot_fig(self, data, x = None, color='r', xLabel = "", yLabel = "", title = "", label = "", linestyle = "-", strXLabel = None, strXLabelNumber = None):
        if x == None:
            x = np.arange(len(data))
        plotTmp = plt.plot(x, data, color = color, label = label, linestyle = linestyle)
        if strXLabel != None and strXLabelNumber != None:
            ax=plt.gca()  
            ax.set_xticks(np.linspace(0,strXLabelNumber - 1,strXLabelNumber))
            ax.set_xticklabels(strXLabel)  

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

    def __set_param(self, xLabel = "", yLabel = "", title = ""):
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        return
