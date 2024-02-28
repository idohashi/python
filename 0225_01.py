import streamlit as st
import mysql.connector
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode
import os  # Importe a biblioteca 'os' para executar o arquivo Arq02.py
from sqlalchemy import create_engine

st.set_page_config(page_title="TESTE01_ABRIR_2_ARQS", page_icon=":smiley:", layout="wide")
st.title("Cliente")
st.markdown("<p style='text-align: center; font-family: Calibri; font-size: 10pt; color: green;'>Tamanho: wide; auto dimensionável; fundo dark; centralizado</p>", unsafe_allow_html=True)
# Função para conectar ao banco de dados
#def conectar_bd():clea
#    return mysql.connector.connect(host='localhost', user='root', password='Mari160571#', database='x_go')

def conectar_bd():
        # Substitua as informações de conexão com o banco de dados pelo seu próprio banco
        engine = create_engine("mysql+mysqlconnector://root:Mari160571#@localhost/x_go")
        return engine.connect()


    # Função para listar os registros
def listar_registros():
        conn = conectar_bd()
        #mydb = conectar_bd()
        query = '''
            SELECT 
                teste_2502.ORD AS 'ORD', 
                teste_2502.CLIE  AS 'CLIE', 
                teste_2502.ALIAS  AS 'ALIAS', 
                teste_2502.RAZ_SOC  AS 'RAZ_SOC', 
                teste_2502.ORC_NRO  AS 'ORC_NRO', 
                teste_2502.DATA  AS 'DATA', 
                teste_2502.QTDE1  AS 'QTDE1',  
                teste_2502.QTDE2  AS 'QTDE2',  
                teste_2502.VLR_UNIT  AS 'VLR_UNIT' ,  
                teste_2502.HON   AS 'HON'
                #[teste_2502.QTDE1] * [teste_2502.QTDE2] AS 'QTSE'
                FROM teste_2502
        '''
        #df = pd.read_sql(query, mydb)
        #mydb.close()
        #return df
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Formata a coluna 6 como data no formato brasileiro
        df['DATA'] = df['DATA'].dt.strftime('%d/%m/%Y')
       
        df['QTDE1'] = df['QTDE1'].apply(lambda x: f'{x:.4f}'.replace('.', ','))
        df['QTDE2'] = df['QTDE2'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
        df['VLR_UNIT'] = df['VLR_UNIT'].apply(lambda x: f'{x:.2f}'.replace('.', ','))
        return df
def var01(selected_rows):

        return f"Você clicou no registro com ID {selected_rows[0]['ORD']}"

# Divide a tela em 3 colunas
col1, col2, col3 = st.columns([8, 1, 1])

    # Função para exibir a tabela com os registros
def exibir_tabela(df):
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_selection(selection_mode="single", use_checkbox=True)
        #gb.configure_side_bar()
        gridOptions = gb.build()
        with col1:
            data = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, allow_unsafe_jscode=True,
                        update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        selected_rows = data["selected_rows"]
        if len(selected_rows) != 0:
                    st.write(f"Você clicou no registro com ID {selected_rows[0]['ORD']}")
                    st.write(f"<button onclick=\"window.open('http://localhost:8501/record?id={selected_rows[0]['ORD']}')\">Abrir registro</button>", unsafe_allow_html=True)
def main():
    df = listar_registros()
    exibir_tabela(df)
    st.markdown("---")

if __name__ == "__main__":
    main()
        
        
 