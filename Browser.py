import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from io import StringIO, BytesIO
import tkinter as tk
from googletrans import Translator
import fitz  # Esta é a biblioteca PyMuPDF
from PIL import Image # Esta é a biblioteca Pillow
import datetime
from urllib.parse import urlparse
from OpenSSL import crypto
import ssl
import socket
import requests


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
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.add_plus_button()
        
        # Abre a primeira guia
        self.add_tab("https://www.google.com")

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
        self.url_bar.insert("https://www.google.com")

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

        new_tab_btn = QAction('+', self)
        new_tab_btn.setStatusTip('Abrir nova guia')
        new_tab_btn.triggered.connect(self.add_empty_tab)
        self.navbar.addAction(new_tab_btn)

        history_btn = QAction('Histórico', self)
        history_btn.setStatusTip('Visualizar histórico')
        history_btn.triggered.connect(self.show_history)
        self.navbar.addAction(history_btn)

        # Sinal de atualização da barra de URL
        self.current_browser().urlChanged.connect(self.update_urlbar)
        self.game_console = None

    def add_plus_button(self):
        # Cria o botão "+" e adiciona ao QTabWidget
        plus_button = QPushButton('+')
        plus_button.setFixedSize(25, 25)
        plus_button.clicked.connect(self.add_empty_tab)
        self.tabs.setCornerWidget(plus_button, Qt.TopRightCorner)


    def traduzir(self):
        self.game_console = TradutorApp(browser=self)
        self.tabs.addTab(self.game_console, "Tradutor")
        self.tabs.setCurrentWidget(self.game_console)

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

    def segurity(self):
        self.segurityroot = tk.Tk()
        self.segurityroot.title("Segurança de Sites")

        self.button = tk.Button(self.segurityroot, text="Ver segurança", command=self.verificar_seguranca)
        self.button.pack()

        self.seguranca = tk.Label(self.segurityroot, text="")
        self.seguranca.pack()

        self.ssl = tk.Label(self.segurityroot, text="Certificado SSL:")
        self.ssl.pack()

        self.ssl2 = tk.Label(self.segurityroot, text="")
        self.ssl2.pack()

        self.red = tk.Label(self.segurityroot, text="Redirecionamentos:")
        self.red.pack()

        self.red2 = tk.Label(self.segurityroot, text="")
        self.red2.pack()

        self.cabe = tk.Label(self.segurityroot, text="Cabeçalhos:")
        self.cabe.pack()

        self.cabe2 = tk.Label(self.segurityroot, text="")
        self.cabe2.pack()

        self.segurityroot.mainloop()

    def verificar_certificado_ssl(self, url):
        try:
            hostname = urlparse(url).hostname
            port = 443
            context = ssl.create_default_context()

            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cert_subject = dict(x[0] for x in cert['subject'])
                    cert_issuer = dict(x[0] for x in cert['issuer'])

                    self.ssl2.config(text=f"Certificado válido\nSubject: {cert_subject}\nIssuer: {cert_issuer}")
        except Exception as e:
            self.ssl2.config(text=f"Erro ao verificar certificado SSL: {str(e)}")

    def verificar_redirecionamentos(self, url):
        try:
            response = requests.get(url, allow_redirects=True)
            if response.history:
                self.red2.config(text=f"Redirecionamentos detectados: {[r.url for r in response.history]}")
            else:
                self.red2.config(text="Nenhum redirecionamento detectado")
        except Exception as e:
            self.red2.config(text=f"Erro ao verificar redirecionamentos: {str(e)}")

    def verificar_cabecalhos(self, url):
        try:
            response = requests.get(url)
            headers = response.headers
            seguranca_headers = []

            if 'Strict-Transport-Security' in headers:
                seguranca_headers.append('HSTS Ativado')
            if 'Content-Security-Policy' in headers:
                seguranca_headers.append('CSP Ativado')
            if 'X-Frame-Options' in headers:
                seguranca_headers.append('X-Frame-Options Ativado')

            if seguranca_headers:
                self.cabe2.config(text=f"Cabeçalhos de Segurança: {', '.join(seguranca_headers)}")
            else:
                self.cabe2.config(text="Nenhum cabeçalho de segurança detectado")
        except Exception as e:
            self.cabe2.config(text=f"Erro ao verificar cabeçalhos: {str(e)}")

    def verificar_seguranca(self):
        url = self.url_bar.text()  # Obtém o texto do QLineEdit
        self.seguranca.config(text="")
        self.red2.config(text="")
        self.ssl2.config(text="")

        if not url:
            self.seguranca.config(text="URL vazia")
            return

        # Verificação do esquema
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme

        if scheme == "file":
            self.seguranca.config(text="Arquivo ou Ficheiro")

        else:
            self.verificar_certificado_ssl(url)
            self.verificar_redirecionamentos(url)
            self.verificar_cabecalhos(url)

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
        self.current_browser().setUrl(QUrl("https://www.google.com/"))

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
