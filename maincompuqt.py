import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog, QLineEdit, QTabWidget, QPushButton, QHBoxLayout
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "mysql+pymysql://root:@localhost/tde"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    pets = relationship('Pet', back_populates='dono')

class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    especie = Column(String(255), nullable=False)
    raca = Column(String(255), default=None)
    idade = Column(Integer, default=None)
    id_dono = Column(Integer, ForeignKey('clientes.id'))
    dono = relationship('Cliente', back_populates='pets')

class Servico(Base):
    __tablename__ = 'servicos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, default=None)
    preco = Column(Numeric(10, 2), nullable=False)

class Taxidog(Base):
    __tablename__ = 'taxidog'
    id = Column(Integer, primary_key=True, autoincrement=True)
    preco = Column(Numeric(10, 2), nullable=False)
    tempo_ida = Column(Integer, nullable=False)
    tempo_volta = Column(Integer, nullable=False)

class PetshopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Petshop")
        self.setGeometry(100, 100, 900, 600)  # Definindo o tamanho inicial da janela

        layout_principal = QVBoxLayout()
        self.abas = QTabWidget()
        layout_principal.addWidget(self.abas)

        self.setLayout(layout_principal)

        self.criar_aba_cliente()
        self.criar_aba_pet()
        self.criar_aba_servico()
        self.criar_aba_taxidog()

        self.show()

    def criar_aba_cliente(self):
        aba_cliente = QWidget()
        layout = QVBoxLayout()

        botao_adicionar = QPushButton("Adicionar Cliente")
        botao_adicionar.clicked.connect(self.adicionar_cliente)

        botao_atualizar = QPushButton("Atualizar Cliente")
        botao_atualizar.clicked.connect(self.atualizar_cliente)

        botao_deletar = QPushButton("Deletar Cliente")
        botao_deletar.clicked.connect(self.deletar_cliente)

        botao_listar = QPushButton("Listar Clientes")
        botao_listar.clicked.connect(self.listar_clientes)

        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(botao_listar)

        aba_cliente.setLayout(layout)
        self.abas.addTab(aba_cliente, "Cliente")

    def criar_aba_pet(self):
        aba_pet = QWidget()
        layout = QVBoxLayout()

        botao_adicionar = QPushButton("Adicionar Pet")
        botao_adicionar.clicked.connect(self.adicionar_pet)

        botao_atualizar = QPushButton("Atualizar Pet")
        botao_atualizar.clicked.connect(self.atualizar_pet)

        botao_deletar = QPushButton("Deletar Pet")
        botao_deletar.clicked.connect(self.deletar_pet)

        botao_listar = QPushButton("Listar Pets")
        botao_listar.clicked.connect(self.listar_pets)

        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(botao_listar)

        aba_pet.setLayout(layout)
        self.abas.addTab(aba_pet, "Pet")

    def criar_aba_servico(self):
        aba_servico = QWidget()
        layout = QVBoxLayout()

        botao_adicionar = QPushButton("Adicionar Serviço")
        botao_adicionar.clicked.connect(self.adicionar_servico)

        botao_atualizar = QPushButton("Atualizar Serviço")
        botao_atualizar.clicked.connect(self.atualizar_servico)

        botao_deletar = QPushButton("Deletar Serviço")
        botao_deletar.clicked.connect(self.deletar_servico)

        botao_listar = QPushButton("Listar Serviços")
        botao_listar.clicked.connect(self.listar_servicos)

        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(botao_listar)

        aba_servico.setLayout(layout)
        self.abas.addTab(aba_servico, "Serviço")

    def criar_aba_taxidog(self):
        aba_taxidog = QWidget()
        layout = QVBoxLayout()

        botao_adicionar = QPushButton("Adicionar Taxidog")
        botao_adicionar.clicked.connect(self.adicionar_taxidog)

        botao_atualizar = QPushButton("Atualizar Taxidog")
        botao_atualizar.clicked.connect(self.atualizar_taxidog)

        botao_deletar = QPushButton("Deletar Taxidog")
        botao_deletar.clicked.connect(self.deletar_taxidog)

        botao_listar = QPushButton("Listar Taxidog")
        botao_listar.clicked.connect(self.listar_taxidog)

        layout.addWidget(botao_adicionar)
        layout.addWidget(botao_atualizar)
        layout.addWidget(botao_deletar)
        layout.addWidget(botao_listar)

        aba_taxidog.setLayout(layout)
        self.abas.addTab(aba_taxidog, "TaxiDog")

    def exibir_dados(self, dados, colunas):
        tabela = QTableWidget()
        tabela.setRowCount(len(dados))
        tabela.setColumnCount(len(colunas))
        tabela.setHorizontalHeaderLabels(colunas)

        for i, dado in enumerate(dados):
            for j, atributo in enumerate(colunas):
                valor = getattr(dado, atributo.lower())
                tabela.setItem(i, j, QTableWidgetItem(str(valor)))

        self.abas.addTab(tabela, "Resultados")
        self.abas.tabBar().setTabsClosable(True)
        self.abas.tabBar().tabCloseRequested.connect(lambda: self.fechar_aba(self.abas.indexOf(tabela)))
        self.abas.setCurrentWidget(tabela)

    def fechar_aba(self, index):
        self.abas.removeTab(index)

    def adicionar_cliente(self):
        nome, ok_nome = QInputDialog.getText(self, "Adicionar Cliente", "Nome do Cliente:")
        telefone, ok_telefone = QInputDialog.getText(self, "Adicionar Cliente", "Telefone do Cliente:")
        email, ok_email = QInputDialog.getText(self, "Adicionar Cliente", "Email do Cliente:")
        if ok_nome and ok_telefone and ok_email:
            novo_cliente = Cliente(nome=nome, telefone=telefone, email=email)
            session.add(novo_cliente)
            session.commit()

    def atualizar_cliente(self):
        id_cliente, ok = QInputDialog.getInt(self, "Atualizar Cliente", "Digite o ID do Cliente:")
        if ok:
            cliente = session.query(Cliente).filter_by(id=id_cliente).first()
            if cliente:
                nome, ok_nome = QInputDialog.getText(self, "Atualizar Cliente", "Nome:", QLineEdit.Normal, cliente.nome)
                telefone, ok_telefone = QInputDialog.getText(self, "Atualizar Cliente", "Telefone:", QLineEdit.Normal, cliente.telefone)
                email, ok_email = QInputDialog.getText(self, "Atualizar Cliente", "Email:", QLineEdit.Normal, cliente.email)

                if ok_nome and ok_telefone and ok_email:
                    cliente.nome = nome
                    cliente.telefone = telefone
                    cliente.email = email
                    session.commit()

    def deletar_cliente(self):
        id_cliente, ok = QInputDialog.getInt(self, "Deletar Cliente", "Digite o ID do Cliente para excluir:")
        if ok:
            cliente = session.query(Cliente).filter_by(id=id_cliente).first()
            if cliente:
                session.delete(cliente)
                session.commit()

    def listar_clientes(self):
        clientes = session.query(Cliente).all()
        colunas = ['id', 'nome', 'telefone', 'email']
        self.exibir_dados(clientes, colunas)

    def adicionar_pet(self):
        nome, ok_nome = QInputDialog.getText(self, "Adicionar Pet", "Nome do Pet:")
        especie, ok_especie = QInputDialog.getText(self, "Adicionar Pet", "Espécie do Pet:")
        raca, ok_raca = QInputDialog.getText(self, "Adicionar Pet", "Raça do Pet:")
        idade, ok_idade = QInputDialog.getInt(self, "Adicionar Pet", "Idade do Pet:")
        id_dono, ok_id_dono = QInputDialog.getInt(self, "Adicionar Pet", "ID do Dono do Pet:")
        if ok_nome and ok_especie and ok_raca and ok_idade and ok_id_dono:
            novo_pet = Pet(nome=nome, especie=especie, raca=raca, idade=idade, id_dono=id_dono)
            session.add(novo_pet)
            session.commit()

    def atualizar_pet(self):
        id_pet, ok = QInputDialog.getInt(self, "Atualizar Pet", "Digite o ID do Pet:")
        if ok:
            pet = session.query(Pet).filter_by(id=id_pet).first()
            if pet:
                nome, ok_nome = QInputDialog.getText(self, "Atualizar Pet", "Nome:", QLineEdit.Normal, pet.nome)
                especie, ok_especie = QInputDialog.getText(self, "Atualizar Pet", "Espécie:", QLineEdit.Normal, pet.especie)
                raca, ok_raca = QInputDialog.getText(self, "Atualizar Pet", "Raça:", QLineEdit.Normal, pet.raca)
                idade, ok_idade = QInputDialog.getInt(self, "Atualizar Pet", "Idade:", QLineEdit.Normal, pet.idade)

                if ok_nome and ok_especie and ok_raca and ok_idade:
                    pet.nome = nome
                    pet.especie = especie
                    pet.raca = raca
                    pet.idade = idade
                    session.commit()

    def deletar_pet(self):
        id_pet, ok = QInputDialog.getInt(self, "Deletar Pet", "Digite o ID do Pet para excluir:")
        if ok:
            pet = session.query(Pet).filter_by(id=id_pet).first()
            if pet:
                session.delete(pet)
                session.commit()

    def listar_pets(self):
        pets = session.query(Pet).all()
        colunas = ['id', 'nome', 'especie', 'raca', 'idade', 'id_dono']
        self.exibir_dados(pets, colunas)

    def adicionar_servico(self):
        nome, ok_nome = QInputDialog.getText(self, "Adicionar Serviço", "Nome do Serviço:")
        descricao, ok_descricao = QInputDialog.getText(self, "Adicionar Serviço", "Descrição do Serviço:")
        preco, ok_preco = QInputDialog.getDouble(self, "Adicionar Serviço", "Preço do Serviço:")
        if ok_nome and ok_descricao and ok_preco:
            novo_servico = Servico(nome=nome, descricao=descricao, preco=preco)
            session.add(novo_servico)
            session.commit()

    def atualizar_servico(self):
        id_servico, ok = QInputDialog.getInt(self, "Atualizar Serviço", "Digite o ID do Serviço:")
        if ok:
            servico = session.query(Servico).filter_by(id=id_servico).first()
            if servico:
                nome, ok_nome = QInputDialog.getText(self, "Atualizar Serviço", "Nome:", QLineEdit.Normal, servico.nome)
                descricao, ok_descricao = QInputDialog.getText(self, "Atualizar Serviço", "Descrição:", QLineEdit.Normal, servico.descricao)
                preco, ok_preco = QInputDialog.getDouble(self, "Atualizar Serviço", "Preço:", QLineEdit.Normal, servico.preco)

                if ok_nome and ok_descricao and ok_preco:
                    servico.nome = nome
                    servico.descricao = descricao
                    servico.preco = preco
                    session.commit()

    def deletar_servico(self):
        id_servico, ok = QInputDialog.getInt(self, "Deletar Serviço", "Digite o ID do Serviço para excluir:")
        if ok:
            servico = session.query(Servico).filter_by(id=id_servico).first()
            if servico:
                session.delete(servico)
                session.commit()

    def listar_servicos(self):
        servicos = session.query(Servico).all()
        colunas = ['id', 'nome', 'descricao', 'preco']
        self.exibir_dados(servicos, colunas)

    def adicionar_taxidog(self):
        preco, ok_preco = QInputDialog.getDouble(self, "Adicionar Taxidog", "Preço do TaxiDog:")
        tempo_ida, ok_tempo_ida = QInputDialog.getInt(self, "Adicionar Taxidog", "Tempo de Ida (min):")
        tempo_volta, ok_tempo_volta = QInputDialog.getInt(self, "Adicionar Taxidog", "Tempo de Volta (min):")
        if ok_preco and ok_tempo_ida and ok_tempo_volta:
            novo_taxidog = Taxidog(preco=preco, tempo_ida=tempo_ida, tempo_volta=tempo_volta)
            session.add(novo_taxidog)
            session.commit()

    def atualizar_taxidog(self):
        id_taxidog, ok = QInputDialog.getInt(self, "Atualizar Taxidog", "Digite o ID do Taxidog:")
        if ok:
            taxidog = session.query(Taxidog).filter_by(id=id_taxidog).first()
            if taxidog:
                preco, ok_preco = QInputDialog.getDouble(self, "Atualizar Taxidog", "Preço:", QLineEdit.Normal, taxidog.preco)
                tempo_ida, ok_tempo_ida = QInputDialog.getInt(self, "Atualizar Taxidog", "Tempo de Ida:", QLineEdit.Normal, taxidog.tempo_ida)
                tempo_volta, ok_tempo_volta = QInputDialog.getInt(self, "Atualizar Taxidog", "Tempo de Volta:", QLineEdit.Normal, taxidog.tempo_volta)

                if ok_preco and ok_tempo_ida and ok_tempo_volta:
                    taxidog.preco = preco
                    taxidog.tempo_ida = tempo_ida
                    taxidog.tempo_volta = tempo_volta
                    session.commit()

    def deletar_taxidog(self):
        id_taxidog, ok = QInputDialog.getInt(self, "Deletar Taxidog", "Digite o ID do Taxidog para excluir:")
        if ok:
            taxidog = session.query(Taxidog).filter_by(id=id_taxidog).first()
            if taxidog:
                session.delete(taxidog)
                session.commit()

    def listar_taxidog(self):
        taxidogs = session.query(Taxidog).all()
        colunas = ['id', 'preco', 'tempo_ida', 'tempo_volta']
        self.exibir_dados(taxidogs, colunas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PetshopApp()
    sys.exit(app.exec_())
