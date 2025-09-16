# running the app
import sys                                                  # like command-line arguments, exit) ഉപയോഗിക്കാൻ
from PyQt6.QtWidgets import QApplication , QMessageBox        # QApplication object ഇല്ലാതെ PyQt6 app run ചെയ്യാനാകില്ല.
from app import ExpenseApp                                              # നമുക്ക് മുമ്പ്  ExpenseApp class import ചെയ്യുന്നു.

from database import init_db                                   # data base import


def main():
    app = QApplication(sys.argv)                                                 # sys.argv command-line arguments handle ചെയ്യാൻ. # argv → argument values (argument vector) # sys.argv[0] → ഇപ്പോൾ run ചെയ്യുന്ന python file-ന്റെ പേര്
    
    if not init_db("expense.db"):
        QMessageBox.critical(None, "Error","Could not load your database...")
        sys.exit(1)                                                          # ഇൻഡെന്റേഷൻ ഇല്ല, അതിരുകൾ തെറ്റ്
        

    window = ExpenseApp()
    window.show()                                                           # Window screen-ൽ കാണിക്കാൻ

    sys.exit(app.exec())                                                    # App run loop start ചെയ്ത്, close ചെയ്താൽ system exit command return ചെയ്യുന്നു

if __name__== "__main__":
    main()

    

