import sys

from PyQt5.QtWidgets import QApplication

from src.views.home_page import HomePage

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = HomePage()
    win.show()
    sys.exit(app.exec_())
