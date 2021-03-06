#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# matplotlib/seaborn font garbage
import matplotlib.font_manager as fm
font0 = fm.FontProperties()
font0.set_family("monospace")
font0.set_name("M+ 1mn")
font0.set_weight("medium")

import seaborn as sns
sns.set_style("whitegrid", {'grid.linestyle': ':'})
sns.plt.rcParams.update({'mathtext.fontset' : 'custom',
                         'mathtext.rm' : 'Bitstream Vera Sans',
                         'mathtext.it' : 'Bitstream Vera Sans:italic',
                         'mathtext.bf' : 'Bitstream Vera Sans:bold',
                         'mathtext.bf' : 'Bitstream Vera Sans:bold',
                         'mathtext.tt' : 'mononoki',
                         'mathtext.cal' : 'MathJax_Caligraphic'})
#sns.set_palette("Set2")
sns.set_palette(sns.color_palette("cubehelix", 6))


import datetime
import time

import collections
from collections import OrderedDict


from functools import partial

import pprint
pp = pprint.PrettyPrinter(indent=2)
"""
import json

import collections
from collections import OrderedDict
from collections import defaultdict

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

import numpy as np
import scipy as sp
import scipy.stats

def ci(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return h 

import re
def trailing_num(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else None

################################################################################

def ndigits(num):
    return len(str(num))

def swparse(fname, tag):
    tdata = {}
    with open(fname, "r") as sw:
        while True:
            line1 = sw.readline().rstrip()
            line2 = sw.readline().rstrip()
            if not line1 or not line2:
                break
            name1 = line1.split(':')[0]
            info1 = line1.split(',')[1:]
            name2 = line2.split(':')[0]
            info2 = line2.split(',')[1:]
            tdata[tag] = (name1, info1, name2, info2)
    return tdata

for i in range(8):
    si = str(i)
    tdata = swparse("seriesdata_" + si + ".log", si)
    print(tdata[si][0] + " " + str(tdata[si][1]))
    print(tdata[si][2] + " " + str(tdata[si][3]))
    plt.plot(tdata[si][1], tdata[si][3])
plt.savefig("zest-s.png")
plt.close()
"""

def tparse(fname, tag):
    tdata = {}
    with open(fname, "r") as timings:
        for timing in timings:
            timing = timing.rstrip()
            if not timing:
                continue
            tkeyvals = timing.split(',')
            tname = tkeyvals[0].split(':')[1]
            if tname+tag not in tdata:
                tdata[tname+tag] = {}
            for keyval in tkeyvals:
                tdatapair = keyval.split(':')
                if tdatapair[0] == "name":
                    continue
                if tdatapair[0] not in tdata[tname+tag]:
                    tdata[tname+tag][tdatapair[0]] = []
                tdata[tname+tag][tdatapair[0]] += [tdatapair[1]]
    return tdata
fdata = sorted(tparse("durs_mean.log", "").items())
print(json.dumps(fdata, indent=2))

bar_width = 0.8

def var_to_ci(x,n):
#    return np.sqrt(x)
    return np.sqrt(x)/np.sqrt(n)*1.96

index = range(len(fdata)/2)
print index
y1vals = defaultdict(list)
y1errs = defaultdict(list)
y2vals = defaultdict(list)
y2errs = defaultdict(list)
for k,v in fdata:
    print k
    if len(v["avg"]) > 1:
        print len(v["avg"])
    col = trailing_num(k)
    if ("splt" in k):
        y1vals[col] += [np.mean(map(float,v["avg"]))]
        y1errs[col] += [np.sqrt(np.sum(np.square(map(var_to_ci, map(float,v["var"]), map(float,v["its"]))), axis=0))]
    elif ("rslv" in k):
        y2vals[col] += [np.mean(map(float,v["avg"]))]
        y2errs[col] += [np.sqrt(np.sum(np.square(map(var_to_ci, map(float,v["var"]), map(float,v["its"]))), axis=0))/len(v["var"])]
    else:
        print("Bad key")

