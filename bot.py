from banco_dados_rpa import BancoDadosRpa
from logs import salvar_log_erro
from config import LOG_SUCESSO
import pastas_arquivos as pa
from fluig import Fluig
import signal


execucao_interrompida = False

def finalizar_execucao(signum, frame):
    global execucao_interrompida
    print("Comando de finalização da execução recebido.")
    execucao_interrompida = True

# Registrar o manipulador para SIGTERM (sinal padrão do Cronicle)
signal.signal(signal.SIGTERM, finalizar_execucao)


def main():

    global execucao_interrompida
    pa.limpar_pasta_prints()

    fluig = None
    bd_rpa = None

    try:
        atendimentos = bd_tasy.pegar_backlog()
        if atendimentos:
            fluig = Fluig()
            fluig.login()
            bd_rpa = BancoDadosRpa()

        for atend in atendimentos:

            if execucao_interrompida:
                print("Execução interrompida.")
                break

            # Set de variáveis
            exec_seq = exec_log = exec_cod_erro = atendimento_umi = ""
            exec_status = LOG_SUCESSO
            prontuario = atend[0]

            try:
                # Salvar dados de execução no banco de dados do robô
                exec_seq = bd_rpa.iniciar_execucao(
                    prontuario=prontuario, atendimento_umc=atendimento_umc, cd_medico=cd_medico, setor=setor,
                    dt_liberacao=dt_liberacao, estabelecimento=estabelecimento, nm_paciente=nm_paciente
                )
                if exec_seq == 0:
                    print(f"Atendimento ({atendimento_umc}) processado com falha mais de 3 vezes")
                    continue

            except:
                exec_status, exec_log, exec_cod_erro = salvar_log_erro(bot=fluig.driver)

            finally:
                bd_rpa.salvar_log_atendimentos(
                    exec_seq=exec_seq, exec_status=exec_status, exec_log=exec_log,
                    exec_cod_erro=exec_cod_erro, atendimento_umi=atendimento_umi
                )
                fluig.driver.refresh()  # Voltar para a tela inicial

    finally:
        if fluig:
            fluig.stop_browser()
        if bd_rpa:
            bd_rpa.encerrar_conexao()


if __name__ == '__main__':
    main()
