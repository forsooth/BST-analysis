import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.gridspec as gridspec
from matplotlib.font_manager import FontProperties
import err
import colors
import matplotlib.ticker as ticker
import os
from pyx import canvas, document, epsfile
import numpy as np
import sys


def plot(logn, logt, opsn, opst, pages, graphs, no_clean, debug):

        fname = str(datetime.now()).replace(' ', '_')

        plt.rc('font', family='Input Mono') 
        cwd = sys.path[0]

        try:
                os.mkdir(cwd + '/../tmp')
                if debug > 0:
                        err.log('../tmp/ directory created for temporary storage.')
        except FileExistsError:
                if debug > 0:
                        err.log('../tmp/ directory exists; using it for temporary storage.')

        new_logn = []
        new_logt = []
        new_pairs = set()
        for i, t in enumerate(logt):
                p = (t, logn[i])
                if p not in new_pairs:
                        new_logn.append(logn[i])
                        new_logt.append(t)

        logn = new_logn
        logt = new_logt

        xmax = int(max(logn))
        xmin = int(min(logn))
        ymax = int(max(logt))
        ymin = int(min(logt))
        xrng = max(xmax - xmin, 0)
        yrng = max(ymax - ymin, 0)

        roots = {}
        t_counts = np.zeros(yrng + 1)
        n_counts = np.zeros(xrng + 1)
        t_pairs = set()
        n_pairs = set()

        ylist = range(ymin, ymax + 1)
        xlist = range(xmin, xmax + 1)

        xticker_base = 1.0
        if xrng > ticker.MultipleLocator.MAXTICKS - 50:
                xticker_base = xrng / ticker.MultipleLocator.MAXTICKS * 1.5

        yticker_base = 1.0
        if yrng > ticker.MultipleLocator.MAXTICKS - 50:
                yticker_base = yrng / ticker.MultipleLocator.MAXTICKS * 1.5

        yloc = ticker.MultipleLocator(base=yticker_base)
        xloc = ticker.MultipleLocator(base=xticker_base)


        fig = plt.figure(figsize=(10, 10))

        fontP = FontProperties()
        fontP.set_size('small')

        gs = gridspec.GridSpec(2, 2)
                
        kx = dict(aspect='auto')
                
        ax_main = plt.subplot(gs[1, 0], **kx)
        ax_count = plt.subplot(gs[1, 1], **kx)
        ax_vcount = plt.subplot(gs[0, 0], **kx)
        ax_none = plt.subplot(gs[0, 1], **kx)
        ax_small = plt.axes([0.73, 0.11, 0.17, 0.17])
        ax_main.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax_main.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax_count.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax_count.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax_vcount.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax_vcount.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.xticks([])
        plt.yticks([])
        ax_small.yaxis.set_minor_locator(yloc)
        ax_small.yaxis.grid(True, which='minor', color=colors.h_light_gray)
        ax_small.set_axisbelow(True)

        gs.update(wspace=0.00, hspace=-0.00)

        log_marker = 'x'
        if len(opst) > 50:
                if debug > 1:
                        err.log('Input size is ' + str(len(opst)) + ', using marker \'o\'')
                log_marker = 'o'
        elif debug > 1:
                err.log('Input size is ' + str(len(opst)) + ', using marker \'x\'')

        if pages:
                partial_logn = []
                partial_logt = []
                partial_opst = []
                partial_opsn = []
                last_logt_i = 0
                logt_i = 0
                
                for i in range(0, len(opst)):
                        if debug > 1:
                                err.log("Generating data plot number " + str(i))

                        partial_opst = [opst[i]]
                        partial_opsn = [opsn[i]]
                        op_t = opst[i]

                        last_logt_i = logt_i + 1
                        roots = {}
                        while logt_i + 1 < len(logt) and logt[logt_i + 1] <= op_t:
                                logt_i += 1
                                roots[logt[last_logt_i]] = logn[last_logt_i]
        
                        partial_logn = []
                        partial_logt = []
                        for j in range(last_logt_i, logt_i + 1):
                                partial_logt.append(logt[j])
                                partial_logn.append(logn[j])



                        if debug > 1:
                                err.log("Starting plot generation")
        
                        add_plot(fname, cwd, fig, partial_logn, partial_logt,
                                 partial_opsn, partial_opst,
                                 t_counts, n_counts,
                                 t_pairs, n_pairs,
                                 log_marker, xloc, yloc,
                                 ax_main, ax_count, ax_vcount, ax_none, ax_small,
                                 xmax, xmin, ymax, ymin, xrng, 
                                 yrng, xlist, ylist, roots, graphs, i, debug)
                        if len(graphs) > 0:
                                del graphs[0]
        else:
                for i, t in enumerate(logt):
                        if t not in roots.keys():
                                roots[t] = logn[i]

                add_plot(fname, cwd, fig, logn, logt,
                         opsn, opst,
                         t_counts, n_counts,
                         t_pairs, n_pairs,
                         log_marker, xloc, yloc,
                         ax_main, ax_count, ax_vcount, ax_none, ax_small,
                         xmax, xmin, ymax, ymin, xrng,
                         yrng, xlist, ylist, roots, graphs, 0, debug)


        plt.close()
        page_list = []
        page_size = document.paperformat(200, 200)
        
        num_plots = 1
        if pages:
                num_plots = len(opsn)

        for i in range(0, num_plots):

                if debug > 0:
                        err.log("Concatenating PS pages for plot #" + str(i))

                plots_name = cwd + '/../tmp/' + fname + '_' + str(i) + '.eps'
                tree_name = cwd + '/../tmp/' + fname + '_' + str(i) + '.gv.eps'

                got_tree = True
                try:
                        tree_file = open(tree_name, 'r')
                        tree_w = 0
                        tree_h = 0
                        for line in tree_file:
                                if line.startswith("%%BoundingBox:"):
                                        bbline = line.split()
                                        tree_w = bbline[3]
                                        tree_h = bbline[4]
                                        if debug > 1:
                                                err.log("In EPS #{} got height: {} and width {} from line {}".format(i, tree_h, tree_w, line.replace('\n', '')))
                                        break
                        else:
                                err.err("BoundingBox line not found in EPS file for tree diagram.")
                        tree_file.close()
                except:
                        got_tree = False

                c = canvas.canvas()
                plots_file = epsfile.epsfile(0, 0, plots_name, height=160, width=160)

                c.insert(plots_file)

                if got_tree:
                        if tree_w > tree_h:
                                tree_file = epsfile.epsfile(120, 120, tree_name, align='cc', width=70)
                        else:
                                tree_file = epsfile.epsfile(120, 120, tree_name, align='cc', height=70)
        
                        c.insert(tree_file)
                
                p = document.page(c, fittosize=True, centered=True, paperformat=page_size)
                if no_clean:
                        c.writeEPSfile(cwd + '/../tmp/' + fname + '_' + str(i) + '.zipped.eps')

                page_list.append(p)

        d = document.document(page_list)
        out_name = cwd + '/../outputs/' + fname + '.ps'
        if debug > 0:
                err.log("Saving final output " + out_name)
        d.writePSfile(out_name)

        if not no_clean:
                for tmpf in os.listdir(cwd + '/../tmp/'):
                        os.remove(cwd + '/../tmp/' + tmpf)
        
                os.rmdir(cwd + '/../tmp/')