i = 0
scales = [386.468/200, 1585.95/200, 45.51625]
colors = ['r','g','b']
errorc = {'ecolor': '0.3'}
fig, axes = plt.subplots(2, 1, gridspec_kw = {'height_ratios':[1, 2]})
p2, p1 = axes
for k in sorted(y1vals.keys()):
    print len(y1vals[k])
    xvals = range(0, len(y1vals[k])*len(y1vals), len(y1vals))
    xvals = [x/3 + bar_width/3*i+0.1 for x in xvals]
    p1.bar(xvals, np.array(y1vals[k])/scales[i], bar_width/3, yerr=np.array(y1errs[k])/scales[i], color=colors[i], error_kw=errorc, label='step runtime')
    p2.bar(xvals, np.array(y2vals[k])/scales[i], bar_width/3, yerr=np.array(y2errs[k])/scales[i], color=colors[i], error_kw=errorc, label='resolution runtime')
    #p1.bar(xvals, y1vals[k], bar_width, yerr=y1errs[k], color=colors[i], error_kw=errorc, label='step runtime')
    #p2.bar(xvals, y2vals[k], bar_width, yerr=y2errs[k], color=colors[i], error_kw=errorc, label='resolution runtime')
    i += 1
for i in range(5):
    p1.plot([i,i+1], [72.4935/45.51625/(2**i), 72.4935/45.51625/(2**i)], color = 'b')
#plt.setp(axes,
#         xticks = [x*3 + bar_width*1.5 for x in range(len(fdata)/6)],
#         xticklabels = [str(x) for x in range(1,(len(fdata)/6+1))])
plt.setp(axes,
         xticks = [x + 0.5 for x in range(len(xvals))],
         xticklabels = [str(2**x) for x in range((len(xvals)))])
plt.xlabel("processor ID")
plt.ylabel("CPU time (ms)")
plt.suptitle("Load Balance of step and resolutions across threads")
#plt.legend((p1[0], p2[0]), ("step", "resolution"))
plt.savefig("aest.png")
plt.close()
"""

"""
# get data from File
def get_fdata(bench, proc_set, size_set, bpsz_set, curve_type):
    fdata = {}
    for proc in proc_set:
        for size in size_set:
            for bpsz in bpsz_set:
                fname = fname_tmpl.format(bench, proc, size, bpsz)
                if curve_type == "proc":
                    tag = str(proc)
                    pad = max(map(ndigits, proc_set))
                elif curve_type == "size":
                    tag = str(size)
                    pad = max(map(ndigits, size_set))
                elif curve_type == "bpsz":
                    tag = str(bpsz)
                    pad = max(map(ndigits, bpsz_set))
                fdata[fname] = tparse(fname, tag.zfill(pad))
                for impl in fdata[fname]:
                    # possible x axes units
                    fdata[fname][impl]["proc"] = proc
                    fdata[fname][impl]["size"] = size
                    fdata[fname][impl]["bpsz"] = bpsz

    print(json.dumps(fdata, indent=2))
    return fdata

# make data for Plot
def make_pdata(fdata, stat_type, x_axis):
    pdata = {}
    for lkey, log in fdata.items():
        for key, stat_set in log.items():
            if key not in pdata:
                pdata[key] = [];
            for i in stat_set:
                if i == stat_type:
                    pdata[key] += [ (stat_set[x_axis], float(stat_set[i])) ]
    for pkey in pdata:
        pdata[pkey] = sorted(pdata[pkey])
    return pdata

def rpvs(pkey, size):
    return str(size) in pkey
def rpvs_all(pkey):
    return "cont" in pkey
def fpvs_all(pkey):
    return "cont" in pkey
def hpvs_all(pkey):
    return "cont" in pkey
def rsvt(pkey):
    return "4" in pkey
def svt(pkey):
    return True
def fbvs(pkey):
    return "cont006291456" in pkey

selector = {
    "reduce_size-v-time": rsvt,
    "reduce_procs-v-speed-s": partial(rpvs, size=2**19 * 3),
    "reduce_procs-v-speed-m": partial(rpvs, size=2**21 * 3),
    "reduce_procs-v-speed-l": partial(rpvs, size=2**23 * 3),
    "reduce_procs-v-speed-a": rpvs_all,
    "foreach_size-v-time": svt,
    "foreach_procs-v-speed-a": fpvs_all,
    "foreach_bpbits-v-speed": fbvs,
    "heat_size-v-time": svt,
    "heat_width-v-speed-a": hpvs_all,
    "heat_steps-v-speed-a": hpvs_all
}
        

