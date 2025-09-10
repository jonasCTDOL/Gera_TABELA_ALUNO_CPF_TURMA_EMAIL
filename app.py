# -*- coding: utf-8 -*-
"""
Script Python para uma aplicação web com Streamlit para processar um arquivo de texto
no formato específico CIAI.
"""

import streamlit as st # Importa a biblioteca principal do Streamlit para criar a interface web
import pandas as pd # Importa a biblioteca pandas para manipulação e análise de dados tabulares (DataFrames)
import re # Importa a biblioteca re para trabalhar com expressões regulares, usadas na extração de dados
from typing import Optional, List, Tuple # Importa tipos para anotações de tipo

# --- Constantes ---
# Definir constantes para nomes de colunas e arquivos melhora a manutenibilidade.
COLUMNS = ['GRUPO', 'CPF', 'NOME']
OUTPUT_FILENAME = "dados_extraidos.csv"

# --- Padrões de Expressão Regular ---
# Compilar os padrões de regex uma vez no nível do módulo melhora a performance,
# pois evita a recompilação a cada chamada da função.
# r'^([\w-]+)\t': Captura o GRUPO no início da linha, seguido por um TAB.
GRUPO_PATTERN = re.compile(r'^([\w-]+)\t')
# r'([^,]+?)\s*\.\s*\(\s*(\d+),': Captura NOME e CPF em pares.
NOME_CPF_PATTERN = re.compile(r'([^,]+?)\s*\.\s*\(\s*(\d+),')

# --- Configurações da página Streamlit ---
# Define as configurações iniciais da página web, como o título que aparece na aba do navegador
# e o layout (wide usa a largura total da tela).
st.set_page_config(page_title="Processador de Arquivo CIAI", layout="wide")

# --- Título e Descrição da Aplicação na Interface ---
# Adiciona um título principal à aplicação exibida na página web.
st.title("Processador de Arquivo CIAI")
# Adiciona um texto descritivo abaixo do título, explicando o propósito da aplicação.
st.markdown("""
    Esta aplicação processa arquivos de texto no formato específico CIAI,
    extraindo informações de GRUPO, CPF e NOME, formatando o CPF e gerando um arquivo CSV.
    Por favor, carregue o arquivo .txt para iniciar o processamento.
""")


# --- Função Principal de Processamento dos Dados ---
# Define a função que contém a lógica para ler, extrair e formatar os dados do arquivo.
def process_ciai_data(file_content: str) -> pd.DataFrame:
    """
    Processa o conteúdo de um arquivo de texto, extrai dados relevantes,
    formata o CPF e retorna um DataFrame pandas.

    Args:
        file_content (str): Uma string contendo o conteúdo completo do arquivo de texto.

    Returns:
        pd.DataFrame: Um DataFrame pandas com os dados extraídos. Pode estar vazio se nenhum dado for encontrado.
    """
    lines = file_content.splitlines()

    # --- Extração dos Dados Usando Expressões Regulares ---
    extracted_data: List[Tuple[str, str, str]] = []

    # Itera sobre cada linha lida do arquivo para processamento.
    for line in lines:
        # Tenta encontrar o padrão do GRUPO no início da linha atual.
        grupo_match = GRUPO_PATTERN.search(line)

        # Se um GRUPO for encontrado nesta linha:
        if grupo_match:
            grupo = grupo_match.group(1)
            rest_of_line = line[grupo_match.end():]

            # Encontra todas as ocorrências de NOME e CPF no restante da linha.
            for nome_cpf_match in NOME_CPF_PATTERN.finditer(rest_of_line):
                nome = nome_cpf_match.group(1).strip()
                cpf = nome_cpf_match.group(2).strip()
                
                # Formatação do CPF e adição à lista em um único passo
                formatted_cpf = cpf.zfill(11)
                extracted_data.append((grupo, formatted_cpf, nome))

    return pd.DataFrame(extracted_data, columns=COLUMNS)


# --- Interface Streamlit: Componentes Interativos ---

# Inicializa o estado da sessão para armazenar o DataFrame processado
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None

uploaded_file = st.file_uploader("Passo 1: Carregue o arquivo .txt", type=["txt"])

status_message_placeholder = st.empty()

# --- Lógica de Fluxo da Aplicação ---
# Verifica se um arquivo foi carregado pelo usuário.
if uploaded_file is not None:
    # Se um arquivo foi carregado, exibe uma mensagem informativa usando o placeholder de status.
    status_message_placeholder.info(f"Arquivo **'{uploaded_file.name}'** carregado. Clique em 'Processar' para continuar.")

    # Adiciona um botão à interface com o rótulo "Processar".
    if st.button("Passo 2: Processar Arquivo"):
        with st.spinner("Processando dados... Aguarde."):
            try:
                # Tenta decodificar com UTF-8, mas oferece fallback para latin-1
                file_content = uploaded_file.getvalue().decode("utf-8")
            except UnicodeDecodeError:
                st.warning("Não foi possível decodificar o arquivo como UTF-8. Tentando com Latin-1...")
                try:
                    file_content = uploaded_file.getvalue().decode("latin-1")
                except Exception as e:
                    st.error(f"Falha ao ler o arquivo. Codificação não suportada. Erro: {e}")
                    file_content = None
            
            if file_content:
                st.session_state.df_processed = process_ciai_data(file_content)

                if st.session_state.df_processed.empty:
                    status_message_placeholder.warning("Processamento concluído, mas nenhum dado foi extraído. Verifique o formato do arquivo de entrada.")
                else:
                    status_message_placeholder.success(f"Dados processados com sucesso! {len(st.session_state.df_processed)} registros encontrados.")

# Exibe os resultados se o DataFrame estiver no estado da sessão
if st.session_state.df_processed is not None and not st.session_state.df_processed.empty:
    st.subheader("Passo 3: Dados Extraídos e Formatados:")
    st.dataframe(st.session_state.df_processed)

    # Garante que o CSV seja gerado com codificação UTF-8 para máxima compatibilidade
    csv_output = st.session_state.df_processed.to_csv(index=False, encoding='utf-8')

    st.download_button(
        label="Passo 4: Baixar CSV Processado",
        data=csv_output,
        file_name=OUTPUT_FILENAME,
        mime="text/csv"
    )
elif uploaded_file is None:
    status_message_placeholder.info("Aguardando o upload do arquivo .txt.")