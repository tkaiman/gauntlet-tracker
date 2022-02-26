from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import csv


## TODO : Add a graph function to show w/l over time
## TODO : Add a label that shows w/l over the last x days
## TODO : add more??

class app_gui(QDialog):
    def __init__(self, parent=None):
        super(app_gui, self).__init__(parent)
        self.left_box = None
        self.right_box = None
        self.file_path = None
        self.currentRow = 0
        self.tableWidget = None
        self.wins = 0
        self.losses = 0
        self.win_loss = QLabel(f'Wins: {self.wins} Losses: {self.losses}')
        self.win_button = QPushButton("Win")
        self.loss_button = QPushButton("Loss")
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load")
        self.setFixedSize(800, 600)
        self.originalPalette = QApplication.palette()
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("$Use Style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("Disable widgets")

        self.create_right_box()
        self.create_left_box()
        self.win_button.clicked.connect(self.set_win_text)
        self.loss_button.clicked.connect(self.set_loss_text)
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)

    def save(self):
        if self.file_path is None:
            self.save_as()
        else:
            with open(self.file_path, 'w') as f:
                writer = csv.writer(f, delimiter=' ', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                for row in range(self.currentRow):
                    print(row)
                    writer.writerow([self.tableWidget.item(row, 0).text(),
                                     self.tableWidget.item(row, 1).text()])

    def save_as(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', "", "CSV(*.csv)")
        if path:
            self.file_path = path[0]
            self.save()

    def load(self):
        self.file_path = QFileDialog.getOpenFileName(self, 'Open File', "", "CSV(*.csv)")[0]
        self.currentRow = 0
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            for row in reader:
                print(row)
                self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem(row[0]))
                self.tableWidget.setItem(self.currentRow, 1, QTableWidgetItem(row[1]))
                self.currentRow += 1
        self.load_button.setEnabled(False)

    def create_right_box(self):
        self.right_box = QGroupBox("")

        layout = QGridLayout()
        layout.setRowStretch(0, 300)
        layout.addWidget(self.win_button, 0, 0)
        layout.addWidget(self.loss_button, 0, 1)
        layout.addWidget(self.win_loss, 1, 0, 1, 2)
        layout.addWidget(self.save_button, 2, 0)
        layout.addWidget(self.load_button, 2, 1)
        self.right_box.setLayout(layout)
        self.win_button.setFixedSize(200, 200)
        self.loss_button.setFixedSize(200, 200)
        self.win_button.setFont(QFont("Times", 20, QFont.Bold))
        self.loss_button.setFont(QFont("Times", 20, QFont.Bold))

    def set_win_text(self):
        datetime = QDateTime.currentDateTime()
        self.wins += 1
        self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem("Win"))
        self.tableWidget.setItem(self.currentRow, 1, QTableWidgetItem(datetime.toString()))
        self.win_loss.setText(f'Wins: {self.wins} Losses: {self.losses}')
        self.currentRow += 1

    def set_loss_text(self):
        datetime = QDateTime.currentDateTime()
        self.losses += 1
        self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem("Loss"))
        self.tableWidget.setItem(self.currentRow, 1, QTableWidgetItem(datetime.toString()))
        self.win_loss.setText(f'Wins: {self.wins} Losses: {self.losses}')
        self.currentRow += 1

    def update_data(self):
        pass

    def create_left_box(self):
        self.left_box = QTabWidget()
        self.left_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        tab1 = QWidget()
        self.tableWidget = QTableWidget(1000, 2)
        self.tableWidget.setColumnWidth(1, 200)
        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(self.tableWidget)
        tab1.setLayout(tab1hbox)
        self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem("Result"))
        self.tableWidget.setItem(self.currentRow, 1, QTableWidgetItem("Date"))
        self.currentRow += 1

        self.left_box.addTab(tab1, "Spreadsheet")
        self.create_main_layout()
        self.setWindowTitle("Gauntlet Tracker")

    def create_main_layout(self):
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.left_box, 0, 0, 1, 1)
        self.main_layout.addWidget(self.right_box, 0, 1, 1, 1)
        self.setLayout(self.main_layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = app_gui()
    gallery.show()
    sys.exit(app.exec_())