################################################################################

# filename path/template
date = "2016-09-19"
log_path = "logs_" + date
fname_tmpl = log_path + "/{0:s}_{1:d}_{2:d}_{3:d}.log"

# key of dispatch table, etc
#bench_name = "reduce_size-v-time"
#bench_name = "reduce_procs-v-speed-s"
#bench_name = "reduce_procs-v-speed-m"
#bench_name = "reduce_procs-v-speed-l"
bench_name = "reduce_procs-v-speed-a"
#bench_name = "foreach_size-v-time"
#bench_name = "foreach_procs-v-speed-a"
#bench_name = "foreach_bpbits-v-speed"
#bench_name = "heat_size-v-time"
#bench_name = "heat_width-v-speed-a"
#bench_name = "heat_steps-v-speed-a"
if "reduce" in bench_name:
    test_name = "reduce"
    op = "+"
elif "foreach" in bench_name:
    test_name = "foreach"
    op = "*"
elif "heat" in bench_name:
    test_name = "heat"
    op = "stencil"

if "procs-v-speed" in bench_name:
    curve_type = "size"
    x_axis = "proc"
elif "size-v-time" in bench_name:
    curve_type = "proc"
    x_axis = "size"
elif "bpsz-v-speed" in bench_name:
    curve_type = "size"
    x_axis = "bpsz"
if "width-v-speed" in bench_name:
    curve_type = "size"
    x_axis = "proc"
if "steps-v-speed" in bench_name:
    curve_type = "bpsz"
    x_axis = "proc"

# name of saved file
graph_name = "graphs_" + date + "/" + bench_name

# processor counts
proc_set = [1, 2, 4]
proc_val = 4
procs = proc_set

# vector sizes
size_set = map(lambda x: x * (2**15 * 3), [2**0, 2**2, 2**4, 2**6, 2**8, 2**10])
size_val_s = 2**19 * 3
size_val_m = 2**21 * 3
size_val_l = 2**23 * 3
if "procs-v-speed-a" in bench_name:
    sizes = size_set
elif bench_name == "reduce_procs-v-speed-s":
    sizes = [size_val_s]
elif bench_name == "reduce_procs-v-speed-m":
    sizes = [size_val_m]
elif bench_name == "reduce_procs-v-speed-l":
    sizes = [size_val_l]
elif "size-v-time" in bench_name:
    sizes = size_set
else:
    sizes = [size_val_m]

# bit partition sizes
bpsz_set = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
bpsz_val = 10
if bench_name == "foreach_bpbits-v-speed":
    bpszs = bpsz_set
else:
    bpszs = [bpsz_val]

r_set = [3, 11, 21, 101, 201, 1000]
r_val = 1000

c_set = [7801, 31240, 125001, 500000, 2000001, 8000000]
c_val = 8000000

# unresolved depth values (unused as of now)
unre_set = [2**0, 2**1, 2**2, 2**3, 2**4, 2**5, 2**6]
unre_val = 8


################################################################################

# file data
print("Reading data from disk...")
if "reduce" in test_name or "foreach" in test_name:
    fdata = get_fdata(test_name, procs, sizes, bpszs, curve_type)
elif "heat_size" in bench_name:
    fdata = get_fdata(test_name, procs, c_set, [r_val], curve_type)
elif "heat_width" in bench_name:
    fdata = get_fdata(test_name, procs, c_set, [r_val], curve_type)
elif "heat_steps" in bench_name:
    fdata = get_fdata(test_name, procs, [c_val], r_set, curve_type)

# plot data
print("Importing data...")
pdata = make_pdata(fdata, "min", x_axis)
pp.pprint(pdata)
pdata = { k: zip(*v) for k,v in pdata.items() }

for k,v in pdata.items():
    print (k,v)

def keysort(s):
    if True:
        keyorder = {k:v for v,k in enumerate(["seq", "vec", "cont", "async", "omp"])}
        for k,v in keyorder.items():
            if k in s[0]:
                print "AH HA",k,s[0],v
                print v*5+int("0" + "".join(i for i in s[0] if i.isdigit()))
                return v*5+int("0" + "".join(i for i in s[0] if i.isdigit()))
        return len(keyorder)
