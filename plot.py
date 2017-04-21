# from pyx import *
# 
# g = graph.graphxy(width=8)
# g.plot(graph.data.file("plot.dat", x=1, y=2))
# g.writePDFfile("plot")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages as pdfbackend
from datetime import datetime
import matplotlib.gridspec as gridspec
from matplotlib.font_manager import FontProperties
import err
import colors
import matplotlib.ticker as ticker
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)
from matplotlib.cbook import get_sample_data
import os

def plot(logn, logt, opsn, opst, pages, graphs, debug):
        with pdfbackend('outputs/' + str(datetime.now()) + '.pdf') as pdf:

                plt.rcParams["font.family"] = "Input Mono"

                cwd = os.getcwd()

                xmax = max(logn)
                xmin = min(logn)
                ymax = max(logt)
                ymin = min(logt)
                xrng = max(xmax - xmin, 1)
                yrng = max(ymax - ymin, 1)
                roots = {}

                if pages:
                        partial_logn = []
                        partial_logt = []
                        partial_opst = []
                        partial_opsn = []
                        last_logt_i = 0
                        logt_i = 0
        
                        for i in range(0, len(opst)):
                                if debug == 1:
                                        if debug == 2:
                                                err.log("Generating data plot number " + str(i))
                                partial_opst.append(opst[i])
                                partial_opsn.append(opsn[i])
                                op_t = opst[i]
                                last_logt_i = logt_i + 1
                                while logt_i + 1 < len(logt) and logt[logt_i + 1] <= op_t:
                                        logt_i += 1
        
                                roots[logt[last_logt_i]] = logn[last_logt_i]
        
                                for j in range(last_logt_i, logt_i + 1):
                                        partial_logt.append(logt[j])
                                        partial_logn.append(logn[j])

                                if debug == 2:
                                        err.log("Starting plot generation")
        
                                add_plot(pdf, cwd, partial_logn, partial_logt,
                                         partial_opsn, partial_opst,
                                         xmax, xmin, ymax, ymin, xrng,
                                         yrng, roots, graphs, i, debug)
                else:
                        roots = {}
                        for i, t in enumerate(logt):
                                if t not in roots.keys():
                                        roots[t] = logn[i]

                        add_plot(pdf, cwd, logn, logt,
                                 opsn, opst,
                                 xmax, xmin, ymax, ymin, xrng,
                                 yrng, roots, graphs, len(graphs) - 1, debug)


