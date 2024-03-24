import sys
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

