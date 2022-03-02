from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import csv


# TODO : add more??

class app_gui(QDialog):
    def __init__(self, parent=None):
        super(app_gui, self).__init__(parent)
        self.main_layout = None
        self.left_box = None
        self.right_box = None
        self.file_path = None
        self.currentRow = 0
        self.tableWidget = None
        self.wins = 0
        self.losses = 0
        self.wlratio = 0
        self.dailywins = 0
        self.dailyloss = 0
        self.textBoxValue = ''
        self.parameters = QLineEdit(f'1')
        self.ratios = QLabel(f'W/l over last x days {self.wlratio}')
        self.win_loss = QLabel(f'Wins: {self.wins} Losses: {self.losses}                                         W/l for the day : {self.dailywins}/{self.dailyloss} ')
        self.win_loss.setWordWrap(True)
        self.ratio_button = QPushButton("Set parameter")
        self.win_button = QPushButton("Win")
        self.loss_button = QPushButton("Loss")
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load")
        self.width = 1000
        self.height = 600
        self.setFixedSize(self.width, self.height)
        self.originalPalette = QApplication.palette()
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("$Use Style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        self.create_right_box()
        self.create_left_box()
        self.win_button.clicked.connect(self.set_win_text)
        self.loss_button.clicked.connect(self.set_loss_text)
        self.save_button.clicked.connect(self.save)
        self.load_button.clicked.connect(self.load)
        self.ratio_button.clicked.connect(self.ratio)

    def ratio(self):
        tallywins = 0
        tallyloss = 0
        self.dailywins = 0
        self.dailyloss = 0
        self.textBoxValue = self.parameters.text()
        try:
            self.wlratio = int(self.textBoxValue)
        except ValueError as e:
            print(e)
            QMessageBox.critical(self, 'Error', 'Couldnt read value, put a positive integer in')
        if self.wlratio != 0:
            now = QDateTime.currentDateTime()
            days = self.wlratio
            for row in range(1, self.currentRow):
                date = QDateTime.fromString(self.tableWidget.item(row, 1).text())
                delta = date.daysTo(now)
                if self.wlratio >= delta:
                    if self.tableWidget.item(row, 0).text() == "Win":
                        tallywins += 1
                    else:
                        tallyloss += 1
                if delta < 1:
                    if self.tableWidget.item(row, 0).text() == "Win":
                        self.dailywins += 1
                    else:
                        self.dailyloss += 1
            self.wlratio = (tallywins / (tallyloss + tallywins)) * 100
            self.ratios.setText(f'W/l over last {days} days {int(self.wlratio)}%')
            self.win_loss.setText(f'Wins: {self.wins} Losses: {self.losses}                                               W/l for the day : {self.dailywins}/{self.dailyloss} ')
            self.check_day()

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
                if row[0] == "Win":
                    self.wins += 1
                    self.tableWidget.item(self.currentRow, 0).setBackground(QColor(0, 255, 0, 127))
                elif row[0] == "Loss":
                    self.losses += 1
                    self.tableWidget.item(self.currentRow, 0).setBackground(QColor(255, 0, 0, 127))
                self.currentRow += 1
        self.load_button.setEnabled(False)

    def create_right_box(self):
        self.right_box = QGroupBox("")

        layout = QGridLayout()
        layout.setRowStretch(0, 300)
        layout.addWidget(self.win_button, 0, 0)
        layout.addWidget(self.loss_button, 0, 1)
        layout.addWidget(self.win_loss, 1, 0)
        layout.addWidget(self.ratios, 1, 1)
        layout.addWidget(self.parameters, 2, 0)
        layout.addWidget(self.ratio_button, 2, 1)
        layout.addWidget(self.save_button, 3, 0)
        layout.addWidget(self.load_button, 3, 1)
        self.right_box.setLayout(layout)
        self.win_button.setFixedSize(200, 200)
        self.loss_button.setFixedSize(200, 200)
        self.parameters.setFixedSize(200, 80)
        self.win_button.setFont(QFont("Times", 20, QFont.Bold))
        self.loss_button.setFont(QFont("Times", 20, QFont.Bold))

    def set_win_text(self):
        datetime = QDateTime.currentDateTime()
        self.wins += 1
        self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem("Win"))
        self.tableWidget.item(self.currentRow, 0).setBackground(QColor(0, 255, 0, 127))
        self.tableWidget.setItem(self.currentRow, 1, QTableWidgetItem(datetime.toString()))
        self.win_loss.setText(f'Wins: {self.wins} Losses: {self.losses}           W/l for the day : {self.dailywins}/{self.dailyloss} ')
        self.currentRow += 1
        self.ratio()

    def set_loss_text(self):
        datetime = QDateTime.currentDateTime()
        self.losses += 1
        self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem("Loss"))
        self.tableWidget.item(self.currentRow, 0).setBackground(QColor(255, 0, 0, 127))
        self.tableWidget.setItem(self.currentRow, 1, QTableWidgetItem(datetime.toString()))
        self.win_loss.setText(f'Wins: {self.wins} Losses: {self.losses}            W/l for the day : {self.dailywins}/{self.dailyloss} ')
        self.currentRow += 1
        self.ratio()

    def check_day(self):

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
        self.left_box.setFixedSize(self.width // 2, self.height)

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
