import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from io import StringIO
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="SIG E-commerce - Dashboard Gerencial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
:root{
  --accent:#1e3c72;
  --accent-2:#2a5298;
  --muted:#6b7280;
  --card-bg: rgba(255,255,255,0.85);
  --card-border: rgba(0,0,0,0.06);
}

/* Theme-aware text color */
:root { --text-color: #0b2545; }
[data-theme="dark"] { --text-color: #e6eef9; --card-bg: rgba(8,14,30,0.45); --card-border: rgba(255,255,255,0.06); }

.block-container {
  padding-top: 1.2rem;
  padding-left: 1.6rem;
  padding-right: 1.6rem;
  max-width: 1500px;
}

/* Top header */
.topbar {
  background: linear-gradient(90deg, var(--accent), var(--accent-2));
  color: white;
  padding: 16px;
  border-radius: 10px;
  box-shadow: 0 6px 18px rgba(20,30,60,0.08);
}

/* KPI Card */
.kpi-card {
  background: var(--card-bg);
  padding: 16px;
  border-radius: 10px;
  border: 1px solid var(--card-border);
  box-shadow: 0 6px 18px rgba(11,37,69,0.03);
  min-height: 100px;
}
.kpi-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 6px;
}
.kpi-value {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-color);
}

/* Insight styles */
.insight {
  padding: 14px;
  border-radius: 10px;
  margin-bottom: 10px;
  color: #0b2a3a;
  box-shadow: 0 4px 12px rgba(11,37,69,0.03);
}
.insight-success { background: linear-gradient(90deg,#e9f7ee,#dff2e6); border-left: 6px solid #28a745; }
.insight-warning { background: linear-gradient(90deg,#fff8e6,#fff2d9); border-left: 6px solid #ffc107; }
.insight-info { background: linear-gradient(90deg,#e9f6fb,#dff0f6); border-left: 6px solid #17a2b8; }
.insight-danger { background: linear-gradient(90deg,#fff0f0,#ffe6e8); border-left: 6px solid #dc3545; }

.section-title { color: var(--accent); font-weight:800; margin-bottom:8px; }
.small-muted { color: var(--muted); font-size:13px; }

</style>
""", unsafe_allow_html=True)

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove BOM, espaços e padroniza nomes para minúsculo.
    Ex.: "﻿order_id" -> "order_id"
    """
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )
    return df


def _normalize_number_str(s):
    """
    Normaliza strings numéricas no formato BR/EN para float.
    Exemplos:
     - "1.234,56" -> 1234.56
     - "1234,56"  -> 1234.56
     - "1234.56"  -> 1234.56
    """
    if pd.isna(s):
        return np.nan
    s = str(s).strip()
    if s == "":
        return np.nan
    if '.' in s and ',' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s and '.' not in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return np.nan


def carregar_csv_robusto(uploaded_file):
    """
    Lê CSV tentando encodings e separadores comuns.
    Retorna DataFrame com colunas normalizadas.
    """
    try:
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
    except Exception:
        uploaded_file.seek(0)
        df = None
        for enc in ['utf-8-sig', 'utf-8', 'latin1', 'iso-8859-1', 'cp1252']:
            for sep in [',', ';', '\t']:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=enc, sep=sep)
                    break
                except Exception:
                    continue
            if df is not None:
                break
        if df is None:
            uploaded_file.seek(0)
            content = uploaded_file.read()
            if isinstance(content, bytes):
                try:
                    content = content.decode('utf-8')
                except:
                    content = content.decode('latin1', errors='ignore')
            df = pd.read_csv(StringIO(content), sep=None, engine="python")

    df = _normalize_columns(df)

    if 'total_value' in df.columns:
        df['total_value'] = df['total_value'].apply(_normalize_number_str)
    if 'product_price' in df.columns:
        df['product_price'] = df['product_price'].apply(_normalize_number_str)
    if 'quantity' in df.columns:
        try:
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
        except Exception:
            df['quantity'] = df['quantity'].apply(lambda x: int(float(_normalize_number_str(x))) if not pd.isna(x) else 0)

    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    return df


def create_sample_data(n_records=1000):
    np.random.seed(42)
    categories = ['Eletrônicos', 'Moda', 'Casa e Decoração', 'Livros', 'Esportes', 'Beleza']
    states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE']
    cities_by_state = {
        'SP': ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto'],
        'RJ': ['Rio de Janeiro', 'Niterói'],
        'MG': ['Belo Horizonte', 'Uberlândia'],
        'RS': ['Porto Alegre', 'Caxias do Sul'],
        'PR': ['Curitiba', 'Londrina'],
        'SC': ['Florianópolis', 'Joinville'],
        'BA': ['Salvador', 'Feira de Santana'],
        'PE': ['Recife', 'Olinda'],
    }
    payment_methods = ['Cartão de Crédito', 'PIX', 'Boleto', 'Cartão de Débito']

    state_probs = np.array([0.35, 0.20, 0.12, 0.08, 0.06, 0.05, 0.08, 0.06])
    state_probs = state_probs / state_probs.sum()

    dates = pd.date_range(start='2024-01-01', end='2024-10-31').to_pydatetime().tolist()
    rows = []
    for i in range(n_records):
        state = np.random.choice(states, p=state_probs)
        city = np.random.choice(cities_by_state[state])
        cat = np.random.choice(categories)
        if cat == 'Eletrônicos':
            price = round(np.random.uniform(200, 3500), 2)
        elif cat == 'Moda':
            price = round(np.random.uniform(30, 700), 2)
        elif cat == 'Casa e Decoração':
            price = round(np.random.uniform(60, 1500), 2)
        elif cat == 'Livros':
            price = round(np.random.uniform(15, 120), 2)
        elif cat == 'Esportes':
            price = round(np.random.uniform(40, 900), 2)
        else:
            price = round(np.random.uniform(20, 400), 2)

        qty = int(np.random.randint(1, 5))
        total = round(price * qty, 2)
        datec = pd.Timestamp(np.random.choice(dates)).strftime('%Y-%m-%d')

        rows.append({
            'order_id': f'ORD_{i+1:06d}',
            'customer_id': f'CUST_{np.random.randint(1,2000):06d}',
            'order_date': datec,
            'product_category': cat,
            'product_price': price,
            'quantity': qty,
            'total_value': total,
            'customer_state': state,
            'customer_city': city,
            'payment_method': np.random.choice(payment_methods, p=[0.45,0.3,0.15,0.10])
        })

    df = pd.DataFrame(rows)
    df = _normalize_columns(df)
    df['total_value'] = df['total_value'].astype(float)
    df['product_price'] = df['product_price'].astype(float)
    df['quantity'] = df['quantity'].astype(int)
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df


def calcular_kpis(df: pd.DataFrame):
    """
    Calcula KPIs principais a partir do dataframe filtrado.
    Retorna dicionário com resultados e série mensal (period).
    """
    df = df.copy()
    if 'total_value' not in df.columns:
        df['total_value'] = 0.0
    if 'order_id' not in df.columns:
        df['order_id'] = range(1, len(df) + 1)

    total_orders = df['order_id'].nunique()
    total_revenue = df['total_value'].fillna(0).sum()
    total_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
    total_items = df['quantity'].sum() if 'quantity' in df.columns else 0
    avg_ticket = df.groupby('order_id')['total_value'].sum().mean() if total_orders > 0 else 0.0

    if 'order_date' in df.columns:
        df['period'] = pd.to_datetime(df['order_date']).dt.to_period('M').astype(str)
        monthly = df.groupby('period').agg(
            orders=('order_id', 'nunique'),
            revenue=('total_value', 'sum'),
            customers=('customer_id', 'nunique'),
            items=('quantity', 'sum')
        ).reset_index().sort_values('period')
        if len(monthly) >= 2:
            monthly['revenue_growth'] = monthly['revenue'].pct_change() * 100
            monthly['orders_growth'] = monthly['orders'].pct_change() * 100
        else:
            monthly['revenue_growth'] = 0
            monthly['orders_growth'] = 0
    else:
        monthly = pd.DataFrame(columns=['period','orders','revenue','customers','items'])

    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_customers': total_customers,
        'total_items': total_items,
        'avg_ticket': avg_ticket,
        'monthly': monthly,
        'df': df
    }


def generate_insights(kpis: dict, df: pd.DataFrame):
    """
    Gera lista de insights (tipo, título, texto) com regras simples.
    """
    insights = []
    monthly = kpis.get('monthly', pd.DataFrame())
    if len(monthly) >= 2:
        last = monthly.iloc[-1]['revenue']
        prev = monthly.iloc[-2]['revenue']
        if prev != 0:
            growth = (last - prev) / prev * 100
            if growth > 5:
                insights.append({'type':'success','title':'Crescimento','text':f'Crescimento de {growth:.1f}% na receita mês-a-mês.'})
            elif growth < -5:
                insights.append({'type':'danger','title':'Queda','text':f'Queda de {abs(growth):.1f}% na receita mês-a-mês.'})

    if 'customer_state' in df.columns and 'total_value' in df.columns:
        state_rev = df.groupby('customer_state')['total_value'].sum().sort_values(ascending=False)
        if len(state_rev) > 0:
            top_state = state_rev.index[0]
            share = (state_rev.iloc[0] / state_rev.sum()) * 100 if state_rev.sum() > 0 else 0
            if share > 35:
                insights.append({'type':'warning','title':'Concentração','text':f'{top_state} representa {share:.1f}% da receita. Alta dependência geográfica.'})

    if 'product_category' in df.columns:
        cat_rev = df.groupby('product_category')['total_value'].sum().sort_values(ascending=False)
        if len(cat_rev) > 0:
            top_cat = cat_rev.index[0]
            share = (cat_rev.iloc[0] / cat_rev.sum()) * 100 if cat_rev.sum() > 0 else 0
            insights.append({'type':'info','title':'Categoria Líder','text':f'"{top_cat}" gera {share:.1f}% da receita.'})

    if kpis.get('avg_ticket', 0) < 200:
        insights.append({'type':'danger','title':'Ticket Médio Baixo','text':f'Ticket médio R$ {kpis.get("avg_ticket",0):.2f}. Considere upsell.'})

    return insights

def main():
    st.markdown("""
    <div class="topbar">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h2 style='margin:0; color: white;'>
            📊 Sistema de Informações Gerenciais para E-commerce
          </h2>
          <div style="font-size:13px; opacity:0.95; color: rgba(255,255,255,0.92);">Dashboard Gerencial - SIG</div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:13px; color:rgba(255,255,255,0.9);">IFAL • 2025</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("⚙️ Configurações")
    st.sidebar.subheader("Fonte de Dados")
    data_option = st.sidebar.radio("Selecionar dataset", ["Usar dados de exemplo", "Upload de arquivo CSV"])

    company_name = "Empresa de Exemplo"
    if data_option == "Upload de arquivo CSV":
        st.sidebar.subheader("Informações da Empresa")
        company_name = st.sidebar.text_input("Nome da empresa", value="Empresa de Exemplo")

    df = None
    if data_option == "Usar dados de exemplo":
        if st.sidebar.button("Carregar dados de exemplo"):
            df = create_sample_data(1000)
            st.session_state['df'] = df
            st.session_state['company'] = company_name
            st.success("Dados de exemplo carregados.")
            st.rerun()
        else:
            if 'df' in st.session_state:
                df = st.session_state['df']
                company_name = st.session_state.get('company', company_name)
    else:
        uploaded_file = st.sidebar.file_uploader("Selecione o arquivo CSV", type=['csv'])
        if uploaded_file is not None:
            try:
                df = carregar_csv_robusto(uploaded_file)
                df = _normalize_columns(df)
                st.session_state['df'] = df
                st.session_state['company'] = company_name
                st.success("Arquivo carregado e processado.")
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
                st.stop()
        else:
            if 'df' in st.session_state:
                df = st.session_state['df']
                company_name = st.session_state.get('company', company_name)

    if df is None:
        st.info("Use a barra lateral para carregar um arquivo CSV ou carregar dados de exemplo.")
        return

    df = _normalize_columns(df)
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    else:
        st.error("Coluna obrigatória 'order_date' não encontrada no dataset.")
        st.stop()

    df = df[~df['order_date'].isna()].copy()
    if 'total_value' in df.columns:
        df['total_value'] = df['total_value'].apply(lambda x: _normalize_number_str(x) if not pd.api.types.is_numeric_dtype(type(x)) else x)
        df['total_value'] = pd.to_numeric(df['total_value'], errors='coerce').fillna(0.0)
    else:
        df['total_value'] = 0.0

    if 'product_price' in df.columns:
        df['product_price'] = df['product_price'].apply(lambda x: _normalize_number_str(x) if not pd.api.types.is_numeric_dtype(type(x)) else x)
        df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce').fillna(0.0)

    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0).astype(int)
    else:
        df['quantity'] = 0

    st.markdown(f"""
    <div style="margin-top:10px; margin-bottom:8px;">
        <h3 style="margin:0;">📈 Dashboard Gerencial - <span style="color:#1e3c72;">{company_name}</span></h3>
        <div class="small-muted">Período de dados: {df['order_date'].min().strftime('%d/%m/%Y')} a {df['order_date'].max().strftime('%d/%m/%Y')} | Registros: {len(df):,}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            min_date = df['order_date'].min().date()
            max_date = df['order_date'].max().date()
            date_range = st.date_input("Período:", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        with col2:
            states = sorted(df['customer_state'].dropna().unique().tolist()) if 'customer_state' in df.columns else []
            selected_states = st.multiselect("Estados:", options=states, default=states)

    try:
        start_date, end_date = date_range
    except:
        start_date = date_range
        end_date = date_range

    df_filtered = df[(df['order_date'] >= pd.to_datetime(start_date)) & (df['order_date'] <= pd.to_datetime(end_date))]
    if 'customer_state' in df_filtered.columns and selected_states:
        df_filtered = df_filtered[df_filtered['customer_state'].isin(selected_states)]

    k = calcular_kpis(df_filtered)

    st.markdown("### 📊 Indicadores Principais")
    col1, col2, col3, col4, col5 = st.columns(5)
    card_html = """
    <div style="
        background-color: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        min-height:90px;
    ">
        <div style="font-size: 18px; margin-bottom: 4px;">{icon} {title}</div>
        <div style="font-size: 22px; font-weight: 700; margin-top: 6px;">{value}</div>
    </div>
    """

    with col1:
        st.markdown(card_html.format(icon="🛒", title="Total de Pedidos", value=f"{k['total_orders']:,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(card_html.format(icon="💰", title="Receita Total", value=f"R$ {k['total_revenue']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), unsafe_allow_html=True)
    with col3:
        st.markdown(card_html.format(icon="👥", title="Clientes Únicos", value=f"{k['total_customers']:,}"), unsafe_allow_html=True)
    with col4:
        st.markdown(card_html.format(icon="📦", title="Itens Vendidos", value=f"{k['total_items']:,}"), unsafe_allow_html=True)
    with col5:
        st.markdown(card_html.format(icon="🎯", title="Ticket Médio", value=f"R$ {k['avg_ticket']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")), unsafe_allow_html=True)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução Temporal", "🏆 Produtos", "🗺️ Geografia", "💳 Pagamentos"])

    with tab1:
        st.subheader("📅 Evolução de Receita e Pedidos (Mensal)")
        monthly = k['monthly'].copy() if 'monthly' in k else pd.DataFrame()
        if len(monthly) == 0:
            st.info("Sem dados suficientes para mostrar séries temporais.")
        else:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=monthly['period'], y=monthly['orders'], name='Pedidos', marker_color='#1e3c72'), secondary_y=False)
            fig.add_trace(go.Scatter(x=monthly['period'], y=monthly['revenue'], name='Receita (R$)', mode='lines+markers', line=dict(color='#ff7f0e', width=3)), secondary_y=True)
            fig.update_layout(hovermode='x unified', height=420, legend=dict(orientation='h'))
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Pedidos por Dia")
        df_days = df_filtered.groupby(df_filtered['order_date'].dt.date).agg(revenue=('total_value','sum'), orders=('order_id','nunique')).reset_index()
        if len(df_days) == 0:
            st.info("Sem dados para mostrar por dia.")
        else:
            fig2 = px.line(df_days, x='order_date', y='revenue', labels={'order_date':'Data','revenue':'Receita (R$)'})
            fig2.update_traces(line_color='#0b6bf7', line_width=2)
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🏆 Performance por Categoria/Produto")
        if 'product_category' in df_filtered.columns:
            prod = df_filtered.groupby('product_category').agg(revenue=('total_value','sum'), orders=('order_id','nunique'), qty=('quantity','sum')).reset_index().sort_values('revenue', ascending=False)
            figp = px.bar(prod.head(8), x='revenue', y='product_category', orientation='h', labels={'revenue':'Receita','product_category':'Categoria'}, color='revenue', color_continuous_scale='Blues')
            figp.update_layout(height=420, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(figp, use_container_width=True)

            st.markdown("#### Tabela de categorias")
            prod_display = prod.copy()
            prod_display['revenue'] = prod_display['revenue'].map(lambda x: f"R$ {x:,.2f}")
            st.dataframe(prod_display.reset_index(drop=True), use_container_width=True)
        else:
            st.info("Coluna 'product_category' não encontrada.")

    with tab3:
        st.subheader("🗺️ Análise Geográfica")
        if 'customer_state' in df_filtered.columns:
            geo = df_filtered.groupby('customer_state').agg(revenue=('total_value','sum'), orders=('order_id','nunique')).reset_index().sort_values('revenue', ascending=False)
            figg = px.bar(geo.head(10), x='customer_state', y='revenue', labels={'customer_state':'Estado','revenue':'Receita (R$)'}, color='revenue', color_continuous_scale='Purples')
            figg.update_layout(height=420)
            st.plotly_chart(figg, use_container_width=True)
        else:
            st.info("Coluna 'customer_state' não encontrada.")

    with tab4:
        st.subheader("💳 Métodos de Pagamento")
        if 'payment_method' in df_filtered.columns:
            pay = df_filtered.groupby('payment_method').agg(orders=('order_id','nunique'), revenue=('total_value','sum')).reset_index().sort_values('orders', ascending=False)
            figpay = px.pie(pay, names='payment_method', values='orders', hole=0.45)
            figpay.update_traces(textposition='outside', textinfo='percent+label', pull=[0.05 if i==0 else 0 for i in range(len(pay))])
            st.plotly_chart(figpay, use_container_width=True)

            st.markdown("#### Receita por método")
            figpay2 = px.bar(pay, x='payment_method', y='revenue', labels={'revenue':'Receita (R$)','payment_method':'Método'}, color='revenue', color_continuous_scale='Greens')
            figpay2.update_layout(height=380, xaxis_tickangle=-45)
            st.plotly_chart(figpay2, use_container_width=True)
        else:
            st.info("Coluna 'payment_method' não encontrada.")

    st.markdown("---")
    st.markdown("### 🔎 Insights Automáticos")

    def insight_card(title, description, icon="💡", color="#1e3c72"):
        return f"""
        <div style="
            background: linear-gradient(135deg, rgba(30,60,114,0.12), rgba(42,82,152,0.12));
            border-left: 6px solid {color};
            padding: 18px 20px;
            border-radius: 14px;
            margin-bottom: 16px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            height: 100%;
        ">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="font-size: 32px;">{icon}</div>
                <div>
                    <div style="font-size: 18px; font-weight: 600; margin-bottom:4px;">{title}</div>
                    <div style="font-size: 14px; opacity: 0.85; line-height: 1.4;">{description}</div>
                </div>
            </div>
        </div>
        """

    if 'product_category' in df_filtered.columns:
        vc = df_filtered['product_category'].value_counts()
        top_cat = vc.index[0] if len(vc) > 0 else "N/A"
        count_top = int(vc.iloc[0]) if len(vc) > 0 else 0
        bottom_cat = vc.index[-1] if len(vc) > 0 else "N/A"
        count_bottom = int(vc.iloc[-1]) if len(vc) > 0 else 0
        concentration = (count_top / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        categories_count = df_filtered['product_category'].nunique()
    else:
        top_cat = bottom_cat = "N/A"
        count_top = count_bottom = 0
        concentration = 0
        categories_count = 0

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(insight_card("Categoria Líder de Vendas",
                                f"A categoria {top_cat} foi a mais vendida no período, com {count_top} vendas.",
                                icon="🏆", color="#4CAF50"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(insight_card("Categoria com Menor Desempenho",
                                f"A categoria {bottom_cat} teve o menor volume, com apenas {count_bottom} vendas.",
                                icon="📉", color="#E53935"),
                    unsafe_allow_html=True)
    with c1:
        st.markdown(insight_card("Concentração de Vendas",
                                f"A categoria líder representa {concentration:.1f}% de todas as vendas analisadas.",
                                icon="🎯", color="#FF9800"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(insight_card("Diversidade no Mix de Produtos",
                                f"O dataset possui {categories_count} categorias diferentes vendidas.",
                                icon="📦", color="#3F51B5"),
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='text-align:center;color:var(--muted)'>Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} • {company_name}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
