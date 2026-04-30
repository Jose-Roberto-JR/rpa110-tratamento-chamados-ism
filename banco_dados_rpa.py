from config import RPA_BD_DRIVER, RPA_DB_NAME, RPA_DB_USER, RPA_DB_SERVER, RPA_DB_PWD, RPA_SHORT_NAME
import pyodbc


class BancoDadosRpa:
    def __init__(self):
        self.conn = pyodbc.connect(
            f'Driver={RPA_BD_DRIVER};'
            f'Server={RPA_DB_SERVER};'
            f'Database={RPA_DB_NAME};'
            f'UID={RPA_DB_USER};'
            f'PWD={RPA_DB_PWD};'
            f'Encrypt=no;'
            f'TrustServerCertificate=yes;')

        # Cria o cursor
        self.cursor = self.conn.cursor()

    def encerrar_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __exit__(self):
        self.encerrar_conexao()

    def iniciar_execucao(self, prontuario, atendimento_umc, cd_medico, setor, dt_liberacao, estabelecimento, nm_paciente) -> int:
        """
        Inserir informações no banco de dados do robô e pegar a sequência da execução.
        :return: Sequência da execução.
        """
        # Query da consulta no banco de dados
        query = f"""
            DECLARE @exec_seq INT;
            EXEC [{RPA_SHORT_NAME}].[VALIDACOES] 
                @PRONTUARIO = ?,
                @ATENDIMENTO_UMC = ?,
                @CD_MEDICO = ?,
                @SETOR = ?,
                @DT_LIBERACAO = ?,
                @ESTABELECIMENTO = ?,
                @NOME_PACIENTE = ?,
                @EXEC_SEQ = @exec_seq OUTPUT;
            SELECT @exec_seq;
        """

        # Executando a procedure
        dados = (
            prontuario, atendimento_umc, cd_medico, setor, dt_liberacao.strftime("%Y-%m-%d %H:%M:%S"), estabelecimento,
            nm_paciente
        )
        self.cursor.execute(query, dados)

        # Pegando os valores de retorno
        row = self.cursor.fetchone()
        exec_seq = int(row[0])

        # Salva as alterações
        self.conn.commit()

        return exec_seq

    def salvar_log_atendimentos(self, exec_seq, exec_status, exec_log, exec_cod_erro, atendimento_umi):
        """
        Salvar log dos atendimentos do banco de dados do RPA.
        """
        # Query para inserir log no banco de dados
        query = f"""
UPDATE {RPA_SHORT_NAME}.LOG_ATENDIMENTOS
SET 
    EXEC_STATUS = ?
    ,EXEC_LOG = ?
    ,EXEC_COD_ERRO = ?
    ,EXEC_FIM = GETDATE()
    ,ATENDIMENTO_UMI = ?
WHERE EXEC_SEQ = ?
        """

        # Executando o comando
        dados = (exec_status, exec_log, exec_cod_erro, atendimento_umi, exec_seq)
        self.cursor.execute(query, dados)

        # Salva as alterações
        self.conn.commit()

    def salvar_log_prescricoes(self, exec_status, exec_log, exec_cod_erro, exec_inicio, atendimento_umc,
                               nr_prescricao_umc, nr_prescricao_umi) -> None:
        """
        Salvar log das prescrições dos atendimentos do banco de dados do RPA.
        """
        query = f""" 
INSERT INTO {RPA_SHORT_NAME}.LOG_PRESCRICOES(
    EXEC_STATUS
    ,EXEC_LOG
    ,EXEC_COD_ERRO
    ,EXEC_INICIO
    ,EXEC_FIM
    ,ATENDIMENTO_UMC
    ,PRESCRICAO_UMC
    ,PRESCRICAO_UMI
) 
VALUES(
    ?
    ,?
    ,?
    ,?
    ,GETDATE()
    ,?
    ,?
    ,?
)
        """

        # Executando a consulta
        dados = (exec_status, exec_log, exec_cod_erro, exec_inicio.strftime("%Y-%m-%d %H:%M:%S"),
                 atendimento_umc, nr_prescricao_umc, nr_prescricao_umi)
        self.cursor.execute(query, dados)

        # Salva as alterações
        self.conn.commit()

    def salvar_log_exames(self, exec_status, exec_log, exec_cod_erro, exec_inicio, atendimento_umc, nr_prescricao,
                          cd_procedimento, nr_seq_proc_interno, topografia, contraste, lado) -> None:
        """
        Salvar log das exames no banco de dados do RPA.
        """
        query = f""" 
INSERT INTO {RPA_SHORT_NAME}.LOG_EXAMES(
    EXEC_STATUS
    ,EXEC_LOG
    ,EXEC_COD_ERRO
    ,EXEC_INICIO
    ,EXEC_FIM
    ,ATENDIMENTO_UMC
    ,PRESCRICAO_UMC
    ,CD_PROCEDIMENTO
    ,NR_SEQ_PROC_INTERNO
    ,TOPOGRAFIA
    ,CONTRASTE
    ,LADO
) 
VALUES(
    ?
    ,?
    ,?
    ,?
    ,GETDATE()
    ,?
    ,?
    ,?
    ,?
    ,?
    ,?
    ,?
)
        """

        # Executando a consulta
        dados = (exec_status, exec_log, exec_cod_erro, exec_inicio.strftime("%Y-%m-%d %H:%M:%S"), atendimento_umc,
                 nr_prescricao, cd_procedimento, nr_seq_proc_interno, topografia, contraste, lado)
        self.cursor.execute(query, dados)

        # Salva as alterações
        self.conn.commit()
