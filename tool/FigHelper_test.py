# -*- encoding:utf-8 -*-
import sys
import numpy as np
from FigHelper import FigHelper
if __name__ == '__main__':
    figHelper = FigHelper()
    data = np.array([5, 2, 8])
    figHelper.draw_bar_fig(data, xLabel = "xLabel")
    figHelper.draw_plot_fig(data)
    figHelper.finish()
    sys.exit()
