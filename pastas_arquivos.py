from config import RPA_DIR_PRINT
from datetime import datetime
import os


def limpar_pasta_prints(quantidade_dias: int = 15):
    """
    Exclui os arquivos da pasta de prints do robô.
    :param quantidade_dias: Arquivos com mais de 'quantidade_dias' serão excluídos.
    """
    try:
        # Pegar a data de hoje
        hoje = datetime.today().date()

        # Loop por todos os arquivos da pasta de prints, em ordem decrescente
        for arquivo in os.listdir(RPA_DIR_PRINT):
            # Pega o caminho completo do arquivo
            caminho_arquivo = os.path.join(RPA_DIR_PRINT, arquivo)
            # Se certifica que não se trata de um arquivo temporário
            if os.path.isfile(caminho_arquivo):
                # Pega a data de criação do arquivo
                data_criacao_arquivo = datetime.fromtimestamp(os.stat(caminho_arquivo).st_mtime).date()
                # Se maior que "quantidade_dias" dias, exclui o arquivo
                if (hoje - data_criacao_arquivo).days > quantidade_dias:
                    os.remove(caminho_arquivo)
                else:
                    break
    except Exception as error:
        print(str(error))