#   elif "foreach" in s[0]:
#       keyorder = OrderedDict({k:v for v,k in enumerate(["stdv_foreach01", "cont_foreach01", "2", "4", "8", "16"])})
#       for k,v in keyorder.items():
#           if k in s[0]:
#               print k,s[0]
#               return v
#       return len(keyorder)
#   elif "heat" in s[0]:
#       keyorder = OrderedDict({k:v for v,k in enumerate(["stdv_heat1", "cont_heat1", "2", "4", "8", "16"])})
#       for k,v in keyorder.items():
#           if k in s[0]:
#               print k,s[0]
#               return v
#       return len(keyorder)

    print s[0]
    return s[0]

pdata = OrderedDict(sorted(pdata.items(), key=keysort))

# plotting
print("Plotting data...")
figtext = ''
if "-v-speed" in bench_name:
    for pkey, pvals in pdata.items():
        if not selector[bench_name](pkey):
            continue
        plab = "".join(i for i in pkey if not i.isdigit())
        if "cont" in plab:
            plab = "cont"
        elif "stdv" in plab:
            plab = "stdv"
        ptag = "".join(i for i in pkey if i.isdigit())
        if "procs" in bench_name:
            plab += ", " + ptag.lstrip("0") + " elements"
        elif "width" in bench_name:
            plab += ", " + ptag.lstrip("0") + " spatial points"
        elif "steps" in bench_name:
            plab += ", " + ptag.lstrip("0") + " timesteps"
        if "reduce" in bench_name:
            baseline = pdata["vec" + ptag][1][0]
        elif "foreach" in bench_name:
            baseline = pdata["stdv_foreach" + ptag][1][0]
        elif "heat" in bench_name:
            baseline = pdata["stdv_heat" + ptag][1][0]
        if (("seq" in pkey or "vec" in pkey) and "1" in pkey):
            sns.plt.axhline(pvals[1][0] / baseline, color='#777777', linestyle='-', label=plab)
        else:
            sns.plt.plot(pvals[0], [y / baseline for y in pvals[1]], marker='d', label=plab)

    handles, labels = sns.plt.gca().get_legend_handles_labels()
    labels, handles = zip(*zip(labels, handles))
    leg = sns.plt.legend(handles, labels, loc='upper right', fancybox=True, frameon=True, prop=font0)
    leg.get_frame().set_alpha(1.0)
    sns.plt.xlim(1, 4)
    if "reduce" in bench_name:
        sns.plt.ylim(0.4, 1.2)
    elif "foreach" in bench_name:
        sns.plt.ylim(0.3, 1.5)
    sns.plt.title('Scaling (' + test_name + ' with ' + op + ')')
    sns.plt.xlabel('# threads')
    sns.plt.ylabel('relative speedup')
    sns.plt.xticks(proc_set)
    figtext = 'bench: ' + test_name + ', branching factor: 10'
    if "width" in bench_name:
        figtext += ", " + str(r_val) + " timesteps"
        #sns.plt.ylim(0.0, 4.5)
    if "steps" in bench_name:
        figtext += ", " + str(c_val) + " spatial points"
        #sns.plt.ylim(0.0, 1.6)
elif "size-v-time" in bench_name:
    for pkey, pvals in pdata.items():
        if not selector[bench_name](pkey):
            print pkey
            continue
        plab = "".join(i for i in pkey if not i.isdigit())
        if "cont" in plab:
            plab = "cont"
        elif "stdv" in plab:
            plab = "stdv"
            if "1" not in pkey or "16" in pkey:
                continue
        ptag = "".join(i for i in pkey if i.isdigit())
        plab += ", " + ptag.strip("0") + " procs"
        print plab, pvals
        sns.plt.plot(pvals[0], pvals[1], marker='d', label=plab)

    handles, labels = sns.plt.gca().get_legend_handles_labels()
    labels, handles = zip(*zip(labels, handles))
    leg = sns.plt.legend(handles, labels, loc='upper left', fancybox=True, frameon=True, prop=font0)
    leg.get_frame().set_alpha(1.0)
    if "reduce" in bench_name:
        sns.plt.ylim(0.02, 100)
    elif "foreach" in bench_name:
        sns.plt.ylim(0.18, 1000)
    elif "heat" in bench_name:
        sns.plt.xlim(2**12.5, 2**23.5)
    sns.plt.xscale('log', basex=2)
    sns.plt.yscale('log', basey=10)
    sns.plt.title('Runtime (' + test_name + ' with ' + op + ')')
    sns.plt.xlabel('# elements')
    sns.plt.ylabel('time (ms)')
    figtext = 'bench: ' + test_name + ', branching factor: 10'
    if "heat" in bench_name:
        figtext += ", " + str(c_val) + " spatial points"
        figtext += ", " + str(r_val) + " timesteps"
