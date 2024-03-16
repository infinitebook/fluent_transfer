from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QTimer, QRunnable , Slot , QThreadPool

import sys
import time

class MainWindow(QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()

        self.counter = 0

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def oh_no(self):
        a=2314
        worker=Worker(self.execute_this_fn,a,adwdaw="1243",awd="123ad")
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)

    def execute_this_fn(self,a):
        print("hello!")
        print(a)



class Worker(QRunnable):
    def __init__(self,fn,*args, **kwargs):
        super(Worker,self).__init__()
        self.fn = fn
        self.args= args
        self.kwargs= kwargs

    @Slot()
    def run(self):
        self.fn(self.args)
        print("123")
        for key,value in self.kwargs.items():
            print(value)
        print(self.kwargs.get("name"))





app = QApplication(sys.argv)
window = MainWindow()
app.exec()
