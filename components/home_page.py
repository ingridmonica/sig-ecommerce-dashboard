# components/home_page.py

import streamlit as st

def render_home_page():
    """Renderiza a página inicial com instruções"""
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <p style="font-size: 1.2em; color: #6b7280; margin-bottom: 30px;">
            Análise completa de dados de e-commerce com insights automáticos
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Funcionalidades do Sistema")
    
    col1, col2= st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgb(18 48 185) 0%, rgb(118, 75, 162) 100%); 
                    padding: 20px; border-radius: 10px; color: white; height: 280px;">
            <h3 style="margin-top: 0;">📊 Análises Completas</h3>
            <ul style="line-height: 1.8;">
                <li>KPIs em tempo real</li>
                <li>Evolução temporal</li>
                <li>Análise geográfica</li>
                <li>Performance de produtos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgb(132 36 143) 0%, rgb(245, 87, 108) 100%);
                    padding: 20px; border-radius: 10px; color: white; height: 280px;">
            <h3 style="margin-top: 0;">💡 Insights Automáticos</h3>
            <ul style="line-height: 1.8;">
                <li>Crescimento/queda</li>
                <li>Oportunidades</li>
                <li>Alertas estratégicos</li>
                <li>Recomendações</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    

    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("## Como Começar")
    
    st.info("""
    **<- Use a barra lateral** para escolher entre:
    - 📂 **Upload de arquivo CSV** - Envie seus próprios dados
    - 🎲 **Dados de exemplo** - Experimente com dados de demonstração
    """)
    
    st.markdown("## Exemplo de Estrutura CSV")
    
    st.markdown("""
    Seu arquivo CSV deve conter as seguintes colunas (os nomes são case-insensitive):
    """)
    
    exemplo_df = {
        'order_id': ['ORD_000001', 'ORD_000002', 'ORD_000003'],
        'customer_id': ['CUST_000123', 'CUST_000456', 'CUST_000789'],
        'order_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'product_category': ['Eletrônicos', 'Moda', 'Casa e Decoração'],
        'product_price': ['1299.90', '250.50', '450.00'],
        'quantity': ['2', '1', '3'],
        'total_value': ['2599.80', '250.50', '1350.00'],
        'customer_state': ['SP', 'RJ', 'MG'],
        'customer_city': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte'],
        'payment_method': ['PIX', 'Cartão de Crédito', 'Boleto']
    }
    
    import pandas as pd
    exemplo_table = pd.DataFrame(exemplo_df)
    st.dataframe(exemplo_table, use_container_width=True)
    
    with st.expander("📖 Descrição das Colunas", expanded=False):
        st.markdown("""
        | Coluna | Tipo | Descrição | Exemplo |
        |--------|------|-----------|---------|
        | `order_id` | Texto | Identificador único do pedido | ORD_000001 |
        | `customer_id` | Texto | Identificador único do cliente | CUST_000123 |
        | `order_date` | Data | Data do pedido (YYYY-MM-DD ou DD/MM/YYYY) | 2024-01-15 |
        | `product_category` | Texto | Categoria do produto | Eletrônicos |
        | `product_price` | Número | Preço unitário do produto | 1299.90 |
        | `quantity` | Inteiro | Quantidade de itens | 2 |
        | `total_value` | Número | Valor total do pedido | 2599.80 |
        | `customer_state` | Texto | Estado do cliente (UF) | SP |
        | `customer_city` | Texto | Cidade do cliente | São Paulo |
        | `payment_method` | Texto | Forma de pagamento | PIX |
        
        **Observações importantes:**
        - Use vírgula (`,`) como separador de colunas
        - Números podem usar ponto (`.`) ou vírgula (`,`) como decimal
        - O sistema aceita UTF-8, Latin1 e outros encodings comuns
        - Colunas obrigatórias: `order_id`, `order_date`, `total_value`
        """)
    
    st.markdown("### Baixar CSV de Exemplo")
    
    csv_exemplo = """order_id,customer_id,order_date,product_category,product_price,quantity,total_value,customer_state,customer_city,payment_method
ORD_000001,CUST_000123,2024-01-15,Eletrônicos,1299.90,2,2599.80,SP,São Paulo,PIX
ORD_000002,CUST_000456,2024-01-16,Moda,250.50,1,250.50,RJ,Rio de Janeiro,Cartão de Crédito
ORD_000003,CUST_000789,2024-01-17,Casa e Decoração,450.00,3,1350.00,MG,Belo Horizonte,Boleto
ORD_000004,CUST_000234,2024-01-18,Livros,45.90,2,91.80,RS,Porto Alegre,PIX
ORD_000005,CUST_000567,2024-01-19,Esportes,320.00,1,320.00,PR,Curitiba,Cartão de Débito"""
    
    st.download_button(
        label="📥 Baixar exemplo.csv",
        data=csv_exemplo,
        file_name="exemplo_ecommerce.csv",
        mime="text/csv",
        help="Clique para baixar um arquivo CSV de exemplo"
    )
    
    st.markdown("## 💡 Dicas de Uso")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ Boas Práticas:**
        - Mantenha dados consistentes
        - Use formato de data padrão
        - Evite células vazias
        - Nomeie categorias claramente
        """)
    
    with col2:
        st.warning("""
        **⚠️ Evite:**
        - Caracteres especiais em IDs
        - Datas em formatos mistos
        - Valores negativos sem motivo
        - Duplicação de order_id
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 20px;">
        <p>📚 <strong>Desenvolvido para o curso de Sistemas de Informação</strong></p>
        <p>IFAL • Instituto Federal de Alagoas • 2025</p>
    </div>
    """, unsafe_allow_html=True)