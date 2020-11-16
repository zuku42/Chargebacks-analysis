import pandas as pd
import sqlite3

from aux_scripts.vector_decorator import vectorize
from aux_scripts.sql_queries import *


class DatabaseQueries:
	"""
	Class with methods that allow for selected queries to the database.
	"""
	def __init__(self, db_name):
		"""
		Initialize connection with the database.
		"""
		self.conn = sqlite3.connect(db_name)
		self.cur = self.conn.cursor()

	def get_chargebacks(self):
		"""
		A DatabaseQueries class method that returns a dataframe containing
		information (transaction id, card id, bank country, ip country, amount, 
		currency) concerning all chargeback transactions.
		"""
		self.cur.execute(TRANS_CB_SQL)
		return pd.DataFrame(self.cur.fetchall())

	def get_cb_cards(self):
		"""
		A DatabaseQueries class method that returns a dataframe cotaining
		information (card id, bank country and ip country) about all credit 
		cards that reported a chargeback.
		"""
		self.cur.execute(CARDS_CB_SQL)
		return pd.DataFrame(self.cur.fetchall())

	def get_transactions(self):
		"""
		A DatabaseQueries class method that returns a dataframe of all 
		transactions that were successfully processed.
		"""
		self.cur.execute(TRANS_SUCC_SQL)
		return pd.DataFrame(self.cur.fetchall())

	def get_non_cb_count(self, card_id):
		"""
		A DatabaseQueries class method that takes a card id as an argument and
		returns a number of non-chargeback transactions that were made with
		this card.
		"""
		self.cur.execute(COUNT_NONCB_SQL, (int(card_id), ))
		return len(self.cur.fetchall())

	def get_cb_count(self, card_id):
		"""
		A DatabaseQueries class method that takes a card id as an argument and 
		returns a number of chargebacks that were filed by this card.
		"""
		self.cur.execute(COUNT_CB_SQL, (int(card_id), ))
		return len(self.cur.fetchall())

	@vectorize
	def get_transaction_id(self, arn, time, card_no):
		"""
		A DatabaseQueries class method that takes ARN, time of transaction and
		masked number of the card the transaction was made with as arguments and 
		returns an id of that transaction.
		"""
		if type(arn) == str: #if arn provided, use it
			self.cur.execute(TRANS_ARN_SQL, (arn, ))
		else:	#otherwise use card id and transaction time
			first_six = card_no[:6]
			last_four = card_no[-4:]
			self.cur.execute(CARDS_NUM_SQL, (first_six, last_four))
			card_id = self.cur.fetchone()[0]
			self.cur.execute(TRANS_INFO_SQL, (int(card_id), time))
		return self.cur.fetchone()[0]

	def update_chargeback(self, transaction_id):
		"""
		A DatabaseQueries class method that takes a transaction id as an
		argument and updates chargeback information in the database record 
		corresponding with that transaction.
		"""
		self.cur.execute(UPDATE_CB, (transaction_id, ))

	def close(self):
		"""
		A DatabaseQueries class method that commits all changes and closes the
		connection with the database.
		"""
		self.conn.commit()
		self.conn.close()
