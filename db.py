import sqlite3

class SalesDb:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Sales (id INTEGER PRIMARY KEY, SellerName text, CustomerName text, SaleDate text, SaleItemName text, SaleValue float)")
        self.conn.commit()
    
    def GetAllSales(self):
        self.cur.execute('''SELECT Sales.id, SaleDate, Sellers.SellerName as SellerName, CustomerName, SaleItemName, printf("%.2f", SaleValue) as SaleValue 
                            FROM Sales
                            JOIN Sellers ON Sales.SellerId = Sellers.id
                            ORDER BY SaleDate DESC''')
        rows = self.cur.fetchall()
        return rows
    
    def GetSellers(self):
        self.cur.execute('SELECT * FROM Sellers')
        rows = self.cur.fetchall()
        return rows
    
    def GetMainSales(self):
        self.cur.execute('''SELECT DISTINCT Sellers.SellerName as SellerName, printf("%.2f", sum(SaleValue)) as TotalValue
                            FROM Sales
                            JOIN Sellers ON Sales.SellerId = Sellers.id
                            GROUP BY SellerName
                            ORDER BY sum(SaleValue) DESC''')
        rows = self.cur.fetchall()
        return rows

    def InsertSale(self, SaleDate, SellerId, CustomerName, SaleItemName, SaleValue):
        self.cur.execute("INSERT INTO Sales VALUES (NULL, ?, ?, ?, ?, ?)", (SellerId, CustomerName, SaleDate, SaleItemName, SaleValue))
        self.conn.commit()
        
    def RemoveSale(self, id):
        self.cur.execute("DELETE FROM Sales WHERE id=?", (id,))
        self.conn.commit()
        
    def UpdateSale(self, id, SaleDate, SellerId, CustomerName, SaleItemName, SaleValue):
        self.cur.execute("UPDATE Sales SET SellerId = ?, CustomerName = ?, SaleDate = ?, SaleItemName = ?, SaleValue = ? WHERE id = ?", (SellerId, CustomerName, SaleDate, SaleItemName, SaleValue, id))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()
        
# class InitDb:
#     def __init__(self, db):
#         self.conn = sqlite3.connect(db)
#         self.cur = self.conn.cursor()
#         self.cur.execute('''CREATE TABLE "Sales" (
#                             "id"	INTEGER,
#                             "SellerId"	INTEGER NOT NULL,
#                             "CustomerName"	TEXT NOT NULL,
#                             "SaleDate"	TEXT NOT NULL,
#                             "SaleItemName"	TEXT NOT NULL,
#                             "SaleValue"	FLOAT NOT NULL,
#                             FOREIGN KEY("SellerId") REFERENCES "Sellers"("id"),
#                             PRIMARY KEY("id" AUTOINCREMENT)''')
#         self.conn.commit()