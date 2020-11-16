"""
In this python script, data about cards, chargeback transactions and all
transactions are loaded from csv files into dataframes and analysed to generate
values that can be later used to draw conclusions about sources of chargebacks.
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

from aux_scripts.file_paths import CSV_CARDS, CSV_CBS, CSV_ALL


#read data from the csv files into corresponding dataframes
cards = pd.read_csv(CSV_CARDS)
chargebacks = pd.read_csv(CSV_CBS)
transactions = pd.read_csv(CSV_ALL)

#number of chargebacks and percentage of chargebacks claimed 
#among all successful transactions
all_cbs_num = len(chargebacks)
all_transactions_num = len(transactions)
ratio = all_cbs_num/all_transactions_num

#histogram data of cards responsible for chargebacks
max_no = cards["Number of cbs"].max()
bins = range(1, max_no + 2)
cards_hist, edges = np.histogram(chargebacks["Card id"].value_counts(), bins=bins)

#count all chargebacks by country (ip)
cb_country_count = chargebacks["IP country"].value_counts(dropna=False)
#count all successful transactions by country (ip)
all_country_count = transactions["IP country"].value_counts(dropna=False)
#create a common dataframe for countries count data
countries_count = pd.DataFrame()
countries_count["All transactions"] = all_country_count.reindex(cb_country_count.index)
countries_count["% transactions"] = [100*count/all_transactions_num for count 
				     in countries_count["All transactions"]]
countries_count["Chargebacks"] = cb_country_count
countries_count["% chargebacks"] = [100*count/all_cbs_num for count 
				    in countries_count["Chargebacks"]]

#number of chargebacks filed from top 4 countries and from the rest of the countries
top_four_countries = [country_name for country_name
					  in countries_count["Chargebacks"].head(4).index]
top_four_cbs = countries_count["Chargebacks"].head(4).sum()
rest_cbs = all_cbs_num - top_four_cbs

#suspicious activity cards
sus_cards = cards[(cards["Number of cbs"] > 1)
				  & (cards["Number of cbs"] > cards["Number of non-cbs"])]
sus_cards_cbs = sus_cards["Number of cbs"].sum()
top_four_sus_cards = sus_cards[sus_cards["IP country"].isin(top_four_countries)]
top_four_sus_cards_cbs = top_four_sus_cards["Number of cbs"].sum()

#countries mismatch cards
mismatch = cards[cards["Countries match?"] == 0]
mismatch_cbs = mismatch["Number of cbs"].sum()
mismatch_all = mismatch_cbs + mismatch["Number of non-cbs"].sum()

#correlation between countries mismatch and chargebacks
correlation = pearsonr(transactions["Countries match?"], transactions["Chargeback?"])


if __name__ == "__main__":
	#if the script is called directly generate this report
	print(f"There has been {all_cbs_num} chargebacks reported. That makes {100*ratio}% of all transactions.")
	print(f"{len(cards)} of cards were responsible for all the chargebacks.")
	print(f"Customers from four countries with the highest number of chargeback were responsible for {top_four_cbs} of chargebacks.")
	print(f"The remaining countries were responsible for {rest_cbs} chargebacks.")
	print(f"{len(sus_cards)} of cards have shown suspicious activity.")
	print(f"They were responsible for {sus_cards_cbs} of chargebacks.")
	print(f"{top_four_sus_cards_cbs} of these chargebacks were made in one of the four countries with the highest number of chargeback files.")
	print(f"There were {len(mismatch)} customers whose ips do not match the country of their banks.")
	print(f"These customers made {mismatch_all} transactions. {mismatch_cbs} of them involved a chargeback file.")
