import pandas as pd 
import matplotlib
import seaborn as sns
from pathlib import Path

df = pd.read_csv("~/git/libpressio_opt/experiments/threads3.csv")
df = df[df['tolerance'] >= 40]
df['filename'] = df['filename'].map(lambda x: Path(x).stem.replace('_','-'))
single = df[df['config'] == "libpressio+zfp/1"]
multi = df[df['config'] == "libpressio+zfp/10"]
merged = pd.merge(single, multi, on=['tolerance'])
merged['speedup'] = (merged['time:compress_x'] / merged['time:compress_y'])
merged[['tolerance','speedup', 'time:compress_y', 'time:compress_x']]

sns.set_style('whitegrid')
sns.set(font_scale=2.0)
matplotlib.rc('text', usetex=True)
matplotlib.rc('ps', usedistiller='xpdf')
g = sns.catplot(x="tolerance", y="speedup", data=merged, kind="bar", color=sns.color_palette()[0])
g.savefig("/tmp/search_threads.eps")