import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from io import StringIO, BytesIO
import tkinter as tk
from tkinter import scrolledtext, messagebox
import markdown
from tabulate import tabulate
import subprocess
from googletrans import Translator
import fitz  # Esta é a biblioteca PyMuPDF
from PIL import Image
import datetime
# from variaveis import code_py_md
from markdown_inter import MarkdownInterpreter
from webgames import GameConsole

class func_extensions:
 def extension_markdown(browser):
    extensao = MarkdownInterpreter(browser_instance=browser)
    browser_inst2 = Browser()
    browser_inst2.tabs.addTab(extensao, "Markdown Interpreter")
    browser_inst2.tabs.setCurrentWidget(extensao)

 def extension_game(browser):
    extensao = GameConsole(browser=browser)
    browser_instance = Browser()
    browser_instance.tabs.addTab(extensao, "WebGames")
    browser_instance.tabs.setCurrentWidget(extensao)
         

class Extensions(QWidget):
    def __init__(self):
        super().__init__()

        self.browser = Browser()

        self.markdown_checkbox = QCheckBox("Habilitar Markdown Interpreter")
        self.games_checkbox = QCheckBox("Habilitar WebGames")

        self.confirm_button = QPushButton("Confirmar")

        layout = QVBoxLayout()
        layout.addWidget(self.markdown_checkbox)
        layout.addWidget(self.games_checkbox)
        layout.addWidget(self.confirm_button)

        self.confirm_button.clicked.connect(self.confirm_selection)

        self.setLayout(layout)

    def confirm_selection(self):
        markdown_enabled = self.markdown_checkbox.isChecked()
        games_enabled = self.games_checkbox.isChecked()

        if markdown_enabled:
            func_extensions.extension_markdown(browser=self.browser)
        elif games_enabled:
            func_extensions.extension_game(browser=self.browser)

class TradutorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('InHouse Translate')

        self.label1 = QLabel('Digite o texto para traduzir:')
        self.texto_original = QTextEdit(self)

        self.label2 = QLabel('Escolha o idioma de origem:')
        self.combo_idioma_origem = QComboBox(self)
        self.combo_idioma_origem.setEditable(True)
        self.combo_idioma_origem.addItems(['en', 'es', 'fr', 'de', 'pt', 'it', 'nl', 'ru', 'ja', 'ko', 'zh-CN'])

        self.label3 = QLabel('Escolha o idioma de destino:')
        self.combo_idioma_destino = QComboBox(self)
        self.combo_idioma_destino.setEditable(True)
        self.combo_idioma_destino.addItems(['en', 'es', 'fr', 'de', 'pt', 'it', 'nl', 'ru', 'ja', 'ko', 'zh-CN'])

        self.button = QPushButton('Traduzir', self)
        self.button.clicked.connect(self.traduzir_texto)  # Rename the method here

        self.label4 = QLabel(self)
        self.label5 = QLabel(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label1)
        vbox.addWidget(self.texto_original)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.combo_idioma_origem)
        vbox.addWidget(self.label3)
        vbox.addWidget(self.combo_idioma_destino)
        vbox.addWidget(self.button)
        vbox.addWidget(self.label4)
        vbox.addWidget(self.label5)

        self.setLayout(vbox)

    def traduzir_texto(self):  # Rename the method here
        texto = self.texto_original.toPlainText()
        idioma_origem = self.combo_idioma_origem.currentText()
        idioma_destino = self.combo_idioma_destino.currentText()

        translator = Translator()
        traducao = translator.translate(texto, src=idioma_origem, dest=idioma_destino)

        texto_traduzido = traducao.text

        self.label4.setText(f'Texto original ({idioma_origem}): {texto}')
        self.label5.setText(f'Texto traduzido para {idioma_destino}: {texto_traduzido}')