def add_plot(pdf, cwd, 
             logn, logt, opsn, opst,
             xmax, xmin, ymax, ymin,
             xrng, yrng,
             roots,
             graphs, graph_i,
             debug):

                yloc = ticker.MultipleLocator(base=1.0)
                xloc = ticker.MultipleLocator(base=1.0)

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


                pad_xlim = [xmin - 0.05 * xrng, xmax + 0.05 * xrng]
                pad_ylim = [ymin - 0.05 * yrng, ymax + 0.05 * yrng]
                ylim = [0, ymax]
                yloc.view_limits(ymin, ymax)
                xloc.view_limits(xmin, xmax)

                if debug == 2:
                        err.log("Created axes")
                
                ax_main.set_xlabel('Element in BST')
                ax_main.set_ylabel('Time')
                ax_main.spines['top'].set_visible(False)
                ax_main.spines['right'].set_visible(False)
                ax_main.set_axisbelow(True)
                ax_main.set_aspect('auto', adjustable="box-forced")
                ax_main.set_xlim(pad_xlim)
                ax_main.set_ylim(pad_ylim)

                ax_main.yaxis.set_minor_locator(yloc)
                ax_main.yaxis.grid(True, which='minor', color=colors.h_light_gray)
                
                ax_main.xaxis.set_minor_locator(xloc)
                ax_main.xaxis.grid(True, which='minor', color=colors.h_light_gray)

                if debug == 2:
                        err.log("Set up main plot")

                log = ax_main.scatter(logn, logt, s=1000 / 2 / max(xrng, yrng), 
                                      c=[colors.h_light_blue if roots[logt[i]] != logn[i] else colors.h_dark_blue for i in range(0, len(logt))],
                                      marker="x", 
                                      label='Intermediate accesses')

                if debug == 2:
                        err.log("Plotted Xs")

                ops = ax_main.scatter(opsn, opst, s=1000 / max(xrng, yrng), 
                                 c=colors.h_red, 
                                 marker="o", 
                                 label='Operation arguments')

                if debug == 2:
                        err.log("Plotted Os")

                t_counts = {}
                pairs = set()
                for t in range(0, max(logt) + 1):
                        t_counts[t] = 0

                for i, t in enumerate(logt):
                        if (t, logn[i]) not in pairs:
                                pairs.add((t, logn[i]))
                                t_counts[t] += 1

                if debug == 2:
                        err.log("Generated y-axis histogram data")

                xlim = [0, xmax]

                ax_count.set_xlabel('# Accesses At This Time')
                ax_count.spines['top'].set_visible(False)
                ax_count.spines['right'].set_visible(False)
                ax_count.set_axisbelow(True)
                ax_count.set_aspect('auto', adjustable="box-forced")
                ax_count.yaxis.set_minor_locator(yloc)
                ax_count.yaxis.grid(True, which='minor', color=colors.h_light_gray)
                ax_count.set_xlim(xlim)
                ax_count.set_ylim(pad_ylim)
                ax_count.tick_params(axis='y', which='both', left='off')
                ax_count.set_yticklabels([])

                if debug == 2:
                        err.log("Set up y-axis histogram axis")

                ax_count.barh(list(t_counts.keys()), 
                              t_counts.values(), 
                              min(yrng, 128) / 128,
                              align='center',
                              color=colors.h_dark_blue)

                if debug == 2:
                        err.log("Created y-axis histogram bar chart")

                n_counts = {}
                pairs = set()
                for n in range(min(logn), max(logn) + 1):
                        n_counts[n] = 0

                for i, n in enumerate(logn):
                        if (n, logt[i]) not in pairs:
                                pairs.add((n, logt[i]))
                                n_counts[n] += 1

                if debug == 2:
                        err.log("Generated x-axis histogram data")

                ax_vcount.set_ylabel('# Accesses of This Element')
                #ax_vcount.spines['bottom'].set_visible(False)
                ax_vcount.spines['right'].set_visible(False)
                ax_vcount.spines['top'].set_visible(False)
                ax_vcount.set_axisbelow(True)
                ax_vcount.set_aspect('auto', adjustable="box-forced")
                ax_vcount.xaxis.set_minor_locator(xloc)
                ax_vcount.xaxis.grid(True, which='minor', color=colors.h_light_gray)
                ax_vcount.set_xlim(pad_xlim)
                ax_vcount.set_ylim(ylim)
                ax_vcount.yaxis.set_label_position('left')
                ax_vcount.yaxis.tick_left()
                ax_vcount.tick_params(axis='x', which='both', bottom='off')
                ax_vcount.set_xticklabels([])

                if debug == 2:
                        err.log("Set up x-axis histogram axis")

                ax_vcount.bar(list(n_counts.keys()), 
                              n_counts.values(), 
                              min(xrng, 128) / 128,
                              align='center',
                              color=colors.h_dark_blue)

                if debug == 2:
                        err.log("Generated y-axis histogram data")

                ax_none.spines['top'].set_visible(False)
                ax_none.spines['bottom'].set_visible(False)
                ax_none.spines['right'].set_visible(False)
                ax_none.spines['left'].set_visible(False)
                ax_none.set_xticklabels([])
                ax_none.set_yticklabels([])
                ax_none.axis('off')

                if debug == 2:
                        err.log("Set up tree image axis")

                if len(graphs) != 0:
                        graph = graphs[graph_i]
                        graph.write_png(cwd + "/outputs/tmp_tree.png")
        
                        tree_img = get_sample_data(cwd + "/outputs/tmp_tree.png")
                        img_obj = plt.imread(tree_img, format='png')
                        plt.imshow(img_obj)
        
                        if debug == 2:
                                err.log("Added tree image")

                if debug == 1:
                        err.log("Saving new PDF page...")
                pdf.savefig(bbox_inches='tight', dpi=600, pad_inches=0.5)

