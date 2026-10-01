import sys, subprocess
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QFont

OUT = sys.argv[1]
LABELS = ["diag_de_cima-esq", "diag_de_baixo-esq", "diag_de_cima-dir", "diag_de_baixo-dir", "horiz_da_esq", "vert_de_cima"]
LABELS = LABELS[:int(sys.argv[2])] if len(sys.argv) > 2 else LABELS

class Popup(QWidget):
    def __init__(self, parent):
        super().__init__(parent, Qt.ToolTip | Qt.FramelessWindowHint)
        self.resize(220, 300)
    def paintEvent(self, e):
        p = QPainter(self); w, h = self.width(), self.height()
        p.fillRect(self.rect(), QColor("#c0c0c0"))
        p.setFont(QFont("Liberation Sans", 10)); p.setPen(Qt.black)
        for i in range(9):
            p.drawText(28, 50 + i * 26, f"Item {i + 1}   ABCDEFGH")
        for c, x, y in (("#ff0000", 0, 0), ("#00c000", w - 24, 0), ("#0000ff", 0, h - 24), ("#ffff00", w - 24, h - 24)):
            p.fillRect(x, y, 24, 24, QColor(c))
        p.setPen(QColor("#ff00ff")); p.drawRect(0, 0, w - 1, h - 1); p.drawRect(1, 1, w - 3, h - 3)

app = QApplication(sys.argv)
main = QWidget(); main.setWindowTitle("win98 slide test"); main.resize(620, 460)
main.setStyleSheet("background:#203050"); main.show()
popup = Popup(main)
step = [0]

def show_next():
    i = step[0]
    if i >= len(LABELS):
        app.quit(); return
    popup.move(main.mapToGlobal(QPoint(200, 80))); popup.show()
    QTimer.singleShot(1000, lambda: subprocess.Popen(["spectacle", "-f", "-b", "-n", "-o", f"{OUT}/slide_{i}_{LABELS[i]}.png"]))
    QTimer.singleShot(4200, popup.hide)
    step[0] += 1
    QTimer.singleShot(5200, show_next)

QTimer.singleShot(1800, show_next)
app.exec()