class Browser(QMainWindow):
    def __init__(self):
        print("Console do Desenvolvedor")
        super().__init__()
        self.extension_loaded = False

        # Lista para armazenar as guias abertas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Abre a primeira guia
        self.add_tab("file:///M:/Arquivos/Programacao/Python/InHouse/Search/Search.html")

        self.history = []

        # Configura a janela principal
        self.showMaximized()

        # Configuração da barra de navegação
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Botões de navegação
        back_btn = QAction('←', self)
        back_btn.setStatusTip('Voltar para a página anterior')
        back_btn.triggered.connect(self.current_browser().back)
        self.navbar.addAction(back_btn)

        forward_btn = QAction('→', self)
        forward_btn.setStatusTip('Avançar para a próxima página')
        forward_btn.triggered.connect(self.current_browser().forward)
        self.navbar.addAction(forward_btn)

        reload_btn = QAction('⟲', self)
        reload_btn.setStatusTip('Recarregar a página atual')
        reload_btn.triggered.connect(self.current_browser().reload)
        self.navbar.addAction(reload_btn)

        stop_btn = QAction('X', self)
        stop_btn.setStatusTip('Parar o carregamento da página atual')
        stop_btn.triggered.connect(self.current_browser().stop)
        self.navbar.addAction(stop_btn)

        # Barra de URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # Botão de casa
        home_btn = QAction('Início', self)
        home_btn.setStatusTip('Ir para a página inicial')
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)

        # Adicionar espaço
        self.navbar.addSeparator()

        # Botão para abrir URL
        open_url_btn = QAction('Abrir URL', self)
        open_url_btn.setStatusTip('Abrir URL')
        open_url_btn.triggered.connect(self.navigate_to_url)
        self.navbar.addAction(open_url_btn)

        open_url_btn = QAction('Gravador', self)
        open_url_btn.setStatusTip('Abrir Gravador')
        open_url_btn.triggered.connect(self.gravador)
        self.navbar.addAction(open_url_btn)

        close_tab_btn = QAction('Fechar Guia', self)
        close_tab_btn.setStatusTip('Fechar a guia atual')
        close_tab_btn.triggered.connect(self.close_tab)
        self.navbar.addAction(close_tab_btn)

        # Botão para abrir arquivo HTML
        open_html_btn = QAction('Abrir HTML', self)
        open_html_btn.setStatusTip('Abrir arquivo HTML')
        open_html_btn.triggered.connect(self.open_html_file)
        self.navbar.addAction(open_html_btn)

        open_html_btn = QAction('Traductor', self)
        open_html_btn.setStatusTip('Abrir Tradutor')
        open_html_btn.triggered.connect(self.open_translate)
        self.navbar.addAction(open_html_btn)

        open_pdf_btn = QAction('Abrir PDF', self)
        open_pdf_btn.setStatusTip('Abrir arquivo PDF')
        open_pdf_btn.triggered.connect(self.open_pdf_file)
        self.navbar.addAction(open_pdf_btn)


        open_python_console_btn = QAction('Console Python', self)
        open_python_console_btn.triggered.connect(self.open_python_console)
        self.navbar.addAction(open_python_console_btn)

        # Adicionar nova guia
        tkinter_tab_btn = QAction('✔', self)
        tkinter_tab_btn.setStatusTip('Segurity InHouse Browser')
        tkinter_tab_btn.triggered.connect(self.segurity)
        self.navbar.addAction(tkinter_tab_btn)

        tkinter_tab_btn = QAction('GetWeb', self)
        tkinter_tab_btn.setStatusTip('Abrir Console GetWeb')
        tkinter_tab_btn.triggered.connect(self.getweb)
        self.navbar.addAction(tkinter_tab_btn)

        new_tab_btn = QAction('+', self)
        new_tab_btn.setStatusTip('Abrir nova guia')
        new_tab_btn.triggered.connect(self.add_empty_tab)
        self.navbar.addAction(new_tab_btn)

        history_btn = QAction('Histórico', self)
        history_btn.setStatusTip('Visualizar histórico')
        history_btn.triggered.connect(self.show_history)
        self.navbar.addAction(history_btn)

        games_btn = QAction('Games', self)
        games_btn.setStatusTip('Visualizar Página de Games')
        games_btn.triggered.connect(self.game)
        self.navbar.addAction(games_btn)

        extensoes = QAction('Extensões', self)
        extensoes.setStatusTip('Visualizar Página de Extensoes')
        extensoes.triggered.connect(self.extensions)
        self.navbar.addAction(extensoes)


        # Sinal de atualização da barra de URL
        self.tabs.currentWidget().urlChanged.connect(self.update_urlbar)
        self.game_console = None
        # self.game()
    # ... (código anterior)
        
    def extensions(self):
        self.extensoes = Extensions()

        self.tabs.addTab(self.extensoes, "InHouse Web Store")
        self.tabs.setCurrentWidget(self.extensoes)

    def show_history(self):
     with open("history.HISTORY", "r") as arquivo:
        history = arquivo.read()

    # Carregar o conteúdo CSS
     with open("style.css", "r") as css_file:
        css_content = css_file.read()

    # Substituir quebras de linha por <br> tags
     history_html = "<br>".join(history.splitlines())

    # Criar o HTML com o histórico e o CSS
     html_content = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>History</title>
        <style>
            {css_content}
        </style>
    </head>
    <body>
        <div class="history">
            <h1>History</h1>
        </div>
        <p>{history_html}</p>
    </body>
    </html>"""

    # Criar uma nova instância de Browser para exibir o histórico
     browser_window = Browser()
     browser_window.add_tab(f"data:text/html,{html_content}")
     browser_window.showMaximized()

    def open_pdf_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo PDF", "", "Arquivos PDF (*.pdf);;Todos os arquivos (*)", options=options)

        if file_name:
            pdf_view = PDFViewer(file_name)
            self.tabs.addTab(pdf_view, f"PDF {file_name}")
            self.tabs.setCurrentWidget(pdf_view)
        
    def game(self):
        # print("1")
        self.game_console = GameConsole(browser=self)
        # print("2")
        self.tabs.addTab(self.game_console, "Games")
        self.tabs.setCurrentWidget(self.game_console)
    
    def segurity(self):
        self.root = tk.Tk()
        self.root.title("Segurity of Sites")

        self.button = tk.Button(self.root, text="Ver segurança", command=self.ir)
        self.button.pack()

        self.seguranca = tk.Label(self.root, text="")
        self.seguranca.pack()

        self.seguranca2 = tk.Label(self.root, text="")
        self.seguranca2.pack()

        self.root.mainloop()

    def traduzir(self):
        self.game_console = TradutorApp(browser=self)
        # print("2")
        self.tabs.addTab(self.game_console, "Tradutor")
        self.tabs.setCurrentWidget(self.game_console)
    
    def gravador(self):
        self.gravadorapp = subprocess.Popen(["py","M:/Arquivos/Programacao/Python/InHouse/Services/Gravador/Gravador1.0/Gravador.py"])


    def ir(self):
        get = self.url_bar.text()  # Get the text from the QLineEdit

        if "file:///" in get:
            self.seguranca.config(text="Arquivo ou Ficheiro")
        elif "https://" in get:
            self.seguranca.config(text="Segurança média")
        elif "http://" in get:
            self.seguranca.config(text="Segurança básica")
        elif "inHouse://" in get:
            self.seguranca2.config(text="Segurança certificada por InHouse")
        else:
            self.seguranca.config(text="Inseguro")

    
    def sitew3(self):
        self.url_bar.setText("https://w3schools.com")
        self.navigate_to_url()
    
    def getweb(self):
        return GetWeb()

    def search():
        try:
            subprocess.Popen(["py", "Search3.py"])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def open_python_console(self):
        console_widget = PythonConsole(self)
        self.tabs.addTab(console_widget, "Console Python")
        self.tabs.setCurrentWidget(console_widget)
        self.url_bar.clear()
        self.url_bar.insert("inHouse://python_console")

    def open_translate(self):
        console_widget1 = TradutorApp()
        self.tabs.addTab(console_widget1, "Tradutor")
        self.tabs.setCurrentWidget(console_widget1)
        self.url_bar.clear()
        self.url_bar.insert("inHouse://translate")

    def add_empty_tab(self):
        self.add_tab("file:///M:/Arquivos/Programacao/Python/InHouse/Search/Search.html")

    def close_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index != -1:
            current_widget = self.tabs.widget(current_index)
            current_widget.deleteLater()  # Deleta a instância do widget
            self.tabs.removeTab(current_index)

    def add_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        self.tabs.addTab(browser, "")
        self.tabs.setCurrentWidget(browser)
        browser.urlChanged.connect(self.update_urlbar)
        browser.titleChanged.connect(lambda title=browser.title(): self.update_tab_text(browser, title))

    def update_tab_text(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("file:///M:/Arquivos/Programacao/Python/InHouse/NewSearch/Search.html"))

    def navigate_to_url(self):
     now = datetime.datetime.now()
     formatted_date = now.strftime("%d/%m/%Y")
     formatted_time = now.strftime("%H:%M:%S")

     q = QUrl(self.url_bar.text())
     if q.scheme() == "":
        q.setScheme("http")
     self.current_browser().setUrl(q)

    # Salvar a URL no arquivo de histórico
     url = q.toString()
     with open("history.HISTORY", "a") as arquivo:
        arquivo.write(f"{formatted_date} - {formatted_time}:{url}" + "\n")

    def open_html_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Abrir arquivo HTML", "", "Arquivos HTML (*.html *.htm);;Todos os arquivos (*)", options=options)

        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                html_content = file.read()

            self.current_browser().setHtml(html_content, QUrl.fromLocalFile(file_name))

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)


class GetWeb:
# Dicionário para armazenar variáveis
    variables = {}

    def execute_markdown_code(self, markdown_code):
        html_content = markdown.markdown(markdown_code)
        with open("TransformMarkdown.html", "a") as arquivo:
            arquivo.write(html_content)

        browser = Browser()

        browser.add_tab("file:///M:/Arquivos/Programacao/Python/NavegadorII/TransformMarkdown.html")
        browser.showMaximized()


    def transform(self, html):
        with open("TransformMarkdown.html", "a") as arquivo:
            arquivo.write(f"{html}\n")

            browser_window = Browser()

        # Add a new tab with the HTML content
            browser_window.add_tab("file:///M:/Arquivos/Programacao/Python/NavegadorII/TransformMarkdown.html")

        # Show the Browser window
            browser_window.showMaximized()


    def delete(self):
        with open("TransformMarkdown.html", 'w') as arquivo:  # Ou 'wb' se for um arquivo binário
            arquivo.write(tk.END, "")


    def interpret_and_execute_get_commands(self, commands):
        results = []
        for command in commands:
            if command:
                result = self.execute_get_command(command)
                results.append(result)
        return results
    
    def create_table_markdown(self, table_content):
        # Converte a tabela para markdown usando a biblioteca tabulate
        table_data = [row.split("|") for row in table_content.strip().split("\n")]
        headers = table_data[0]
        rows = table_data[2:]
        formatted_table = tabulate(rows, headers=headers, tablefmt="pipe")
        return formatted_table

    def execute_get_command(self, command):
        global variables

    # Implemente a interpretação real da sua linguagem "get" aqui
        if command.startswith("$ "):
            text_content1 = command[len("$ "):]
            textmarkdown1 = f"# {text_content1}"
            htmlm = markdown.markdown(textmarkdown1)

            self.transform(html=htmlm)

        elif command.startswith("reiniciar "):
            self.delete()

        elif command.startswith("$$ "):
            text_content2 = command[len("$$ "):]
            textmarkdown2 = f"## {text_content2}"
            html2 = markdown.markdown(textmarkdown2)

            self.transform(html=html2)
    
        elif command.startswith("$$$ "):
            text_content3 = command[len("$$$ "):]
            textmarkdown3 = f"### {text_content3}"
            html3 = markdown.markdown(textmarkdown3)

            self.transform(html=html3)

        elif command.startswith("p "):
            text_contentp = command[len("p "):]
            textmarkdownp = f"{text_contentp}"
            htmlp = markdown.markdown(textmarkdownp)

            self.transform(html=htmlp)

        elif command.startswith("m "):
            text_contentm = command[len("m "):]
            self.execute_markdown_code(text_contentm)
    
        elif command.startswith("$$$$ "):
            text_content4 = command[len("$$$$ "):]
            textmarkdown4 = f"#### {text_content4}"
            html4 = markdown.markdown(textmarkdown4)

            self.transform(html=html4)

        elif command.startswith("$$$$$ "):
            text_content5 = command[len("$$$$$ "):]
            textmarkdown5 = f"##### {text_content5}"
            html5 = markdown.markdown(textmarkdown5)

            self.transform(html=html5)

        elif command.startswith("$$$$$$ "):
            text_content6 = command[len("$$$$$$ "):]
            textmarkdown6 = f"###### {text_content6}"
            html6 = markdown.markdown(textmarkdown6)

            self.transform(html=html6)
    
        elif command.startswith("@! "):
            return
        # Adicionar suporte para listas
        elif command.startswith("& "):
            list_items = command[len("& "):].split(",")  # Ou qualquer separador desejado
            list_markdown = "\n".join(f"- {item}" for item in list_items)
            self.execute_markdown_code(list_markdown)

        elif command.startswith("&$ "):
            list_ = command[len("&$ ")].split("|")
            with open("file.GET", "a") as file:
                file.write(tk.END, list_)

        # Adicionar suporte para links
        elif command.startswith("link_custom "):
            link_parts = command[len("link_custom "):].split(",", 1)
            if len(link_parts) == 2:
                link_description, link_url = map(str.strip, link_parts)
                link_markdown = f"[{link_description}]({link_url})"
                self.execute_markdown_code(link_markdown)
            else:
                messagebox.showerror("Erro", "Erro: Comando 'link_custom' requer descrição e URL separados por vírgula.")

        elif command.startswith("> "):
            quote_text = command[len("> "):]
            markdown_code = f"> {quote_text}"
            self.execute_markdown_code(markdown_code)

    
        else:
            messagebox.showerror("Erro", "Erro: Função não existente.")
    
    def get(self):
        commands = [
            self.entry1.get(),
            self.entry2.get(),
            self.entry3.get(),
            self.entry4.get(),
            self.entry5.get()
        ]

        results = self.interpret_and_execute_get_commands(commands)

        for result in results:
            print(f"Resultado: {result}")

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Get Language Interpreter")

# Dicionário para armazenar variáveis
        variables = {}

        self.label1 = tk.Label(self.janela, text="Get Language Interpreter")
        self.label1.pack()

        self.entry1 = tk.Entry(self.janela)
        self.entry2 = tk.Entry(self.janela)
        self.entry3 = tk.Entry(self.janela)
        self.entry4 = tk.Entry(self.janela)
        self.entry5 = tk.Entry(self.janela)

        
        self.entry1.pack()
        self.entry2.pack()
        self.entry3.pack()
        self.entry4.pack()
        self.entry5.pack()

        button = tk.Button(self.janela, text="Lançar GetWeb", command=self.get)
        button.pack()

        button2 = tk.Button(self.janela, text="Reiniciar GetWeb", command=self.delete)
        button2.pack()

        self.janela.mainloop()


class PythonConsole(QWidget):
    def __init__(self, browser):
        super().__init__()

        self.browser = browser

        self.layout = QVBoxLayout()

        self.code_input = QTextEdit(self)
        self.layout.addWidget(self.code_input)

        self.execute_button = QPushButton("Executar", self)
        self.execute_button.clicked.connect(self.execute_python_code)
        self.layout.addWidget(self.execute_button)

        self.output_text = QTextEdit(self)
        self.layout.addWidget(self.output_text)

        self.setLayout(self.layout)

    def execute_python_code(self):
        code_to_execute = self.code_input.toPlainText()

        # Redireciona a saída padrão para um buffer para capturar os resultados
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Executa o código Python
            exec(code_to_execute, globals(), locals())

            # Captura a saída
            result = sys.stdout.getvalue()

            # Exibe os resultados na caixa de texto de saída
            self.output_text.clear()
            self.output_text.insertPlainText(result)

        except Exception as e:
            # Exibe mensagens de erro em caso de exceção
            self.output_text.clear()
            self.output_text.insertPlainText(f'Ocorreu um erro: {str(e)}')

        finally:
            sys.stdout = old_stdout

class PDFViewer(QWidget):
    def __init__(self, file_path):
        super().__init__()

        self.layout = QVBoxLayout()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.pdf_document = fitz.open(file_path)
        self.load_pdf()

        self.setLayout(self.layout)

    def load_pdf(self):
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document[page_num]
            img = page.get_pixmap()
            img = Image.frombytes("RGB", (img.width, img.height), img.samples)
            img = img.convert("RGBA")

            img_byte_array = BytesIO()
            img.save(img_byte_array, format="PNG")
            img_byte_array = img_byte_array.getvalue()

            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_array)
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(pixmap_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName("InHouse Browser")
    window = Browser()
    window.showMaximized()
    app.exec_()