import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import io
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="SIG E-commerce - Dashboard Gerencial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Header com gradiente azul empresarial */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Cards de métricas com bordas coloridas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Insights coloridos conforme protótipo */
    .insight-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .insight-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .insight-info {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .insight-danger {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* Área de upload */
    .upload-box {
        border: 2px dashed #1e3c72;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        margin: 1rem 0;
    }
    
    /* Status badges */
    .status-ok {
        background: #28a745;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    
    .status-error {
        background: #dc3545;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    
    /* Títulos de seção */
    .section-title {
        color: #1e3c72;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 3px solid #1e3c72;
        padding-bottom: 0.5rem;
    }
    
    /* Card de histórico */
    .history-card {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #17a2b8;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

class EcommerceSIG:
    """
    Sistema de Informações Gerenciais para E-commerce
    Versão completa com funcionalidades empresariais
    """
    
    def __init__(self):
        self.data = None
        self.company_name = "Empresa"
        self.data_period = ""
        self.upload_history = []
        
    def validate_csv_format(self, df):
        """Valida se o CSV está no formato esperado"""
        required_columns = [
            'order_id', 'customer_id', 'order_date', 'product_category', 
            'product_price', 'quantity', 'total_value', 'customer_state', 
            'customer_city', 'payment_method'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return False, f"❌ Colunas obrigatórias ausentes: {', '.join(missing_columns)}"
        
        return True, "✅ Formato válido"
    
    def load_data(self, uploaded_file, company_name="Empresa"):
        """Carrega dados do arquivo CSV com suporte a múltiplos encodings"""
        try:
            encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
            separators = [',', ';', '\t']
            
            df = None
            for encoding in encodings:
                for sep in separators:
                    try:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding=encoding, sep=sep)
                        if len(df.columns) >= 10:  # Verificar se tem colunas suficientes
                            break
                    except:
                        continue
                if df is not None and len(df.columns) >= 10:
                    break
            
            if df is None:
                return False, "❌ Não foi possível ler o arquivo. Verifique o formato."
            
            self.data = df
            self.company_name = company_name
            
            # Validar formato
            is_valid, message = self.validate_csv_format(self.data)
            if not is_valid:
                return False, message
            
            # Processar dados
            self.data['order_date'] = pd.to_datetime(self.data['order_date'], errors='coerce')
            
            # Remover datas inválidas
            invalid_count = self.data['order_date'].isna().sum()
            if invalid_count > 0:
                self.data = self.data.dropna(subset=['order_date'])
                st.warning(f"⚠️ {invalid_count} registros com datas inválidas foram removidos")
            
            # Criar colunas temporais
            self.data['year'] = self.data['order_date'].dt.year
            self.data['month'] = self.data['order_date'].dt.month
            self.data['month_name'] = self.data['order_date'].dt.strftime('%B')
            self.data['year_month'] = self.data['order_date'].dt.to_period('M').astype(str)
            self.data['weekday'] = self.data['order_date'].dt.day_name()
            self.data['day'] = self.data['order_date'].dt.day
            self.data['quarter'] = self.data['order_date'].dt.quarter
            
            # Definir período dos dados
            min_date = self.data['order_date'].min()
            max_date = self.data['order_date'].max()
            self.data_period = f"{min_date.strftime('%d/%m/%Y')} a {max_date.strftime('%d/%m/%Y')}"
            
            # Adicionar ao histórico
            self.upload_history.append({
                'timestamp': datetime.now(),
                'company': company_name,
                'records': len(self.data),
                'period': self.data_period,
                'status': 'OK'
            })
            
            return True, f"✅ {len(self.data):,} registros carregados com sucesso!"
            
        except Exception as e:
            self.upload_history.append({
                'timestamp': datetime.now(),
                'company': company_name,
                'records': 0,
                'period': '-',
                'status': 'ERRO'
            })
            return False, f"❌ Erro ao processar arquivo: {str(e)}"
    
    def calculate_kpis(self, start_date=None, end_date=None, selected_states=None):
        """Calcula KPIs principais com filtros opcionais"""
        df = self.data.copy()
        
        if start_date and end_date:
            df = df[(df['order_date'] >= pd.to_datetime(start_date)) & 
                    (df['order_date'] <= pd.to_datetime(end_date))]
        
        if selected_states and len(selected_states) > 0:
            df = df[df['customer_state'].isin(selected_states)]
        
        # KPIs 
        total_orders = df['order_id'].nunique()
        total_revenue = df['total_value'].sum()
        total_customers = df['customer_id'].nunique()
        total_items = df['quantity'].sum()
        avg_ticket = df.groupby('order_id')['total_value'].sum().mean() if total_orders > 0 else 0
        
        # Taxa de recorrência
        customer_orders = df.groupby('customer_id')['order_id'].nunique()
        recurring_customers = (customer_orders > 1).sum()
        recurrence_rate = (recurring_customers / total_customers * 100) if total_customers > 0 else 0
        
        # Crescimento mensal
        monthly_data = df.groupby('year_month').agg({
            'order_id': 'nunique',
            'total_value': 'sum',
            'customer_id': 'nunique',
            'quantity': 'sum'
        }).reset_index()
        monthly_data.columns = ['period', 'orders', 'revenue', 'customers', 'items']
        monthly_data = monthly_data.sort_values('period')
        monthly_data['avg_ticket'] = monthly_data['revenue'] / monthly_data['orders']
        
        # Calcular crescimento percentual
        if len(monthly_data) >= 2:
            monthly_data['revenue_growth'] = monthly_data['revenue'].pct_change() * 100
            monthly_data['orders_growth'] = monthly_data['orders'].pct_change() * 100
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_customers': total_customers,
            'total_items': total_items,
            'avg_ticket': avg_ticket,
            'recurring_customers': recurring_customers,
            'recurrence_rate': recurrence_rate,
            'monthly_data': monthly_data,
            'filtered_data': df
        }
    
    def get_top_products(self, df, limit=10):
        """Analisa top produtos/categorias"""
        product_analysis = df.groupby('product_category').agg({
            'quantity': 'sum',
            'total_value': 'sum',
            'order_id': 'nunique'
        }).reset_index()
        product_analysis.columns = ['category', 'quantity', 'revenue', 'orders']
        product_analysis['avg_price'] = product_analysis['revenue'] / product_analysis['quantity']
        product_analysis['revenue_share'] = (product_analysis['revenue'] / product_analysis['revenue'].sum()) * 100
        
        return product_analysis.sort_values('revenue', ascending=False).head(limit)
    
    def get_geographic_analysis(self, df):
        """Análise geográfica das vendas"""
        state_analysis = df.groupby('customer_state').agg({
            'order_id': 'nunique',
            'total_value': 'sum',
            'customer_id': 'nunique'
        }).reset_index()
        state_analysis.columns = ['state', 'orders', 'revenue', 'customers']
        state_analysis['revenue_share'] = (state_analysis['revenue'] / state_analysis['revenue'].sum()) * 100
        state_analysis = state_analysis.sort_values('revenue', ascending=False)
        
        city_analysis = df.groupby(['customer_state', 'customer_city']).agg({
            'order_id': 'nunique',
            'total_value': 'sum'
        }).reset_index()
        city_analysis.columns = ['state', 'city', 'orders', 'revenue']
        city_analysis = city_analysis.sort_values('revenue', ascending=False).head(20)
        
        return state_analysis, city_analysis
    
    def get_payment_analysis(self, df):
        """Análise de métodos de pagamento"""
        payment_analysis = df.groupby('payment_method').agg({
            'order_id': 'nunique',
            'total_value': 'sum'
        }).reset_index()
        payment_analysis.columns = ['method', 'orders', 'revenue']
        payment_analysis['percentage'] = (payment_analysis['orders'] / payment_analysis['orders'].sum()) * 100
        
        return payment_analysis.sort_values('orders', ascending=False)
    
    def generate_insights(self, kpis, top_products, geo_data, payment_data):
        """Gera insights automáticos baseados nos dados (conforme protótipo)"""
        insights = []
        
        monthly = kpis['monthly_data']
        if len(monthly) >= 2:
            last_revenue = monthly.iloc[-1]['revenue']
            prev_revenue = monthly.iloc[-2]['revenue']
            growth = ((last_revenue - prev_revenue) / prev_revenue) * 100
            
            if growth > 5:
                insights.append({
                    'type': 'success',
                    'icon': '📈',
                    'title': 'Crescimento Positivo',
                    'text': f'Crescimento de {growth:.1f}% na receita do último mês analisado. Tendência positiva identificada. Manter estratégias atuais de marketing e vendas.',
                    'value': f'{growth:.1f}%'
                })
            elif growth < -5:
                insights.append({
                    'type': 'danger',
                    'icon': '🚨',
                    'title': 'Queda nas Vendas',
                    'text': f'Queda de {abs(growth):.1f}% na receita do último mês. Revisar estratégias comerciais urgentemente.',
                    'value': f'{growth:.1f}%'
                })
        
        state_data, _ = geo_data
        if len(state_data) > 0:
            top_state = state_data.iloc[0]
            concentration = top_state['revenue_share']
            
            if concentration > 35:
                insights.append({
                    'type': 'warning',
                    'icon': '📍',
                    'title': 'Concentração Geográfica',
                    'text': f'{top_state["state"]} representa {concentration:.1f}% da receita total. Alta concentração em uma única região indica oportunidade de expansão para outros mercados.',
                    'value': f'{concentration:.1f}%'
                })
        
        if len(top_products) > 0:
            top_category = top_products.iloc[0]
            category_share = top_category['revenue_share']
            
            insights.append({
                'type': 'info',
                'icon': '🏆',
                'title': 'Categoria Líder',
                'text': f'"{top_category["category"]}" lidera com {category_share:.1f}% da receita total analisada. Categoria apresenta melhor desempenho e maior ticket médio. Considere expandir portfólio.',
                'value': f'{category_share:.1f}%'
            })
        
        avg_ticket = kpis['avg_ticket']
        if avg_ticket < 200:
            insights.append({
                'type': 'danger',
                'icon': '💰',
                'title': 'Oportunidade de Ticket Médio',
                'text': f'Ticket médio atual: R$ {avg_ticket:.2f}. Valor está abaixo da média do setor (R$ 200). Considere estratégias de upselling e cross-selling para aumentar.',
                'value': f'R$ {avg_ticket:.2f}'
            })
        
        return insights

def create_sample_data():
    """Cria dados de exemplo realistas"""
    np.random.seed(42)
    
    categories = [
        'Eletrônicos', 'Moda e Vestuário', 'Casa e Decoração', 
        'Livros e Papelaria', 'Esportes e Fitness', 'Beleza e Cuidados',
        'Alimentos e Bebidas', 'Brinquedos e Games'
    ]
    
    states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO', 'PE', 'CE', 'DF', 'ES']
    
    cities_by_state = {
        'SP': ['São Paulo', 'Campinas', 'Santos', 'Ribeirão Preto'],
        'RJ': ['Rio de Janeiro', 'Niterói', 'Petrópolis'],
        'MG': ['Belo Horizonte', 'Uberlândia', 'Juiz de Fora'],
        'RS': ['Porto Alegre', 'Caxias do Sul'],
        'PR': ['Curitiba', 'Londrina'],
        'SC': ['Florianópolis', 'Joinville'],
        'BA': ['Salvador', 'Feira de Santana'],
        'GO': ['Goiânia'],
        'PE': ['Recife'],
        'CE': ['Fortaleza'],
        'DF': ['Brasília'],
        'ES': ['Vitória']
    }
    
    payment_methods = ['Cartão de Crédito', 'Cartão de Débito', 'PIX', 'Boleto']
    
    n_records = 5000
    
    # Probabilidades que somam exatamente 1
    state_probs = np.array([0.22, 0.12, 0.10, 0.07, 0.07, 0.06, 0.08, 0.05, 0.06, 0.05, 0.06, 0.06])
    state_probs /= state_probs.sum()  

    # Gera datas com sazonalidade
    dates = []
    for _ in range(n_records):
        year = np.random.choice([2023, 2024], p=[0.4, 0.6])
        month = np.random.choice(
            range(1, 13),
            p=[0.06, 0.05, 0.07, 0.08, 0.09, 0.10, 0.08, 0.09, 0.08, 0.09, 0.11, 0.10]
        )
        day = np.random.randint(1, 29)
        dates.append(f'{year}-{month:02d}-{day:02d}')
    
    data = {
        'order_id': [f'ORD_{i:06d}' for i in range(1, n_records + 1)],
        'customer_id': [f'CUST_{np.random.randint(1, 2000):06d}' for _ in range(n_records)],
        'order_date': dates,
        'product_category': np.random.choice(
            categories, n_records,
            p=[0.25, 0.18, 0.12, 0.08, 0.10, 0.09, 0.08, 0.10]
        ),
    }
    
    df = pd.DataFrame(data)
    
    prices = []
    for cat in df['product_category']:
        if cat == 'Eletrônicos':
            prices.append(round(np.random.uniform(200, 3000), 2))
        elif cat == 'Moda e Vestuário':
            prices.append(round(np.random.uniform(40, 400), 2))
        elif cat == 'Casa e Decoração':
            prices.append(round(np.random.uniform(50, 800), 2))
        elif cat == 'Livros e Papelaria':
            prices.append(round(np.random.uniform(15, 150), 2))
        elif cat == 'Esportes e Fitness':
            prices.append(round(np.random.uniform(30, 500), 2))
        elif cat == 'Beleza e Cuidados':
            prices.append(round(np.random.uniform(25, 300), 2))
        elif cat == 'Alimentos e Bebidas':
            prices.append(round(np.random.uniform(20, 200), 2))
        else:
            prices.append(round(np.random.uniform(30, 400), 2))
    
    df['product_price'] = prices
    
    df['quantity'] = np.random.randint(1, 6, n_records)
    
    df['total_value'] = df['product_price'] * df['quantity']
    
    # Estado com distribuição ajustada
    df['customer_state'] = np.random.choice(states, n_records, p=state_probs)
    
    # Cidades coerentes com o estado
    df['customer_city'] = df['customer_state'].apply(lambda s: np.random.choice(cities_by_state[s]))
    
    # Pagamento
    df['payment_method'] = np.random.choice(payment_methods, n_records, p=[0.45, 0.15, 0.30, 0.10])
    
    return df


def main():
    """Interface principal do SIG"""
    
    st.markdown("""
    <div class="main-header">
        <h1 style='margin:0; font-size: 2rem;'>📊 Sistema de Informações Gerenciais para E-commerce</h1>
        <p style='margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.95;'>Dashboard Gerencial Empresarial</p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.85;'>
            Desenvolvido por: <strong>Ingrid Mônica da Silva Bezerra</strong> e <strong>Karla Cristina de Sousa Araújo</strong><br>
            IFAL - Instituto Federal de Alagoas | Disciplina: Sistemas de Informações Gerenciais | Prof.ª Wladia Bessa | 2025.1
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar sistema
    if 'sig_system' not in st.session_state:
        st.session_state.sig_system = EcommerceSIG()
        st.session_state.data_loaded = False
    
    sig = st.session_state.sig_system
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configurações do Sistema")
        
        st.markdown("---")
        st.markdown("#### 📁 Upload de Dados")
        
        # Botão dados de exemplo
        if st.button("🧪 Usar Dados de Exemplo", type="primary", use_container_width=True):
            sample_data = create_sample_data()
            buffer = io.StringIO()
            sample_data.to_csv(buffer, index=False, sep=',')
            buffer.seek(0)
            
            success, message = sig.load_data(buffer, "Empresa Demonstração")
            if success:
                st.session_state.data_loaded = True
                st.success(message)
                st.rerun()
        
        st.markdown("---")
        
        # Upload de arquivo
        company_name = st.text_input("Nome da Empresa:", value="Minha Empresa")
        uploaded_file = st.file_uploader(
            "Selecione o arquivo CSV:",
            type=['csv'],
            help="Formato: CSV com vírgula ou ponto-e-vírgula"
        )
        
        if uploaded_file is not None:
            success, message = sig.load_data(uploaded_file, company_name)
            if success:
                st.session_state.data_loaded = True
                st.success(message)
                st.rerun()
            else:
                st.error(message)
        
        # Formato esperado
        with st.expander("📋 Formato CSV Esperado"):
            st.markdown("""
            **Colunas obrigatórias:**
            - `order_id`, `customer_id`
            - `order_date` (YYYY-MM-DD)
            - `product_category`
            - `product_price`, `quantity`
            - `total_value`
            - `customer_state`, `customer_city`
            - `payment_method`
            
            **Separador:** , ou ;  
            **Encoding:** UTF-8, Latin1 ou ISO-8859-1
            """)
        
        # Histórico de uploads
        if len(sig.upload_history) > 0:
            st.markdown("---")
            st.markdown("#### 📜 Histórico de Uploads")
            for upload in reversed(sig.upload_history[-3:]):
                status_class = "status-ok" if upload['status'] == 'OK' else "status-error"
                st.markdown(f"""
                <div class="history-card">
                    <span class="{status_class}">{upload['status']}</span><br>
                    <small>
                        <strong>{upload['company']}</strong><br>
                        {upload['timestamp'].strftime('%d/%m/%Y %H:%M')}<br>
                        {upload['records']:,} registros
                    </small>
                </div>
                """, unsafe_allow_html=True)
    
    # Verificar se dados foram carregados
    if not st.session_state.data_loaded:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("👈 **Faça o upload dos dados CSV ou use os dados de exemplo para começar**")
            
            st.markdown("### 🎯 Funcionalidades do Sistema")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("""
                **📊 Análises Completas**
                - KPIs em tempo real
                - Evolução temporal
                - Análise geográfica
                - Performance de produtos
                """)
            
            with col_b:
                st.markdown("""
                **💡 Insights Automáticos**
                - Crescimento/queda
                - Oportunidades
                - Alertas estratégicos
                - Recomendações
                """)
            
            with col_c:
                st.markdown("""
                **🔍 Recursos**
                - Filtros avançados
                - Gráficos interativos
                - Exportação de dados
                - Multi-empresa
                """)
        
        with col2:
            st.markdown("### 📋 Exemplo CSV")
            example_df = pd.DataFrame({
                'order_id': ['ORD_001', 'ORD_002'],
                'customer_id': ['C001', 'C002'],
                'order_date': ['2024-01-15', '2024-01-16'],
                'product_category': ['Eletrônicos', 'Moda'],
                'product_price': [299.90, 89.50],
                'quantity': [1, 2],
                'total_value': [299.90, 179.00],
                'customer_state': ['SP', 'RJ'],
                'customer_city': ['São Paulo', 'Rio de Janeiro'],
                'payment_method': ['Cartão Crédito', 'PIX']
            })
            st.dataframe(example_df, use_container_width=True, hide_index=True)
        
        return
    
    # Dashboard principal
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
        <h2 style='margin: 0; color: #1e3c72;'>📈 Dashboard Gerencial - {sig.company_name}</h2>
        <p style='margin: 0.3rem 0 0 0; color: #666;'>
            📅 Período: {sig.data_period} | 📊 Total de registros: {len(sig.data):,}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtros avançados
    with st.expander("🔍 Filtros Avançados", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            min_date = sig.data['order_date'].min().date()
            max_date = sig.data['order_date'].max().date()
            date_range = st.date_input(
                "📆 Período de análise:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        with col2:
            all_states = sorted(sig.data['customer_state'].unique().tolist())
            selected_states = st.multiselect(
                "🗺️ Estados:",
                options=all_states,
                default=all_states
            )
    
    # Aplicar filtros
    start_date = date_range[0] if len(date_range) == 2 else None
    end_date = date_range[1] if len(date_range) == 2 else None
    
    # Calcular KPIs
    with st.spinner('⏳ Processando dados...'):
        kpis = sig.calculate_kpis(start_date, end_date, selected_states)
    
    # KPIs principais (estilo protótipo - 5 cards)
    st.markdown("### 📊 Indicadores Principais")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🛒 Total de Pedidos",
            f"{kpis['total_orders']:,}",
            help="Número total de pedidos únicos"
        )
    
    with col2:
        st.metric(
            "💰 Receita Total",
            f"R$ {kpis['total_revenue']:,.0f}",
            help="Receita total gerada"
        )
    
    with col3:
        st.metric(
            "👥 Clientes Únicos",
            f"{kpis['total_customers']:,}",
            help="Número de clientes únicos"
        )
    
    with col4:
        st.metric(
            "📦 Itens Vendidos",
            f"{kpis['total_items']:,}",
            help="Total de itens vendidos"
        )
    
    with col5:
        st.metric(
            "🎯 Ticket Médio",
            f"R$ {kpis['avg_ticket']:,.2f}",
            help="Valor médio por pedido"
        )
    
    st.markdown("---")
    
    # Gráficos principais em abas
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Evolução Temporal", "🏆 Produtos", "🗺️ Geografia", "💳 Pagamentos"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Evolução de Vendas (Mensal)")
            fig_revenue = px.line(
                kpis['monthly_data'],
                x='period',
                y='revenue',
                markers=True,
                labels={'revenue': 'Receita (R$)', 'period': 'Período'}
            )
            fig_revenue.update_traces(
                line_color='#1e3c72',
                line_width=3,
                marker=dict(size=8)
            )
            fig_revenue.update_layout(
                xaxis_tickangle=-45,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                height=350
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            st.markdown("#### 🛒 Evolução de Pedidos")
            fig_orders = px.bar(
                kpis['monthly_data'],
                x='period',
                y='orders',
                labels={'orders': 'Número de Pedidos', 'period': 'Período'},
                color='orders',
                color_continuous_scale='Blues'
            )
            fig_orders.update_layout(
                xaxis_tickangle=-45,
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig_orders, use_container_width=True)
        
        # Gráfico de duplo eixo
        st.markdown("#### 📊 Pedidos vs Ticket Médio")
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_dual.add_trace(
            go.Bar(
                x=kpis['monthly_data']['period'],
                y=kpis['monthly_data']['orders'],
                name='Pedidos',
                marker_color='#1e3c72'
            ),
            secondary_y=False
        )
        
        fig_dual.add_trace(
            go.Scatter(
                x=kpis['monthly_data']['period'],
                y=kpis['monthly_data']['avg_ticket'],
                name='Ticket Médio (R$)',
                mode='lines+markers',
                line=dict(color='#28a745', width=3),
                marker=dict(size=8)
            ),
            secondary_y=True
        )
        
        fig_dual.update_xaxes(title_text="Período", tickangle=-45)
        fig_dual.update_yaxes(title_text="Pedidos", secondary_y=False)
        fig_dual.update_yaxes(title_text="Ticket Médio (R$)", secondary_y=True)
        fig_dual.update_layout(hovermode='x unified', height=400)
        
        st.plotly_chart(fig_dual, use_container_width=True)
    
    with tab2:
        top_products = sig.get_top_products(kpis['filtered_data'], limit=10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Top Categorias por Receita")
            fig_products = px.bar(
                top_products.head(8),
                y='category',
                x='revenue',
                orientation='h',
                labels={'revenue': 'Receita (R$)', 'category': 'Categoria'},
                color='revenue',
                color_continuous_scale='Viridis',
                text='revenue'
            )
            fig_products.update_traces(
                texttemplate='R$ %{text:,.0f}',
                textposition='outside'
            )
            fig_products.update_layout(
                showlegend=False,
                yaxis={'categoryorder':'total ascending'},
                height=400
            )
            st.plotly_chart(fig_products, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Participação por Categoria")
            fig_pie = px.pie(
                top_products.head(6),
                values='revenue',
                names='category',
                hole=0.4
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=11
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("#### 📋 Análise Detalhada de Categorias")
        top_display = top_products.copy()
        top_display['revenue'] = top_display['revenue'].apply(lambda x: f"R$ {x:,.2f}")
        top_display['avg_price'] = top_display['avg_price'].apply(lambda x: f"R$ {x:,.2f}")
        top_display['revenue_share'] = top_display['revenue_share'].apply(lambda x: f"{x:.1f}%")
        top_display.columns = ['Categoria', 'Qtd', 'Receita', 'Pedidos', 'Preço Médio', 'Part. %']
        st.dataframe(top_display, use_container_width=True, hide_index=True)
    
    with tab3:
        state_data, city_data = sig.get_geographic_analysis(kpis['filtered_data'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Top Estados por Receita")
            fig_states = px.bar(
                state_data.head(10),
                x='state',
                y='revenue',
                labels={'revenue': 'Receita (R$)', 'state': 'Estado'},
                color='revenue',
                color_continuous_scale='Blues',
                text='revenue'
            )
            fig_states.update_traces(
                texttemplate='R$ %{text:,.0f}',
                textposition='outside'
            )
            fig_states.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_states, use_container_width=True)
        
        with col2:
            st.markdown("#### Top Cidades por Receita")
            fig_cities = px.bar(
                city_data.head(10),
                y='city',
                x='revenue',
                orientation='h',
                labels={'revenue': 'Receita (R$)', 'city': 'Cidade'},
                color='revenue',
                color_continuous_scale='Greens'
            )
            fig_cities.update_layout(
                showlegend=False,
                yaxis={'categoryorder':'total ascending'},
                height=400
            )
            st.plotly_chart(fig_cities, use_container_width=True)
        
        # Distribuição percentual
        st.markdown("#### Distribuição de Receita por Estado (%)")
        state_top = state_data.head(10)
        fig_dist = px.bar(
            state_top,
            x='state',
            y='revenue_share',
            labels={'revenue_share': 'Participação (%)', 'state': 'Estado'},
            color='revenue_share',
            color_continuous_scale='RdYlGn',
            text='revenue_share'
        )
        fig_dist.update_traces(
            texttemplate='%{text:.1f}%',
            textposition='outside'
        )
        fig_dist.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with tab4:
        payment_data = sig.get_payment_analysis(kpis['filtered_data'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💳 Métodos de Pagamento")
            fig_payment = px.pie(
                payment_data,
                values='orders',
                names='method',
                hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_payment.update_traces(
                textposition='outside',
                textinfo='percent+label',
                pull=[0.1 if i == 0 else 0 for i in range(len(payment_data))]
            )
            fig_payment.update_layout(height=400)
            st.plotly_chart(fig_payment, use_container_width=True)
        
        with col2:
            st.markdown("#### 💰 Receita por Método")
            fig_pay_rev = px.bar(
                payment_data,
                x='method',
                y='revenue',
                labels={'revenue': 'Receita (R$)', 'method': 'Método'},
                color='revenue',
                color_continuous_scale='Purples',
                text='revenue'
            )
            fig_pay_rev.update_traces(
                texttemplate='R$ %{text:,.0f}',
                textposition='outside'
            )
            fig_pay_rev.update_layout(
                xaxis_tickangle=-45,
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig_pay_rev, use_container_width=True)
        
        # Tabela comparativa
        st.markdown("#### Análise Comparativa de Métodos")
        payment_display = payment_data.copy()
        payment_display['avg_ticket'] = payment_display['revenue'] / payment_display['orders']
        payment_display['revenue'] = payment_display['revenue'].apply(lambda x: f"R$ {x:,.2f}")
        payment_display['avg_ticket'] = payment_display['avg_ticket'].apply(lambda x: f"R$ {x:,.2f}")
        payment_display['percentage'] = payment_display['percentage'].apply(lambda x: f"{x:.1f}%")
        payment_display.columns = ['Método', 'Pedidos', 'Receita', 'Part. %', 'Ticket Médio']
        st.dataframe(payment_display, use_container_width=True, hide_index=True)
    
    # Insights Automáticos
    st.markdown("---")
    st.markdown("### 💡 Insights Gerenciais Automáticos")
    
    insights = sig.generate_insights(kpis, top_products, (state_data, city_data), payment_data)
    
    # Exibir insights em grid 2x2
    if len(insights) > 0:
        cols = st.columns(2)
        for idx, insight in enumerate(insights):
            with cols[idx % 2]:
                insight_class = f"insight-{insight['type']}"
                st.markdown(f"""
                <div class="{insight_class}">
                    <h4 style='margin: 0 0 0.5rem 0;'>{insight['icon']} {insight['title']}</h4>
                    <p style='margin: 0 0 0.5rem 0; font-size: 0.95rem;'>{insight['text']}</p>
                    {f"<p style='margin: 0; font-weight: bold; color: #1e3c72; font-size: 1.1rem;'>{insight.get('value', '')}</p>" if 'value' in insight else ""}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Nenhum insight relevante identificado com os filtros atuais")
    
    # Métricas complementares
    st.markdown("---")
    st.markdown("### 📈 Métricas Complementares")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔄 Clientes Recorrentes",
            f"{kpis['recurring_customers']:,}",
            f"{kpis['recurrence_rate']:.1f}%",
            help="Clientes que compraram mais de uma vez"
        )
    
    with col2:
        items_per_order = kpis['total_items'] / kpis['total_orders'] if kpis['total_orders'] > 0 else 0
        st.metric(
            "📦 Itens por Pedido",
            f"{items_per_order:.1f}",
            help="Média de itens por pedido"
        )
    
    with col3:
        if len(kpis['monthly_data']) >= 2:
            last_growth = kpis['monthly_data'].iloc[-1].get('revenue_growth', 0)
            st.metric(
                "📊 Crescimento Mensal",
                f"{last_growth:.1f}%",
                delta=f"{last_growth:.1f}%",
                help="Variação percentual do último mês"
            )
        else:
            st.metric("📊 Crescimento Mensal", "N/A")
    
    with col4:
        avg_item_value = kpis['total_revenue'] / kpis['total_items'] if kpis['total_items'] > 0 else 0
        st.metric(
            "💎 Valor Médio/Item",
            f"R$ {avg_item_value:.2f}",
            help="Valor médio por item vendido"
        )
    
    # Dados detalhados
    st.markdown("---")
    st.markdown("### 📊 Dados Detalhados")
    
    detail_tab1, detail_tab2, detail_tab3 = st.tabs(["📦 Produtos", "🗺️ Geografia", "💳 Pagamentos"])
    
    with detail_tab1:
        st.dataframe(top_products, use_container_width=True, hide_index=True)
    
    with detail_tab2:
        st.dataframe(state_data, use_container_width=True, hide_index=True)
    
    with detail_tab3:
        st.dataframe(payment_data, use_container_width=True, hide_index=True)
    
    # Rodapé
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 1.5rem; border-radius: 10px; color: #666;'>
        <p style='margin: 0; font-size: 1.1rem; font-weight: bold; color: #1e3c72;'>
            📊 Sistema de Informações Gerenciais para E-commerce
        </p>
        <p style='margin: 0.5rem 0;'>
            Desenvolvido por <strong>Ingrid Mônica da Silva Bezerra</strong> e <strong>Karla Cristina de Sousa Araújo</strong>
        </p>
        <p style='margin: 0.5rem 0;'>
            IFAL - Instituto Federal de Alagoas | Disciplina: Sistemas de Informações Gerenciais | 2025.1
        </p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
            Professora: <strong>Wladia Bessa</strong> | Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()