from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget,QTableWidgetItem,QLineEdit,QPushButton,QRadioButton,QCheckBox,QVBoxLayout,QHBoxLayout,QLabel,QListWidget, QComboBox, QSpinBox, QHeaderView, QMessageBox,QDateEdit
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
# 

# Database
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("climb.db")
if not db.open():
    QMessageBox.critical(None, "ERROR","Could not open the Database!")
    sys.exit(1)
    
query = QSqlQuery()
query.exec_("""
    CREATE TABLE IF NOT EXISTS climb (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        grade TEXT,
        attempts REAL,
        route TEXT,
        sent TEXT
    )
""")


class ClimbApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UrbanClimber")
        self.resize(500,800)
        
        master_layout = QVBoxLayout()
        self.main_text = QLabel("All Sends")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.session_text = QLabel("Todays Session")
        self.table = QTableWidget()
        self.project = QLabel("Current Project")
        self.grade_selection = QComboBox()
        self.attempt_counter = QSpinBox()
        self.sent = QComboBox()
        self.sent.addItems(["Sent","Not Sent"])
        self.route_title = QLineEdit()
        self.route_title.setPlaceholderText("Enter Route Title")
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.submit = QPushButton("Send Route")
        self.remove = QPushButton("Unsend")
        
        self.grade_selection.addItems(["V0","V1","V2","V4","V5","V6","V7","V8","V9","V10"])
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","Date","Grade","Attempts","Route","Sent"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        
        master_layout.addWidget(self.main_text)
        master_layout.addWidget(self.canvas)
        master_layout.addWidget(self.session_text)
        master_layout.addWidget(self.table)
        master_layout.addWidget(self.project)
        row1.addWidget(QLabel("Grade:"))
        row1.addWidget(self.grade_selection)
        row1.addWidget(QLabel("Attempts:"))
        row1.addWidget(self.attempt_counter)
        row1.addWidget(self.date_box)
        row2.addWidget(self.route_title)
        row2.addWidget(self.sent)
        row3.addWidget(self.submit)
        row3.addWidget(self.remove)
        
        master_layout.addLayout(row1)
        master_layout.addLayout(row2)        
        master_layout.addLayout(row3)  
        
        self.setLayout(master_layout)   
        
        
        self.submit.clicked.connect(self.add_climb)
        self.remove.clicked.connect(self.del_climb)
        
        
        self.load_climbs()   
        
    def load_climbs(self):
        self.table.setRowCount(0)
        
        query = QSqlQuery('SELECT * FROM climb ORDER BY grade DESC')
        row = 0
        while query.next():
            climb_id = query.value(0)
            date = query.value(1)
            grade = query.value(2)
            attempts = query.value(3)
            route = query.value(4)
            sent = query.value(5)
            
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(str(climb_id)))
            self.table.setItem(row,1, QTableWidgetItem(date))
            self.table.setItem(row,2,QTableWidgetItem(grade))
            self.table.setItem(row,3,QTableWidgetItem(str(attempts)))
            self.table.setItem(row,4,QTableWidgetItem(route))
            self.table.setItem(row,5,QTableWidgetItem(sent))
            
            row += 1
            
    def del_climb(self):
        selected_row = self.table.currentRow()
        
        if selected_row == -1:
            QMessageBox.warning(self, "No Climb Selected","Please choose a climb!")
            return
        
        climb_id = int(self.table.item(selected_row,0).text())
        
        confirm = QMessageBox.question(self,"Are you sure?","Delete this climb?", QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM climb WHERE id = ?")
        query.addBindValue(climb_id)
        query.exec_()
        
        self.load_climbs()
        
        
        
        
        
        
            
    def add_climb(self):
        date = self.date_box.date().toString('yyyy-MM-dd')
        grade = self.grade_selection.currentText()
        attempts = self.attempt_counter.text()
        route = self.route_title.text()
        sent = self.sent.currentText()
        
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO climb (date, grade, attempts,route, sent)
            VALUES (?, ?, ?, ?, ?)
        """)        
        query.addBindValue(date)
        query.addBindValue(grade)
        query.addBindValue(attempts)
        query.addBindValue(route)
        query.addBindValue(sent)
        query.exec_()
        
        self.date_box.setDate(QDate.currentDate())
        self.grade_selection.setCurrentIndex(0)
        self.route_title.clear()
        self.sent.setCurrentIndex(0)
        
        self.load_climbs()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
if __name__ in "__main__":
    app = QApplication([])
    main = ClimbApp()
    main.show()
    app.exec_()