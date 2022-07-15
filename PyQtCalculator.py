import sys

from functools import partial

from PyQt5.QtCore import(
    Qt
)

from PyQt5.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QLineEdit
)

ERROR_MSG = 'ERROR'
__version__ = '0.1'
__author__ = 'Dipanshu singh'


def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result


class PyUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #
        self.setWindowTitle('PyQT calculator')
        self.setFixedSize(235, 235)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        #
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
            '7': (0, 0),
            '8': (0, 1),
            '9': (0, 2),
            '/': (0, 3),
            'C': (0, 4),
            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '*': (1, 3),
            '(': (1, 4),
            '1': (2, 0),
            '2': (2, 1),
            '3': (2, 2),
            '-': (2, 3),
            ')': (2, 4),
            '0': (3, 0),
            '00': (3, 1),
            '.': (3, 2),
            '+': (3, 3),
            '=': (3, 4),
        }
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText('')


class clacControl:
    def __init__(self, model, view):
        self._view = view
        self._evaluate = model
        self._connectSignals()

    def _calculateResults(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btnTxt, btn in self._view.buttons.items():
            if btnTxt not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnTxt))

        self._view.buttons['='].clicked.connect(self._calculateResults)
        self._view.display.returnPressed.connect(self._calculateResults)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)


def main():
    PyCal = QApplication(sys.argv)
    view = PyUI()
    view.show()

    model = evaluateExpression
    clacControl(view=view, model=model)
    sys.exit(PyCal.exec())


if __name__ == '__main__':
    main()
