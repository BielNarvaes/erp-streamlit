import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def fluxo_caixa():
    query = "SELECT strftime('%Y-%m', data) AS mes, tipo, SUM(valor) as total FROM lancamentos GROUP BY mes, tipo"
    df = pd.read_sql_query(query, conn)
    
    df_pivot = df.pivot(index='mes', columns='tipo', values='total').fillna(0)
    
    st.write("Fluxo de Caixa por Mês")
    st.dataframe(df_pivot)  # Exibe os dados em formato de tabela
    
    df_pivot.plot(kind='bar', stacked=False)
    st.pyplot()

def distribuicao_fornecedores():
    query = "SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor"
    df = pd.read_sql_query(query, conn)
    
    st.write("Distribuição das Contas a Pagar por Fornecedor")
    st.dataframe(df)  # Exibe a tabela com os fornecedores e seus valores totais
    
    df.set_index('fornecedor', inplace=True)
    df.plot.pie(y='total', legend=False, autopct='%1.1f%%', figsize=(8, 8))
    st.pyplot()

def status_contas():
    query_pagar = "SELECT status, COUNT(*) as quantidade FROM contas_pagar GROUP BY status"
    df_pagar = pd.read_sql_query(query_pagar, conn)
    
    query_receber = "SELECT status, COUNT(*) as quantidade FROM contas_receber GROUP BY status"
    df_receber = pd.read_sql_query(query_receber, conn)
    
    st.write("Status das Contas a Pagar e Receber")
    
    st.subheader("Contas a Pagar")
    df_pagar.set_index('status', inplace=True)
    df_pagar.plot(kind='bar', legend=False, color=['#FF6347', '#4682B4'], figsize=(8, 6))
    st.pyplot()
    
    st.subheader("Contas a Receber")
    df_receber.set_index('status', inplace=True)
    df_receber.plot(kind='bar', legend=False, color=['#FF6347', '#4682B4'], figsize=(8, 6))
    st.pyplot()

def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Fluxo de Caixa", "Distribuição Fornecedores", "Status das Contas", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    
    if choice == "Fluxo de Caixa":
        fluxo_caixa()
    elif choice == "Distribuição Fornecedores":
        distribuicao_fornecedores()
    elif choice == "Status das Contas":
        status_contas()
    else:
        st.subheader("Relatórios")
        df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
        st.dataframe(df)
    
    conn.close()

if __name__ == "__main__":
    main()
