import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer
app = QApplication(sys.argv)
w = QWidget(); w.setWindowTitle("Teste da barra de titulo"); w.resize(700, 160)
w.setStyleSheet("background:#ff00ff"); w.show()
QTimer.singleShot(int(sys.argv[1]), app.quit)
app.exec()
