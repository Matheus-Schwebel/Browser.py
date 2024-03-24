from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from tkinter import messagebox
import subprocess

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
            subprocess.Popen(['py', "M:/Arquivos/Programacao/Python/InHouse/Services/GamesON/EggGame.py"])
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro: {e}")

    def egg_catcherII(self):
        try:
            subprocess.Popen(["py", "M:/Arquivos/Programacao/Python/InHouse/Services/GamesON/EggGameJ.py"])
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro: {e}")