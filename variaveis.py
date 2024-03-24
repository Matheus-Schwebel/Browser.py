code_py_md = """import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QPushButton, QApplication
import markdown
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MarkdownInterpreter(QMainWindow):
    def __init__(self, browser_instance):
        super().__init__()

        self.browser_instance = browser_instance

        self.setWindowTitle("InHouse Markdown Interpreter")

        self.code_markdown = QTextEdit(self)
        self.code_markdown.setWordWrapMode(True)
        self.code_markdown.setGeometry(10, 10, 400, 200)

        self.irbutton = QPushButton('Ir', self)
        self.irbutton.setGeometry(10, 220, 100, 30)
        self.irbutton.clicked.connect(self.ir)

    def ir(self):
        markdown_text = self.code_markdown.toPlainText()
        html = markdown.markdown(markdown_text)

        with open("Markdown.html", "w") as arquivo:
            arquivo.write(html)

        browser_window = self.browser_instance
        browser_window.add_tab("file:///M:/Arquivos/Programacao/Python/InHouse/Navegador/Markdown.html")
        browser_window.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MarkdownInterpreter()
    window.show()
    sys.exit(app.exec_())

"""
webgames = """from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from tkinter import messagebox

class GameConsole(QWidget):
    def __init__(self, browser):
        super().__init__()
        # print("3")

        self.browser = browser

        # print("4")

        self.layout = QVBoxLayout()

        # print("5")

        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        # print("6")
        self.label.setText('Jogos disponíveis para este navegador:')

        # print("7")

        self.execute_button = QPushButton("Egg Catcher", self)
        self.execute_button.clicked.connect(self.egg_catcher)

        self.execute_buttonII = QPushButton("Egg Catcher II", self)
        self.execute_buttonII.clicked.connect(self.egg_catcherII)
        self.layout.addWidget(self.execute_button)

        # print("8")
        self.layout.addWidget(self.execute_buttonII)
        # print("9")

        self.setLayout(self.layout)

        # print("\033[3mTexto em itálico\033[0m")
    def egg_catcher(self):
        try:
            process = QProcess(self)
            process.start("py", ["M:/Arquivos/Programacao/Python/InHouse/Services/GamesON/EggGame.py"])
            process.waitForFinished()
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro: {e}")

    def egg_catcherII(self):
        try:
            process = QProcess(self)
            process.start("py", ["M:/Arquivos/Programacao/Python/InHouse/Services/GamesON/EggGameJ.py"])
            process.waitForFinished()
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro: {e}")"""