import pandas as pd
import argparse
import sys

def gerar_tabela_alunos(arquivo_inscritos, arquivo_turmas, arquivo_saida):
    """
    Cruza dados de inscritos e turmas, incluindo o e-mail, e gera um arquivo CSV.

    Args:
        arquivo_inscritos (str): Caminho para o arquivo CSV de inscritos.
        arquivo_turmas (str): Caminho para o arquivo CSV de turmas.
        arquivo_saida (str): Caminho para o arquivo CSV de saída.
    """
    try:
        # Validação de colunas essenciais
        colunas_inscritos = ['Nome completo', 'CPF', 'Endereço de email']
        colunas_turmas = ['Nome completo', 'Nome curto do curso']

        # Carrega os arquivos CSV
        df_inscritos = pd.read_csv(arquivo_inscritos)
        df_turmas = pd.read_csv(arquivo_turmas)

        # Verifica se as colunas necessárias existem
        if not all(col in df_inscritos.columns for col in colunas_inscritos):
            raise KeyError(f"O arquivo '{arquivo_inscritos}' não contém as colunas necessárias: {colunas_inscritos}")
        if not all(col in df_turmas.columns for col in colunas_turmas):
            raise KeyError(f"O arquivo '{arquivo_turmas}' não contém as colunas necessárias: {colunas_turmas}")

        # Junta os dois dataframes
        df_merged = pd.merge(df_inscritos, df_turmas, on='Nome completo', how='inner')

        # Seleciona e renomeia as colunas
        tabela_final = df_merged[colunas_inscritos + ['Nome curto do curso']]
        tabela_final.columns = ['aluno', 'cpf', 'email', 'turma']

        # Salva e exibe a tabela final
        tabela_final.to_csv(arquivo_saida, index=False)
        print(f"Tabela final gerada com sucesso em '{arquivo_saida}'!")
        print(tabela_final)

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e.filename}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gera uma tabela final de alunos, CPFs, e-mails e turmas a partir de arquivos CSV."
    )
    parser.add_argument(
        '--inscritos',
        type=str,
        default='inscritos.csv',
        help='Caminho para o arquivo CSV de inscritos. Padrão: inscritos.csv'
    )
    parser.add_argument(
        '--turmas',
        type=str,
        default='turmas.csv',
        help='Caminho para o arquivo CSV de turmas. Padrão: turmas.csv'
    )
    parser.add_argument(
        '--saida',
        type=str,
        default='tabela_final.csv',
        help='Caminho para o arquivo CSV de saída. Padrão: tabela_final.csv'
    )

    args = parser.parse_args()

    gerar_tabela_alunos(args.inscritos, args.turmas, args.saida)
