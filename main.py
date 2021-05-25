from GUI import *
import sys, os

def main():
    app = QtWidgets.QApplication(sys.argv)

    ui = UiMainWindow()
    ui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
