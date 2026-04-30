from dotenv import load_dotenv
import socket
import os

load_dotenv()

# Se AMBIENTE_PRODUCAO = True o robô usará todos os sistemas em ambiente de produção
AMBIENTE_PRODUCAO = True if 'aws-' in socket.gethostname().lower() else False

# Se headless = True o robô não exibirá o navegador durante a execução
HEADLESS = True if AMBIENTE_PRODUCAO else False

# Dados do RPA
RPA_SHORT_NAME = 'RPA110'
RPA_FULL_NAME = 'RPA110_TRATAMENTO_CHAMADOS_ISM'
if AMBIENTE_PRODUCAO:
    RPA_DIR = fr'{os.getenv("DIR_RPA")}/{RPA_FULL_NAME}'
else:
    RPA_DIR = fr'\\192.168.31.19\DADOS_CSO$\RPA\{RPA_FULL_NAME}'
RPA_DIR_PRINT = os.path.join(RPA_DIR, 'PRINTS')
RPA_DIR_FILES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files')
RPA_DIR_DOWNLOADS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')

# Informações referente ao banco de dados do RPA
if AMBIENTE_PRODUCAO:
    RPA_BD_DRIVER = "{ODBC Driver 18 for SQL Server}"
    RPA_DB_SERVER = '10.27.10.37'
else:
    RPA_BD_DRIVER = "{SQL Server}"
    RPA_DB_SERVER = '10.27.10.59'

RPA_DB_NAME = 'RPA'
RPA_DB_USER = os.getenv('RPA_DB_USER')
RPA_DB_PWD = os.getenv('RPA_DB_PWD')

# Variáveis do Fluig Identity
if AMBIENTE_PRODUCAO:
    FLUIG_URL = "https://oncoclinicas.fluigidentity.com"
else:
    FLUIG_URL = "https://oncoclinicas.customerfi.com"

FLUIG_USER = os.getenv('FLUIG_USER')
FLUIG_PWD = os.getenv('FLUIG_PWD')

LOG_FALHA = "Falha"
LOG_SUCESSO = "Sucesso"
LOG_MESSAGES = {
    "pegar_backlog": "Falha ao pegar o backlog no banco de dados do Tasy. ",
    "iniciar_execucao": "Falha ao gravar dados de início da execução no banco de dados do robô. ",
    "salvar_log_atendimentos": "Falha ao salvar log do atendimento no banco de dados do robô. ",
    "salvar_log_prescricoes": "Falha ao salvar log da prescrição no banco de dados do robô. ",
    "salvar_log_exames": "Falha ao salvar log do exame no banco de dados do robô. ",
    "login": "Falha ao realizar login no Tasy. ",
    "trocar_estabelecimento": "Falha ao trocar o estabelecimento. ",
    "executar_funcao": "Falha ao executar a função do tasy. ",
    "pesquisar_prontuario": "Falha ao pesquisar pela prontuário no Tasy. ",
    "adicionar_atendimento": "Falha ao adicionar o atendimento. ",
    "atualizar_convenio": "Falha ao atualizar o convênio. ",
    "adicionar_setor": "Falha ao adicionar o setor do atendimento. ",
    "pegar_prescricoes": "Falha ao pegar as prescrições do atendimento do banco de dados do Tasy. ",
    "adicionar_prescricao": "Falha ao adicionar a prescrição. ",
    "liberar_prescricao": "Falha liberar a prescrição. ",
    "pegar_exames": "Falha ao pegar os exames da prescrição do banco de dados do Tasy. ",
    "adicionar_exame": "Falha ao adicionar o exame. "
}
