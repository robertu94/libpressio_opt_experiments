#!/usr/bin/env python

import argparse
import sys
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

sns.set_style('whitegrid')
sns.set(font_scale=1.5)
matplotlib.rc('text', usetex=True)
matplotlib.rc('ps', usedistiller='xpdf')

df = pd.read_csv(args.infile)

df.rename(columns={
    "sz:abs_error_bound": "Absolute Error Bound",
    "error_stat:psnr": "PSNR",
    "pearson:r": "Pearson's Coefficient",
    "size:compression_ratio": "Compression Ratio",
    "ks_test:p_value": "KS Test P Value",
    "composite:objective": "Objective",
    "spatial_error:percent": "Spatial Error \\% $(\\delta = 1e-4)$"
    }, inplace=True)
print(df.describe())

# x is the tick value; p is the position on the axes.


melted = df.melt("Absolute Error Bound")
melted.sort_values('Absolute Error Bound', inplace=True)
melted = melted[melted['variable'] != "Objective"]
'''
plot = sns.relplot(data=melted, x="Absolute Error Bound", y="value", hue="variable", kind="line")
for ax in plot.axes[0]:
    ax.set_xscale('log')
    ax.set_yscale('symlog', linthresh=.05)
    ax.set_ylim(bottom=-0.05)

plt.axhline(y=.05, color=sns.color_palette()[1], linestyle='--') #ks test
plt.axhline(y=5, color=sns.color_palette()[2], linestyle='--') #spatial_error
plt.axhline(y=60, color=sns.color_palette()[3], linestyle='--') #psnr
plt.axhline(y=.99999, color=sns.color_palette()[4], linestyle='--') #pearson
plt.axvline(x=df[df['Objective'] == 0]['Absolute Error Bound'].min(), color='black', label="Objective")

plot.savefig("evaluation.eps")
'''




########################
#
#   New plotting code
#
##########################


# Convert to np arrays
psnr = melted.loc[ melted['variable'] == "PSNR"].to_numpy()
pcc = melted.loc[ melted['variable'] == "Pearson's Coefficient"].to_numpy()
cr = melted.loc[ melted['variable'] == "Compression Ratio"].to_numpy()
ksp = melted.loc[ melted['variable'] == "KS Test P Value"].to_numpy()
s_err= melted.loc[ melted['variable'] == "Spatial Error \\% $(\\delta = 1e-4)$"].to_numpy()



plt.figure(figsize=(8, 10))
plt.subplots_adjust(bottom = 0, hspace=0, wspace=0)
x=df[df['Objective'] == 0]['Absolute Error Bound'].min()


#Compression Ratio
ax1 = plt.subplot(511)
plt.semilogx(cr[:, 0], cr[:,2], label="Compression Ratio", lw=2)
plt.plot([x,x], ax1.get_ylim(), color='k', lw=4)
ax1.legend(loc='lower center',facecolor = 'w')
plt.setp(ax1.get_xticklabels(), visible=False)


#KS Test
ax2 = plt.subplot(512, sharex=ax1)
plt.semilogx(ksp[:,0], ksp[:,2], color=sns.color_palette()[1], label="KS Test P Value", lw=2)
plt.semilogx(ksp[:,0], np.ones(ksp.shape[0])*.05, color=sns.color_palette()[1], linestyle='--', lw=2) #ks test
plt.plot([x,x], ax2.get_ylim(), color='k', lw=4)
ax2.legend(loc='center right',facecolor = 'w')
plt.setp(ax2.get_xticklabels(), visible=False)


#Spatial Error
ax3 = plt.subplot(513, sharex=ax1)
plt.loglog(s_err[:,0], s_err[:,2], color="g", label="Spatial Error \\% $(\\delta = 1e-4)$", lw=2)
plt.loglog(s_err[:,0], np.ones(s_err.shape[0])*5, color=sns.color_palette()[2], linestyle='--', lw=2) #ks test
ax3.set_ylim([1e-7,10])
plt.plot([x,x], ax3.get_ylim(), color='k', lw=4)
ax3.legend(loc='upper center',facecolor = 'w')
plt.setp(ax3.get_xticklabels(), visible=False)


#PSNR
ax4 = plt.subplot(514, sharex=ax1)
plt.semilogx(psnr[:,0], psnr[:,2], color=sns.color_palette()[3], label="PSNR", lw=2)
plt.semilogx(psnr[:,0], np.ones(psnr.shape[0])*60, color=sns.color_palette()[3], linestyle='--', lw=2) #ks test
plt.plot([x,x], ax4.get_ylim(), color='k', lw=4)
ax4.legend(loc='upper right',facecolor = 'w')
plt.setp(ax4.get_xticklabels(), visible=False)


# PCC
ax5 = plt.subplot(515, sharex=ax1)
plt.semilogx(pcc[:,0], pcc[:,2], color=sns.color_palette()[4], label="Pearson's Coefficient", lw=2)
plt.semilogx(pcc[:,0], np.ones(pcc.shape[0])*0.99999, color=sns.color_palette()[4], linestyle='--', lw=2) #ks test
plt.plot([x,x], ax5.get_ylim(), color='k', lw=4)
ax5.set_yticks([0.99999, 1])
ax5.set_yticklabels(["0.99999", "1"])
ax5.legend(loc='center right',facecolor = 'w')


# cleanup the presentation
plt.subplots_adjust(bottom = 0, hspace=0, wspace=0)
plt.xlabel("Absolute Error Bound")
plt.tight_layout()
plt.savefig("evaluation_new.png")
plt.savefig("evaluation_new.eps")

