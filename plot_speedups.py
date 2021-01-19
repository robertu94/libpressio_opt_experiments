import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

df = pd.read_csv("~/git/libpressio_opt/experiments/early-2020-10-16.csv")
sz = df[['time:compress', 'filename', 'config','tolerance']]
sz1 = sz[sz['config'] == 'libpressio+sz+early=1']
sz2 = sz[sz['config'] == 'libpressio+sz+early=0']
merged = pd.merge(sz1,sz2, on=['filename', 'tolerance'])
merged['difference'] = (merged['time:compress_y']) / merged['time:compress_x']
mgard = df[['time:compress', 'filename', 'config','tolerance']]
mgard1 = mgard[mgard['config'] == 'libpressio+mgard+early=1']
mgard2 = mgard[mgard['config'] == 'libpressio+mgard+early=0']
merged2 = pd.merge(mgard1,mgard2, on=['filename', 'tolerance'])
merged2['difference'] = (merged2['time:compress_y']  / merged2['time:compress_x'] )
m = pd.concat([merged,merged2])
m.rename(columns={"config_x": "configuration"}, inplace=True)
m['filename'] = m['filename'].map(lambda x: str(Path(x).stem).replace('_','-'))
m = m[m['tolerance'] >= 40]

print(m)

sns.set_style('whitegrid')
sns.set(font_scale=2.0)
matplotlib.rc('text', usetex=True)
matplotlib.rc('ps', usedistiller='xpdf')
g = sns.catplot(data=m, x="tolerance", y="difference", hue="configuration", col="filename", kind="bar")
for ax in g.axes[0]:
    ax.yaxis.grid(True, which='minor')
    ax.yaxis.set_minor_locator(plt.MaxNLocator(16))
    ax.yaxis.set_major_locator(plt.MaxNLocator(4))
g.set_ylabels("speedup")
g.savefig("/tmp/inter-speedup.png")
g.savefig("/tmp/inter-speedup.eps")
