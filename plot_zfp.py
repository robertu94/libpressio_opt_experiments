import seaborn as sns
import pandas as pd
import matplotlib


sns.set_style('whitegrid')
sns.set(font_scale=1.5)
matplotlib.rc('text', usetex=True)
matplotlib.rc('ps', usedistiller='xpdf')

df = pd.read_csv("zfp-threads.csv")
df.rename(columns={
            "zfp:omp_threads": "Number of Threads",
            "time:compress": "Compression Time (ms)"
        }, inplace=True)
g = sns.boxplot(data=df, x="Number of Threads", y="Compression Time (ms)", color=sns.color_palette()[0])
fig = g.get_figure()
fig.tight_layout()
fig.savefig("zfp_threads.eps")

