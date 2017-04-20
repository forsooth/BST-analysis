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

def plot(logn, logt, opsn, opst):

        plt.rcParams["font.family"] = "Input Mono"

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Elements Accessed Over Time')
        ax.set_xlabel('Element in BST')
        ax.set_ylabel('Time')
        
        fontP = FontProperties()
        fontP.set_size('small')

        xrng = max(logn) - min(logn)
        yrng = max(logt) - min(logt)
        plt.xlim(min(logn) - 0.05 * xrng, max(logn) + 0.05 * xrng)
        plt.ylim(min(logt) - 0.05 * yrng, max(logt) + 0.05 * yrng)

        log = ax.scatter(logn, logt, s=10, c='b', marker="x", label='Intermediate accesses')
        ops = ax.scatter(opsn, opst, s=20, c='r', marker="o", label='Operation arguments')
        plt.legend(handles=[ops, log], prop = fontP, loc='upper center', 
                   bbox_to_anchor=(0.5, -0.12),
                   fancybox=True, shadow=False, ncol=2)

        
        plt.savefig('outputs/' + str(datetime.now()) + '.pdf',
                    bbox_inches='tight', dpi=300, pad_inches=0.5)

