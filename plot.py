# from pyx import *
# 
# g = graph.graphxy(width=8)
# g.plot(graph.data.file("plot.dat", x=1, y=2))
# g.writePDFfile("plot")
import matplotlib.pyplot as plt
from datetime import datetime


def plot(logn, logt, opsn, opst):
        plt.rcParams["font.family"] = "Input Mono"

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        
        ax1.scatter(logn, logt, s=20, c='b', marker="x", label='intermediate steps')
        ax1.scatter(opsn, opst, s=20, c='r', marker="o", label='operation values')
        plt.savefig('outputs/' + str(datetime.now()) + '.pdf')

