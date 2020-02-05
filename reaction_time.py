from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import QTimer, Qt
from pickle_util import PickleUtil
from time import time
import numpy as np
import sys
import os

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.user_num = 0
        self.gen_handle()
        self.press_hold = True
        self.num_presses = 2
        self.presses_remaining = int(self.num_presses)

        self.initUI()

    def initUI(self):
        self.active_color = QColor(70, 200, 255)
        self.inactive_color = QColor(240, 240, 240)
        self.reaction_timer = QTimer()
        self.reaction_timer.singleShot(np.random.randint(2000, 6000), self.start_reaction)

        self.square = QFrame(self)
        self.square_x, self.square_y = np.random.random_integers(200, 800, (2)).tolist()
        self.square.setGeometry(self.square_x, self.square_y, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                  self.inactive_color.name())

        self.setWindowTitle('Reaction Time Measuring')
        self.setGeometry(800, 300, 1000, 1000)
        self.show()

    def gen_handle(self):
        handle_name = "data\\"+str(self.user_num)
        if 'data' not in os.listdir():
            os.mkdir("data")
            os.mkdir(handle_name)
        if str(self.user_num) not in os.listdir("data"):
            os.mkdir(handle_name)

        self.data_handel_rxn = PickleUtil(handle_name+"\\rxn_times.p")
        self.data_handel_dpt = PickleUtil(handle_name + "\\dp_times.p")

        self.reaction_times = self.data_handel_rxn.safe_load()
        if self.reaction_times is None:
            self.reaction_times = []
        print("Loaded ", len(self.reaction_times), "rxn clicks")

        self.double_press_times = self.data_handel_dpt.safe_load()
        if self.double_press_times is None:
            self.double_press_times = []
        print("Loaded ", len(self.double_press_times), "dpt clicks")



    def start_reaction(self):
        self.square.setStyleSheet("QFrame { background-color: %s }" %
                                  self.active_color.name())

        self.square_x, self.square_y = np.random.random_integers(200, 800, (2)).tolist()
        self.square.setGeometry(self.square_x, self.square_y, 100, 100)
        self.start_time = time()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            if self.press_hold:
                self.on_press()
                self.press_hold = True

        if e.key() == Qt.Key_Control:
            self.press_hold = True

    def on_press(self):
        # self.reaction_timer.singleShot(1000, self.end_reaction)
        self.presses_remaining -= 1

        if self.presses_remaining == self.num_presses-1:
            reaction_time = time() - self.start_time
            self.reaction_times.append(reaction_time)

        if self.presses_remaining == 0:
            self.presses_remaining = int(self.num_presses)
            double_press_time = time() - self.reaction_times[-1] - self.start_time
            self.double_press_times.append(double_press_time)
            self.end_reaction()
            self.reaction_timer.singleShot(np.random.randint(2000, 4000), self.start_reaction)

    def end_reaction(self):
        self.square.setStyleSheet("QFrame { background-color: %s }" %
                                  self.inactive_color.name())

    def closeEvent(self, event):
        print("CLOSING THRU CLOSEEVENT")
        self.quit(event)
        # self.deleteLater()

    def quit(self, event=None):
        self.data_handel_rxn.safe_save(self.reaction_times)
        print("Saving ", len(self.reaction_times), " rxn clicks")
        self.data_handel_dpt.safe_save(self.double_press_times)
        print("Saving ", len(self.double_press_times), " dpt clicks")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
