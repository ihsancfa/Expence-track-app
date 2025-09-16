# All sql 

# All SQL stuff here
from PyQt6.QtSql import QSqlDatabase, QSqlQuery



def init_db(db_name):                                   # init_db എന്നൊരു ഫങ്ഷൻ
    database = QSqlDatabase.addDatabase("QSQLITE")    # സൃഷ്ടിക്കാനോ ഉപയോഗിക്കാനോ പോകുന്ന ഡാറ്റാബേസ് ഫയലിന്റെ പേര് (ഉദാ: expenses.db).
    database.setDatabaseName(db_name)                 # QSqlDatabase ക്ലാസ് ഉപയോഗിച്ച് ഒരു SQLite ഡാറ്റാബേസ് കണക്ഷൻ സൃഷ്ടിക്കുന്നു. # QSQLITE" → SQLite ഡാറ്റാബേസ് എൻജിൻ
                                                        # ഡാറ്റാബേസ് ഫയലിന്റെ പേര് / പാത്ത് സജ്ജീകരിക്കുന്നു. ഉദാ: "expenses.db" എന്ന് കൊടുത്താൽ, അതേ ഡയറക്ടറിയിൽ expenses.db എന്നൊരു ഫയൽ ഉണ്ടാകും.
    
    
    if not database.open():                               # ഒന്നും തുറക്കാൻ കഴിഞ്ഞില്ലെങ്കിൽ
        return False 
    
    query = QSqlQuery()                           # SQL query പ്രവർത്തിപ്പിക്കാനായി QSqlQuery ഒബ്ജക്റ്റ് സൃഷ്ടിക്കുന്നു.
                                                  # ശരിയായ SQL query സ്ട്രിംഗ്  # ഇവിടെ SQL query പ്രവർത്തിപ്പിക്കുന്നു
    success = query.exec("""
        CREATE TABLE IF NOT EXISTS expenses (    
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
                    """)  
    return success                                   # query യഥാർത്ഥത്തിൽ വിജയിച്ചോ എന്ന് റിട്ടേൺ ചെയ്യുന്നു                         
                                                 # CREATE TABLE IF NOT EXISTS → expenses എന്നൊരു ടേബിൾ ഇല്ലെങ്കിൽ, പുതിയത് ഉണ്ടാക്കുക.
                                                    # id column → auto-increment primary key (ഓരോ റെക്കോർഡിനും unique നമ്പർ).
                                                    # date TEXT ചെലവിന്റെ തീയതി (string ആയി save ചെയ്യുന്നു).
                                                    # category TEXT → ചെലവിന്റെ വിഭാഗം (ഉദാ: "Food", "Transport").
                                                    # amount REAL → ചെലവിന്റെ തുക (floating number).
                                                    # description TEXT → ചെലവിനെ കുറിച്ചുള്ള വിശദീകരണം (optional text).

    


def fetch_expenses():
    query = QSqlQuery("SELECT * FROM expenses ORDER BY date DESC")
    expenses = []
    while query.next():
        row = [query.value(i) for i in range(5)]
        expenses.append(row)
    return expenses

def add_expenses (date,category,amount,description):
    query = QSqlQuery()
    query.prepare(""" 
                  INSERT INTO expenses (date,category,amount,description) 
                  VALUES (?,?,?,?)
                  """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    return query.exec()

def delete_expenses(expense_id):
    query = QSqlQuery()
    query.prepare("DELETE FROM expenses WHERE id =?")
    query.addBindValue(expense_id)
    return query.exec()