"""
This python script is responsible for loading relevant data from the database, 
and generating dataframes with information about cards, chargeback transactions, 
and all transactions. The dataframes are exported as csv files so that they can be
later analysed.
"""
import pandas as pd
import numpy as np

from db_class import DatabaseQueries
from aux_scripts.file_paths import DB_PATH, CSV_CARDS, CSV_CBS, CSV_ALL


def check_equal(list1, list2):
	"""
	Check if corresponding values of two lists are equal to each other.
	"""
	return np.where([item1 == item2 for item1, item2 
			 in zip(list1, list2)], 1, 0)


#create a DatabaseQueries instance
db = DatabaseQueries(DB_PATH)

#load information about cards that filed a chargeback from the datatabase
cards = db.get_cb_cards().drop_duplicates()
cards.columns = ["Card id", "Bank country", "IP country"]
#check if bank country and IP country are the same
cards["Countries match?"] = check_equal(cards["Bank country"], cards["IP country"])
#count chargebacks and successful non-chargeback transactions made with each card
cards["Number of cbs"] = cards["Card id"].apply(db.get_cb_count)
cards["Number of non-cbs"] = cards["Card id"].apply(db.get_non_cb_count)

#load information about chargebacks from the database
chargebacks = db.get_chargebacks()
chargebacks.columns = ["Transaction id", "Card id", "Bank country", "IP country"]

#load information about all successful transactions from the database
transactions = db.get_transactions()
transactions.columns = ["Transaction id", "Bank country", "IP country", 
							 "Chargeback?"]
#check if bank country and ip country are the same
transactions["Countries match?"] = check_equal(transactions["Bank country"], 
						 transactions["IP country"])

#save dataframes to csv files
cards.to_csv(CSV_CARDS)
chargebacks.to_csv(CSV_CBS)
transactions.to_csv(CSV_ALL)



