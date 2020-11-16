"""
This python script links two sources of data concerning credit card transactions
with each other. It uses data about reported chargebacks stored in the Excel 
file to update relevant records of the sqlite database (cb column of the
Transactions table).  
"""
import pandas as pd

from aux_scripts.file_paths import DB_PATH, EXCEL_PATH
from db_class import DatabaseQueries


#create DatabaseQueries instance
cards_db = DatabaseQueries(DB_PATH)

#load data concerning chargebacks from the excel file into a dataframe,
chargebacks_df = pd.concat(pd.read_excel(EXCEL_PATH, sheet_name=None), 
					ignore_index=True, sort=False)

#add transaction id column to the dataframe
chargebacks_df["Transaction id"] = cards_db.get_transaction_id(chargebacks_df["ARN"], 
			chargebacks_df["Transaction Datetime"], chargebacks_df["Masked CCN"])

#update the database with information about chargebacks
chargebacks_df["Transaction id"].apply(cards_db.update_chargeback)

#commit changes and close the database
cards_db.close()