def add_plot(fname, cwd, fig,
             logn, logt, opsn, opst,
             t_counts, n_counts,
             t_pairs, n_pairs,
             log_marker, xloc, yloc,
             ax_main, ax_count, ax_vcount, ax_none, ax_small,
             xmax, xmin, ymax, ymin,
             xrng, yrng,
             xlist, ylist,
             roots,
             graphs, graph_i,
             debug):

                plot_fname = cwd + '/../tmp/' + fname + '_' + str(graph_i) + '.eps'

                if graph_i == 0:

                        pad_xlim = [xmin - 0.05 * xrng, xmax + 0.05 * xrng]
                        pad_ylim = [ymin - 0.05 * yrng, ymax + 0.05 * yrng]
                        ylim = [0, ymax]
                        yloc.view_limits(ymin, ymax)
                        xloc.view_limits(xmin, xmax)

                        if debug > 1:
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

                        if debug > 1:
                                err.log("Set up main plot")


                log = ax_main.scatter([-1] + logn, [-1] + logt, s=1000 / 2 / max(xrng, yrng),
                                      c=[colors.h_light_blue] + [colors.h_light_blue if roots[logt[i]] != logn[i] else colors.h_dark_blue for i in range(0, len(logt))],
                                      marker=log_marker, 
                                      label='Intermediate accesses')

                root_log = ax_main.scatter([-1], [-1], s=1000 / 2 / max(xrng, yrng),
                                      c=colors.h_dark_blue,
                                      marker=log_marker, 
                                      label='Root value at this time')

                if debug > 1:
                        err.log("Plotted Xs")

                ops = ax_main.scatter(opsn, opst, s=1000 / max(xrng, yrng),
                                 c=colors.h_red, 
                                 marker="o", 
                                 label='Operation arguments')

                if debug > 1:
                        err.log("Plotted Os")

                for i, t in enumerate(logt):
                        if (t, logn[i]) not in t_pairs:
                                t_pairs.add((t, logn[i]))
                                t_counts[t - ymin] += 1

                if debug > 1:
                        err.log("Generated y-axis histogram data")

                if graph_i == 0:
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
                        ax_count.xaxis.get_major_ticks()[0].label1.set_visible(False)


                if debug > 1:
                        err.log("Set up y-axis histogram axis")

                hbar = ax_count.barh(ylist, 
                                     t_counts, 
                                     min(yrng, 128) / 128,
                                     align='center',
                                     color=colors.h_dark_blue)

                if debug > 1:
                        err.log("Created y-axis histogram bar chart")

                for i, n in enumerate(logn):
                        if (n, logt[i]) not in n_pairs:
                                n_pairs.add((n, logt[i]))
                                n_counts[int(n) - xmin] += 1

                if debug > 1:
                        err.log("Generated x-axis histogram data")

                if graph_i == 0:
                        ax_vcount.set_ylabel('# Accesses of This Element')
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
                        ax_vcount.yaxis.get_major_ticks()[0].label1.set_visible(False)

                sbar = ax_small.barh(ylist, 
                                     t_counts, 
                                     1,
                                     align='center',
                                     color=colors.h_dark_blue)

                if debug > 1:
                        err.log("Set up x-axis histogram axis")

                vbar = ax_vcount.bar(xlist, 
                                     n_counts, 
                                     min(xrng, 128) / 128,
                                     align='center',
                                     color=colors.h_dark_blue)

                if debug > 1:
                        err.log("Generated y-axis histogram data")
                if graph_i == 0:
                        ax_none.spines['top'].set_visible(False)
                        ax_none.spines['bottom'].set_visible(False)
                        ax_none.spines['right'].set_visible(False)
                        ax_none.spines['left'].set_visible(False)
                        ax_none.set_xticklabels([])
                        ax_none.set_yticklabels([])
                        ax_none.axis('off')

                        ax_main.legend(loc='lower center', bbox_to_anchor=(1, -0.25), ncol=3)


                if debug > 1:
                        err.log("Set up tree image axis")

                if len(graphs) > 0:
                        graph = graphs[0]
                        graph.render(cwd + '/../tmp/' + fname + '_' + str(graph_i) + '.gv')
                        if debug > 0:
                                err.log("Saving intermediary graphviz EPS file #" + str(graph_i))

                if debug > 0:
                        err.log("Saving intermediary matplotlib EPS file #" + str(graph_i))

                plt.savefig(plot_fname, bbox_inches='tight', pad_inches=0.5, format='eps')

                ax_small.patches = []
                ax_count.patches = []
                ax_vcount.patches = []

