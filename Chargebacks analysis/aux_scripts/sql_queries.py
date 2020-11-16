"""
SQL queries used in the DatabaseQueries class methods.
"""
TRANS_CB_SQL = "SELECT Transactions.Id, Cards.id, Cards.Bin_country,\
		Customers.ip_country\
		FROM Transactions\
		JOIN Cards ON Transactions.card_id=Cards.id\
		JOIN Customers ON Customers.Card_id=Transactions.card_id\
		AND cb=1"
CARDS_CB_SQL = "SELECT Cards.Id, Cards.Bin_country, Customers.ip_country\
		FROM Cards\
		JOIN Customers ON Customers.Card_id=Cards.Id\
		JOIN Transactions ON Transactions.cb=1\
		AND Transactions.card_id=Cards.Id"
TRANS_SUCC_SQL = "SELECT Transactions.Id, Cards.Bin_country,\
		  Customers.ip_country, Transactions.cb\
		  FROM Transactions\
		  JOIN Cards on Transactions.card_id=Cards.id\
		  JOIN Customers ON Customers.Card_id=Transactions.card_id\
		  AND succes=1"
COUNT_NONCB_SQL = "SELECT * FROM Transactions WHERE cb=0 AND succes=1 AND card_id=?"
COUNT_CB_SQL = "SELECT * FROM Transactions WHERE cb=1 AND card_id=?"
CARDS_NUM_SQL = "SELECT Id FROM Cards WHERE bin=? AND Last_4=?"
TRANS_ARN_SQL = "SELECT Id FROM Transactions WHERE acq_tid=?"
TRANS_INFO_SQL = "SELECT Id FROM Transactions WHERE card_id=? AND Created_at=?"
UPDATE_CB = "UPDATE Transactions SET cb=1 WHERE Id=?"
