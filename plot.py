# from pyx import *
# 
# g = graph.graphxy(width=8)
# g.plot(graph.data.file("plot.dat", x=1, y=2))
# g.writePDFfile("plot")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from matplotlib.font_manager import FontProperties
import err
import matplotlib.ticker as ticker

def plot(logn, logt, opsn, opst):

        roots = []
        root_ts = []
        for i, t in enumerate(logt):
                if t not in root_ts:
                        root_ts.append(t)
                        roots.append(i)

        plt.rcParams["font.family"] = "Input Mono"
        fig = plt.figure()
        
        ax = fig.add_subplot(111)
        ax.set_title('Elements Accessed Over Time')
        ax.set_xlabel('Element in BST')
        ax.set_ylabel('Time')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_axisbelow(True)

        loc = ticker.MultipleLocator(base=1.0)
        ax.yaxis.set_minor_locator(loc)
        # ax.set_yticks([x for x in logt], minor=True)
        ax.yaxis.grid(True, which='minor', color='#eeeeee')

        fontP = FontProperties()
        fontP.set_size('small')

        xmax = max(logn)
        xmin = min(logn)
        ymax = max(logt)
        ymin = min(logt)
        xrng = xmax - xmin
        yrng = ymax - ymin
        plt.xlim(xmin - 0.05 * xrng, xmax + 0.05 * xrng)
        plt.ylim(ymin - 0.05 * yrng, ymax + 0.05 * yrng)

        log = ax.scatter(logn, logt, s=10, 
                        c=['#768fff' if i not in roots 
                           else '#2962ff' for i, x in enumerate(logn)],
                        marker="x", 
                        label='Intermediate accesses')

        ops = ax.scatter(opsn, opst, s=15, 
                         c='#ef5350', 
                         marker="o", 
                         label='Operation arguments')
        
        plt.legend(handles=[ops, log], prop = fontP, loc='upper center', 
                   bbox_to_anchor=(0.5, -0.12),
                   fancybox=True, shadow=False, ncol=2)

        
        plt.savefig('outputs/' + str(datetime.now()) + '.pdf',
                    bbox_inches='tight', dpi=300, pad_inches=0.5)