elif "bpsz-v-speed" in bench_name:
    for pkey, pvals in pdata.items():
        if not selector[bench_name](pkey):
            print pkey
            continue
        plab = "".join(i for i in pkey if not i.isdigit())
        print plab
        if "cont" in plab:
            plab = "cont"
        elif "stdv" in plab:
            plab = "stdv"
        ptag = "".join(i for i in pkey if i.isdigit())
        plab += ", " + ptag.strip("0") + " procs"
        sns.plt.plot(pvals[0], pvals[1], marker='d', label=plab)

    handles, labels = sns.plt.gca().get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: len(t[0])))
    leg = sns.plt.legend(handles, labels, loc='upper left', fancybox=True, frameon=True, prop=font0)
    leg.get_frame().set_alpha(1.0)
    if "reduce" in bench_name:
        sns.plt.ylim(0.02, 150)
    elif "foreach" in bench_name:
        sns.plt.ylim(0.18, 1000)
    sns.plt.xscale('log', basex=2)
    sns.plt.yscale('log', basey=10)
    sns.plt.title('Runtime (' + test_name + ' with ' + op + ')')
    sns.plt.xlabel('# elements')
    sns.plt.ylabel('time (ms)')
    figtext = 'bench: ' + test_name + ', branching factor: 10'


# old options
#sns.plt.ylim(0.35, 1.75)
#sns.plt.xlim(0, 16)
#sns.plt.gca().xaxis.grid(False)
#sns.plt.gca().yaxis.set_major_locator(mpl.ticker.MultipleLocator(0.25))
#sns.plt.xticks(range(0, 16))

# 2
#sns.plt.title('Effect of BP_SIZE on runtime')
#sns.plt.xlabel(r'BP_SIZE ($\log_2~$of branches/node)')
#sns.plt.ylabel('relative speedup')
#t = sns.plt.figtext(0.512, 0.12, 'bench: foreach, #elements: 6291456, #threads: 4',
#                    fontsize=10, fontproperties=font0, ha='center')

t = sns.plt.figtext(0.512, 0.12, figtext, fontsize=10, fontproperties=font0,
                    ha='center')
t.set_bbox(dict(color='white', alpha=1.0, edgecolor='grey'))

print("Saving plot...")
sns.plt.savefig(graph_name + ".png")
sns.plt.close()

# plotting
sns.plt.axhline(1, color='#777777', linestyle='-', label="std::vector<double>")
    if (("seq" in pkey or "vec" in pkey) and "1" in pkey) or \
       (("seq" not in pkey and "vec" not in pkey) and "4" in pkey):
        plabel = "".join(i for i in pkey if not i.isdigit())
        if "seq" not in pkey and "vec" not in pkey:
            if "avx" in pkey:
                ptag = "256 bits"
            elif "omp" in pkey:
                ptag = "4 cores"
            else:
                ptag = "".join(i for i in pkey if i.isdigit()) + " threads"
            plabel += ", " + ptag
        pvals.sort()
        sns.plt.plot(size_set, pvals, marker='d', label=plabel)
    if (("stdv" in pkey) and "4" in pkey) or \
        ("stdv" not in pkey):
        if "stdv" in pkey:
            plabel = "std::vector<double>"
        elif "cont" in pkey:
            ptag = ''.join(i for i in pkey if i.isdigit())
            plabel = "cts::ctvector<double>, threads=" + ptag
        pvals.sort()
        sns.plt.plot(size_set, pvals, marker='d', label=plabel)
"""
