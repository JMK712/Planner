# 入口脚本：直接调用 UI
from ui_main import SchedulePlanner
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = SchedulePlanner()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        print("程序发生错误，详情见 error.log")
