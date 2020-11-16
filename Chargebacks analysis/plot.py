"""
In this python script, data obtained in the analysis are plotted
using the matplotlib library. Plots are saved in the figures directory.
"""
import numpy as np
import matplotlib.pyplot as plt

from analyse import edges, cards_hist, countries_count, sus_cards
from aux_scripts.file_paths import FIG_ONE, FIG_TWO, FIG_THREE, FIG_FOUR


def set_labels(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
    	height = rect.get_height()
    	plt.text(rect.get_x() + rect.get_width()/2., height+2,'%d' % int(height), 
    							ha='center', va='bottom')


#plot a histogram of the count of cards that reporeted chargebacks
ind = edges[:-1]
width = np.min(np.diff(ind))/2

fig = plt.figure()
bars = plt.bar(ind, cards_hist, width=width, facecolor="midnightblue", 
		edgecolor="black", align="center", zorder=3)
plt.grid(axis="y", linestyle="--", zorder=0)
plt.ylim(top=180)
plt.xlabel("Number of chargebacks", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
set_labels(bars)
plt.savefig(FIG_ONE, transparent=True)

#plot a bar plot of the share in transactions that involved a chargeback
#and the share in all transactions by country (ip)
ind = range(20)
width = np.min(np.diff(ind))/3.

fig = plt.figure()
plt.bar(ind, countries_count.head(20)["% chargebacks"], width=width, 
				  edgecolor="black", facecolor = "navy", zorder=3)
plt.bar(ind+width, countries_count.head(20)["% transactions"], width=width, 
					edgecolor="black", facecolor="cornflowerblue", zorder=2)
plt.grid(axis="y", linestyle="--", zorder=0)
plt.xticks(np.arange(0.5*width, 20, step=3*width), 
			list(countries_count.head(20).index))
plt.xlabel("Countries the transactions were made from", fontsize=12)
plt.ylabel("%age of total transactions", fontsize=12)
plt.legend(["Transactions involving chargebacks","All transactions"])
plt.savefig(FIG_TWO, transparent=True)

#pie charts kwargs
colors = ["#7982B9", "#A5C1DC", "#E9F6FA", "#74BBFB", "lavender"]
labels = ["Panama", "Russia","Turkey", "Thailand", "Other countries"]
explode = 5*[0.1]

#plot pie chart of the ip countries of transactions
#that involved a chargeback
fig = plt.figure()
pie_list = list(countries_count["Chargebacks"].head(4))
rest_sum = countries_count["Chargebacks"][4:].sum()
pie_list.append(rest_sum)
plt.pie(pie_list, colors=colors, labels=labels, explode=explode, autopct='%.2f')
plt.savefig(FIG_THREE, transparent=True)

#plot pie chart of the ip countries of suspicious activity cards
sus_counts = sus_cards["IP country"].value_counts(dropna=False)
pie_list = list(sus_counts.head(4))
rest_sum = sus_counts.iloc[4:].sum()
pie_list.append(rest_sum)
fig = plt.figure()
plt.pie(pie_list, colors=colors, labels=labels, explode=explode, autopct="%.2f")
plt.savefig(FIG_FOUR, transparent=True)
