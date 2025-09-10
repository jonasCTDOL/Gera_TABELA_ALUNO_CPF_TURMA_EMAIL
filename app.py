import pandas as pd
import argparse
import sys
import streamlit as st

def gerar_tabela_alunos(arquivo_inscritos, arquivo_turmas, arquivo_saida):
def gerar_tabela_alunos(arquivo_inscritos, arquivo_turmas):
    """
    Cruza dados de inscritos e turmas, incluindo o e-mail, e gera um arquivo CSV.
    Cruza dados de inscritos e turmas a partir de arquivos CSV carregados.

    Args:
        arquivo_inscritos (str): Caminho para o arquivo CSV de inscritos.
        arquivo_turmas (str): Caminho para o arquivo CSV de turmas.
        arquivo_saida (str): Caminho para o arquivo CSV de saída.
        arquivo_inscritos (UploadedFile): Arquivo CSV de inscritos carregado via Streamlit.
        arquivo_turmas (UploadedFile): Arquivo CSV de turmas carregado via Streamlit.

    Returns:
        pandas.DataFrame: O DataFrame final com os dados combinados.

    Raises:
        KeyError: Se as colunas necessárias não forem encontradas nos arquivos.
        Exception: Para outros erros de processamento.
    """
    try:
        # Validação de colunas essenciais
        colunas_inscritos = ['Nome completo', 'CPF', 'Endereço de email']
        colunas_turmas = ['Nome completo', 'Nome curto do curso']

        # Carrega os arquivos CSV
        # Carrega os arquivos CSV a partir dos objetos carregados
        df_inscritos = pd.read_csv(arquivo_inscritos)
        df_turmas = pd.read_csv(arquivo_turmas)

        # Verifica se as colunas necessárias existem
        if not all(col in df_inscritos.columns for col in colunas_inscritos):
            raise KeyError(f"O arquivo '{arquivo_inscritos}' não contém as colunas necessárias: {colunas_inscritos}")
            raise KeyError(f"O arquivo de inscritos não contém as colunas necessárias: {colunas_inscritos}")
        if not all(col in df_turmas.columns for col in colunas_turmas):
            raise KeyError(f"O arquivo '{arquivo_turmas}' não contém as colunas necessárias: {colunas_turmas}")
            raise KeyError(f"O arquivo de turmas não contém as colunas necessárias: {colunas_turmas}")

        # Junta os dois dataframes
        df_merged = pd.merge(df_inscritos, df_turmas, on='Nome completo', how='inner')

        # Seleciona e renomeia as colunas
        tabela_final = df_merged[colunas_inscritos + ['Nome curto do curso']]
        tabela_final.columns = ['aluno', 'cpf', 'email', 'turma']

        # Salva e exibe a tabela final
        tabela_final.to_csv(arquivo_saida, index=False)
        print(f"Tabela final gerada com sucesso em '{arquivo_saida}'!")
        print(tabela_final)
        return tabela_final

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado - {e.filename}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)
        # Re-levanta a exceção para ser tratada pela interface do Streamlit
        raise e

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
# --- Interface do Streamlit ---

    args = parser.parse_args()
st.set_page_config(page_title="Gerador de Tabela de Alunos", layout="wide")
st.title("Gerador de Tabela Aluno/Turma")
st.write("Faça o upload dos arquivos CSV de inscritos e turmas para gerar a tabela final.")

    gerar_tabela_alunos(args.inscritos, args.turmas, args.saida)
# File Uploaders na barra lateral
st.sidebar.header("1. Carregar Arquivos")
uploaded_inscritos = st.sidebar.file_uploader("Arquivo de Inscritos (CSV)", type=['csv'])
uploaded_turmas = st.sidebar.file_uploader("Arquivo de Turmas (CSV)", type=['csv'])

if uploaded_inscritos and uploaded_turmas:
    st.sidebar.success("Arquivos carregados com sucesso!")

    if st.button("Gerar Tabela Final"):
        try:
            with st.spinner("Processando os dados..."):
                # Chama a função com os arquivos carregados
                tabela_final_df = gerar_tabela_alunos(uploaded_inscritos, uploaded_turmas)

            st.header("Resultado")
            st.dataframe(tabela_final_df)

            # Converte o DataFrame para CSV para o download
            csv = tabela_final_df.to_csv(index=False).encode('utf-8')

            st.download_button(
               label="Baixar tabela como CSV",
               data=csv,
               file_name='tabela_final.csv',
               mime='text/csv',
            )

        except KeyError as e:
            st.error(f"Erro de Coluna: {e}. Verifique se os arquivos CSV contêm as colunas necessárias.")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")
else:
    st.info("Por favor, carregue ambos os arquivos CSV na barra lateral para começar.")
