# App desigh 
# Install first (already done)
# pip install PyQt6

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QComboBox, # PyQt6-ൽ നിന്നും വേണ്ട UI ക്ലാസ്സുകൾ import ചെയ്യുന്നു
    QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout,
    QMessageBox, QTableWidgetItem, QHeaderView
)

from PyQt6.QtCore import QDate, Qt # തീയതി (Date) കൈകാര്യം ചെയ്യാനും alignment/flags (Qt) ഉപയോഗിക്കാനും
from database import fetch_expenses,add_expenses,delete_expenses

class ExpenseApp(QWidget): #ExpenseApp എന്നൊരു ക്ലാസ് ഉണ്ടാക്കുന്നു. ഇത് QWidget inherit ചെയ്യുന്നു. അതായത്, നമ്മുടെ Expense App basically ഒരു window ആകും
    def __init__(self): # ExpenseApp ഇപ്പോൾ QWidget-ന്റെ എല്ലാ properties (window ഉണ്ടാക്കാൻ, resize ചെയ്യാൻ, close button, background, layout support തുടങ്ങിയവ) use ചെയ്യാം.
        super().__init__() #ഇത് കൊടുക്കാതിരുന്നാൽ ചില window features properly initialize ആകില്ല. #QWidget → Base window frame പോലെ, അതിൽ നമ്മൾ button, textbox, labels, മുതലായവ ചേർക്കാം.
        self.initUI() # ആദ്യം UI create ചെയ്യുക # ശേഷം settings + load_table_data
        self.settings() # Constructor-ൽ തന്നെ, app-ന്റെ settings load ചെയ്യുന്നു. (Window size, title etc.)
        

    def settings(self):
        self.setGeometry(750,300,550,500) # Window-ന്റെ സ്ഥാനം (position) screen position x,y+ വലുപ്പം (size) fix ചെയ്യുന്നു.
        self.setWindowTitle("Expense Tracker App") # Window-ന്റെ മുകളിൽ കാണുന്ന title bar name 
        self.load_table_data()


    # Design

    def initUI(self): # ഇവിടെ UI widgets ഉണ്ടാക്കുന്നു # Create all objects

        self.date_box = QDateEdit() # ഇത് Date Picker Widget ആണ്.
        self.date_box.setDate(QDate.currentDate()) # Program run ചെയ്യുമ്പോൾ ഇന്നത്തെ date auto set ചെയ്യും.

        self.dropdown = QComboBox() # Drop-down box ഉണ്ടാക്കുന്നു (category select ചെയ്യാൻ) , "Food", "Travel", "Shopping" തുടങ്ങിയ expense category ചേർക്കാം
        self.amount = QLineEdit() # Text input field ആണ്
        self.description = QLineEdit() # മറ്റൊരു text field, ഇവിടെ expense description (ഉദാ: "Lunch at hotel") type ചെയ്യാം.

        self.btn_add = QPushButton("Add Expense") # Button widget. # User click ചെയ്താൽ expense add ചെയ്യുന്ന function connect ചെയ്യാം.
        self.btn_delete = QPushButton("Delete Expense") # Delete Expense" → table-ലുള്ള selected expense delete ചെയ്യാൻ
        self.btn_delete.setObjectName("btn_delete")

        self.table = QTableWidget(0, 5) # (0, 5) → ആദ്യം 0 rows, 5 columns
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"]) # Table header row set ചെയ്യുന്നു:

        # Edit table width
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense) # last

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)

        self.apply_styles()
        # Add widget to a layout (row/colom)

        self.setup_layout()


    def setup_layout(self):
                                                    # പ്രധാന vertical layout സൃഷ്ടിക്കുന്നു
        master = QVBoxLayout()                             #   ഉള്ളടക്കങ്ങൾ ലംബമായി (താഴേക്ക്) ക്രമീകരിക്കുന്നു
                                                # മൂന്ന് horizontal rows സൃഷ്ടിക്കുന്നു
        row1 = QHBoxLayout()                             # ഉള്ളടക്കങ്ങൾ തിരശ്ചീനമായി (വലത്തോട്ട്) ക്രമീകരിക്കുന്നു
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
                                            # Row 1 - തീയതിയും കാറ്റഗറിയും
        row1.addWidget(QLabel("Date"))           # "Date" എന്ന ലേബൽ
        row1.addWidget(self.date_box)            # തീയതി ഇൻപുട്ട് ബോക്സ്
        row1.addWidget(QLabel("Category"))       # "Category" എന്ന ലേബൽ
        row1.addWidget(self.dropdown)            # ഡ്രോപ്പ്ഡൗൺ മെനു
                                            # Row 2 - തുക, വിവരണം, ബട്ടണുകൾ
        row2.addWidget(QLabel("Amount"))         # "Amount" എന്ന ലേബൽ
        row2.addWidget(self.amount)              # തുക ഇൻപുട്ട് ബോക്സ്
        row2.addWidget(QLabel("Description"))    # "Description" എന്ന ലേബൽ
        row2.addWidget(self.description)         # വിവരണ ഇൻപുട്ട് ബോക്സ്

        row3.addWidget(self.btn_add)             # "Add" ബട്ടൺ
        row3.addWidget(self.btn_delete)          # "Delete" ബട്ടൺ

                                            # എല്ലാ rows മാസ്റ്റർ ലേഔട്ടിലേക്ക് ചേർക്കുന്നു
        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)

                                            # ടേബിൾ വിഡ്ജറ്റ് മാസ്റ്റർ ലേഔട്ടിലേക്ക് ചേർക്കുന്നു
        master.addWidget(self.table)

                                            # മാസ്റ്റർ ലേഔട്ട് മുഖ്യ വിന്ഡോയിലേക്ക് സെറ്റ് ചെയ്യുന്നു
        self.setLayout(master)

    
    def apply_styles(self):
        self.setStyleSheet("""
        QWidget{
            background-color: #e3e9f2;                    /* ആകെ Window-ന്റെ ബാക്ക്ഗ്രൗണ്ട് കളർ */
            font-family: Arial, sans-serif;                      /* ഡിഫോൾട്ട് ഫോണ്ട് */
            font-size: 14px;                                 /* Widget-ുകളുടെ ടെക്സ്റ്റ് സൈസ് */
            color:#333;                                         /* Widget-ിലെ ടെക്സ്റ്റ് കളർ */
        }

        QLabel{
            font-size: 16px;                                   /* ലേബലുകളുടെ ഫോണ്ട് സൈസ് */
            color: #2c3e50;                                          /* ലേബൽ ടെക്സ്റ്റ് കളർ */
            font-weight: bold;                            /* ലേബൽ bold ആയി കാണിക്കാൻ */
            padding: 5px;                                 /* ടെക്സ്റ്റിന് ചുറ്റുമുള്ള സ്പേസ് */
        }
                           
        QLineEdit, QComboBox, QDateEdit {
                border: 1px solid #b0bfc6;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
                selection-background-color: #4caf50;
            }
            
            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #4caf50;
            }
            
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #2a9d8f;
                background-color: #e8f4f8;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                min-width: 120px;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #1c5980;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            
            QTableWidget {
                background-color: white;
                alternate-background-color: #f2f8ff;
                gridline-color: #c0c9d0;
                selection-background-color: #4caf50;
                selection-color: white;
                font-size: 14px;
                border: 1px solid #cfd9e1;
                border-radius: 6px;
            }
            
            QHeaderView::section {
                background-color: #4caf50;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
            }
            
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #b0bfc6;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #b0bfc6;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }



        """)



    def populate_dropdown(self):
        categories = ["Food","Rent","Bills","Entertaiment","Shoping","Others"]
        self.dropdown.addItems(categories)


    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx ,expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for colm_idx,data in enumerate(expense):
                self.table.setItem(row_idx,colm_idx,QTableWidgetItem(str(data)))

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd") # date,category,amount,description)
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self,"Input error","amount and description can not be empty")
            return
        
        if add_expenses(date,category,amount,description):
            self.load_table_data()
            self.clear_inputs()
            #clear inputs
        else :
            QMessageBox.critical(self,"Error", "Failed to add expense")
          

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"Uh , Oh","You need to choose a row to delete")
            return
        
        expense_id = int(self.table.item(selected_row,0).text())
        confirm = QMessageBox.question(self,"Confirm ","Are you sure you want to delete ?",
                                       QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No
                                       )
        
        if confirm == QMessageBox.StandardButton.Yes and delete_expenses(expense_id):self.load_table_data()


