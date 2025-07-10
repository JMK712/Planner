from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import sys

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试按钮")
        layout = QVBoxLayout()

        btn = QPushButton("点击我")
        btn.clicked.connect(self.on_click)

        layout.addWidget(btn)
        self.setLayout(layout)

    def on_click(self):
        print("按钮被点击了！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Demo()
    win.show()
    sys.exit(app.exec_())
