# from pyx import *
# 
# g = graph.graphxy(width=8)
# g.plot(graph.data.file("plot.dat", x=1, y=2))
# g.writePDFfile("plot")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import matplotlib.gridspec as gridspec
from matplotlib.font_manager import FontProperties
import err
import colors
import matplotlib.ticker as ticker

def plot(logn, logt, opsn, opst):

        plt.rcParams["font.family"] = "Input Mono"
        loc = ticker.MultipleLocator(base=1.0)
        fontP = FontProperties()
        fontP.set_size('small')

        fig = plt.figure(1, (10., 10.))

        gs = gridspec.GridSpec(2, 2)

        kx = dict(aspect='auto')

        ax_main = plt.subplot(gs[1, 0], **kx)
        ax_count = plt.subplot(gs[1, 1], **kx)
        ax_vcount = plt.subplot(gs[0, 0], **kx)
        ax_none = plt.subplot(gs[0, 1], **kx)

        gs.update(wspace=0.00, hspace=-0.00)

        xmax = max(logn)
        xmin = min(logn)
        ymax = max(logt)
        ymin = min(logt)
        xrng = xmax - xmin
        yrng = ymax - ymin
        pad_xlim = [xmin - 0.05 * xrng, xmax + 0.05 * xrng]
        pad_ylim = [ymin - 0.05 * yrng, ymax + 0.05 * yrng]
        ylim = [0, ymax]
        
        #ax_main.set_title('Elements Accessed Over Time')
        ax_main.set_xlabel('Element in BST')
        ax_main.set_ylabel('Time')
        ax_main.spines['top'].set_visible(False)
        ax_main.spines['right'].set_visible(False)
        ax_main.set_axisbelow(True)
        ax_main.set_aspect('auto', adjustable="box-forced")
        ax_main.set_xlim(pad_xlim)
        ax_main.set_ylim(pad_ylim)

        ax_main.yaxis.set_minor_locator(loc)
        ax_main.yaxis.grid(True, which='minor', color=colors.h_light_gray)
        ax_main.xaxis.set_minor_locator(loc)
        ax_main.xaxis.grid(True, which='minor', color=colors.h_light_gray)

        roots = []
        root_ts = []
        for i, t in enumerate(logt):
                if t not in root_ts:
                        root_ts.append(t)
                        roots.append(i)

        log = ax_main.scatter(logn, logt, s=500 / max(xrng, yrng), 
                              c=[colors.h_light_blue if i not in roots else colors.h_dark_blue for i, x in enumerate(logn)],
                              marker="x", 
                              label='Intermediate accesses')

        ops = ax_main.scatter(opsn, opst, s=1000 / max(xrng, yrng), 
                         c=colors.h_red, 
                         marker="o", 
                         label='Operation arguments')

        t_counts = {}
        for t in range(min(logt), max(logt) + 1):
                t_counts[t] = 0

        for i, t in enumerate(logt):
                t_counts[t] += 1

        xlim = [0, max(t_counts.values()) + 1]

        ax_count.set_xlabel('# Accesses At This Time')
        ax_count.spines['top'].set_visible(False)
        #ax_count.spines['left'].set_visible(False)
        ax_count.spines['right'].set_visible(False)
        ax_count.set_axisbelow(True)
        ax_count.set_aspect('auto', adjustable="box-forced")
        ax_count.yaxis.set_minor_locator(loc)
        ax_count.yaxis.grid(True, which='minor', color=colors.h_light_gray)
        ax_count.set_xlim(xlim)
        ax_count.set_ylim(pad_ylim)
        ax_count.tick_params(axis='y', which='both', left='off')
        ax_count.set_yticklabels([])
        #ax_count.yaxis.set_visible(False)

        ax_count.barh(list(t_counts.keys()), 
                      t_counts.values(), 
                      min(len(t_counts.keys()), 128) / 128,
                      align='center',
                      color=colors.h_dark_blue)

        n_counts = {}
        for n in range(min(logn), max(logn) + 1):
                n_counts[n] = 0

        for i, n in enumerate(logn):
                n_counts[n] += 1

        ax_vcount.set_ylabel('# Accesses of This Element')
        #ax_vcount.spines['bottom'].set_visible(False)
        ax_vcount.spines['right'].set_visible(False)
        ax_vcount.spines['top'].set_visible(False)
        ax_vcount.set_axisbelow(True)
        ax_vcount.set_aspect('auto', adjustable="box-forced")
        ax_vcount.xaxis.set_minor_locator(loc)
        ax_vcount.xaxis.grid(True, which='minor', color=colors.h_light_gray)
        ax_vcount.set_xlim(pad_xlim)
        ax_vcount.set_ylim(ylim)
        ax_vcount.yaxis.set_label_position('left')
        ax_vcount.yaxis.tick_left()
        ax_vcount.tick_params(axis='x', which='both', bottom='off')
        ax_vcount.set_xticklabels([])
        #ax_vcount.xaxis.set_visible(False)

        ax_vcount.bar(list(n_counts.keys()), 
                      n_counts.values(), 
                      min(len(n_counts.keys()), 128) / 128,
                      align='center',
                      color=colors.h_dark_blue)

        ax_none.spines['top'].set_visible(False)
        ax_none.spines['bottom'].set_visible(False)
        ax_none.spines['right'].set_visible(False)
        ax_none.spines['left'].set_visible(False)
        ax_none.set_visible(False)

        #plt.legend(handles=[ops, log], prop = fontP, loc='upper center', 
        #           bbox_to_anchor=(0.5, -0.12),
        #           fancybox=True, shadow=False, ncol=2)

        plt.savefig('outputs/' + str(datetime.now()) + '.pdf',
                    bbox_inches='tight', dpi=300, pad_inches=0.5)

