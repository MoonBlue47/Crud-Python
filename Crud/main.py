import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from database import Database


class MainWindow(QMainWindow):

  def __init__(self):
    super().__init__()
    self.db = Database()
    self.selected_id = None

    self.setWindowTitle("Gerenciador de Contatos Senai")
    self.resize(650, 500)

    self.init_ui()

  def init_ui(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)

    # ===========================================
    # 1. DECLARANDO COMPONENTES DA TELA
    # ===========================================
    self.lbl_titulo = QLabel("Cadastro de Contatos")

    # Grupo do Formulário
    self.group_form = QGroupBox("Informações do Contato")
    self.lbl_nome = QLabel("Nome: ")
    self.txt_nome = QLineEdit()
    self.lbl_telefone = QLabel("Telefone: ")
    self.txt_telefone = QLineEdit()
    self.lbl_email = QLabel("E-mail: ")
    self.txt_email = QLineEdit()

    self.btn_cadastrar = QPushButton("Cadastrar")
    self.btn_atualizar = QPushButton("Atualizar")
    self.btn_excluir = QPushButton("Excluir")
    self.btn_limpar = QPushButton("Limpar Campos")

    # Declaração da Tabela que faltava
    self.tabela = QTableWidget()

    # ===========================================
    # CONFIGURAÇÕES E SINAIS DOS COMPONENTES
    # ===========================================
    # Estilização Básica
    font_titulo = self.lbl_titulo.font()
    font_titulo.setPointSize(14)
    font_titulo.setBold(True)
    self.lbl_titulo.setFont(font_titulo)
    self.lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Configuração da Tabela
    self.tabela.setColumnCount(4)
    self.tabela.setHorizontalHeaderLabels(
        ["Nome", "E-mail", "Telefone", "Cadastro"]
    )
    # Correção aplicada aqui (passando True em vez de ResizeMode):
    self.tabela.horizontalHeader().setStretchLastSection(True)

    self.tabela.setSelectionBehavior(
        QTableWidget.SelectionBehavior.SelectRows
    )
    self.tabela.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    # Conexão dos eventos aos botões
    self.btn_cadastrar.clicked.connect(self.cadastrar)
    self.btn_atualizar.clicked.connect(self.atualizar)
    self.btn_excluir.clicked.connect(self.excluir)
    self.btn_limpar.clicked.connect(self.limpar_campos)
    self.tabela.itemSelectionChanged.connect(self.selecionar_contato)

    # Layout do Formulário
    layout_form = QGridLayout()
    layout_form.addWidget(self.lbl_nome, 0, 0)
    layout_form.addWidget(self.txt_nome, 0, 1)
    layout_form.addWidget(self.lbl_telefone, 1, 0)
    layout_form.addWidget(self.txt_telefone, 1, 1)
    layout_form.addWidget(self.lbl_email, 2, 0)
    layout_form.addWidget(self.txt_email, 2, 1)
    self.group_form.setLayout(layout_form)

    # Layout dos Botões
    layout_botoes = QHBoxLayout()
    layout_botoes.addWidget(self.btn_cadastrar)
    layout_botoes.addWidget(self.btn_atualizar)
    layout_botoes.addWidget(self.btn_excluir)
    layout_botoes.addWidget(self.btn_limpar)

    # Layout da Tabela
    layout_tabela = QVBoxLayout()
    layout_tabela.addWidget(self.tabela)

    # Layout Principal
    layout_principal = QVBoxLayout()
    layout_principal.addWidget(self.lbl_titulo)
    layout_principal.addWidget(self.group_form)
    layout_principal.addLayout(layout_botoes)
    layout_principal.addLayout(layout_tabela)

    central_widget.setLayout(layout_principal)
    self.atualizar_tabela()

  def cadastrar(self):
    nome = self.txt_nome.text()
    telefone = self.txt_telefone.text()
    email = self.txt_email.text()

    if not nome or not telefone or not email:
      QMessageBox.critical(
          self, "Erro", "Preencha todos os campos para cadastrar!"
      )
      return

    self.db.inserir(nome, telefone, email)
    QMessageBox.information(self, "Sucesso", "Contato cadastrado com sucesso!")
    self.limpar_campos()
    self.atualizar_tabela()

  def atualizar(self):
    if self.selected_id is None:
      QMessageBox.warning(
          self, "Aviso", "Selecione um contato da tabela para atualizar!"
      )
      return
    nome = self.txt_nome.text().strip()
    telefone = self.txt_telefone.text().strip()
    email = self.txt_email.text().strip()
    if not nome or not telefone or not email:
      QMessageBox.critical(self, "Erro", "Todos os campos devem ser preenchidos")
      return
    self.db.atualizar(self.selected_id, nome, telefone, email)
    QMessageBox.information(self, "Sucesso", "Contato atualizado!")

    self.limpar_campos()
    self.atualizar_tabela()

  def excluir(self):
    if self.selected_id is None:
      QMessageBox.warning(
          self, "Aviso", "Selecione um contato da tabela para excluir!"
      )
      return
    resposta = QMessageBox.question(
        self,
        "Confirmação",
        "Deseja realmente excluir este contato?",
        QMessageBox.StandardButton.Yes,
        QMessageBox.StandardButton.No,
    )
    if resposta == QMessageBox.StandardButton.Yes:
      self.db.excluir(self.selected_id)
      QMessageBox.information(
          self, "Sucesso!", "Contato excluido com sucesso!"
      )
      self.limpar_campos()
      self.atualizar_tabela()

  def selecionar_contato(self):
    linhas_selecionadas = self.tabela.selectionModel().selectedRows()
    if linhas_selecionadas:
      linha = linhas_selecionadas[0].row()
      # Preenchimento posterior conforme a estrutura do banco

  def limpar_campos(self):
    self.txt_nome.clear()
    self.txt_telefone.clear()
    self.txt_email.clear()
    self.selected_id = None
    self.tabela.clearSelection()

  def atualizar_tabela(self):
    self.tabela.setRowCount(0)
    dados = self.db.listar()

    for linha_idx, linha_data in enumerate(dados):
      self.tabela.insertRow(linha_idx)
      for col_idx, col_data in enumerate(linha_data):
        item = QTableWidgetItem(str(col_data))
        self.tabela.setItem(linha_idx, col_idx, item)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  janela = MainWindow()
  janela.show()
  sys.exit(app.exec())