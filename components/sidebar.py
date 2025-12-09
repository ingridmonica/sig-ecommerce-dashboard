import streamlit as st
import base64
from pathlib import Path
from utils.sample_data import create_sample_data
from utils.data_loader import load_csv_robust
from utils.data_processor import process_dataframe

def get_svg_as_base64(svg_path):
    """Converte SVG em base64 para usar em HTML"""
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        return base64.b64encode(svg_content.encode()).decode()
    except:
        return None

def render_sidebar():
    """Renderiza a barra lateral e retorna df e company_name"""
    
    st.sidebar.markdown("""
    <style>
    /* Estilo para fixar rodapé na sidebar */
    [data-testid="stSidebar"] {
        position: relative;
    }
    
    .sidebar-footer {
        bottom: 0;
        left: 0;
        width: 100%;
        padding: 20px 0 10px 0;
        text-align: center;
        z-index: 999;
    }
    
    /* Modo escuro */
    [data-theme="dark"] .sidebar-footer {
        background: linear-gradient(180deg, rgba(14,17,23,0) 0%, rgba(14,17,23,1) 20%);
    }
    
    .sidebar-footer-content {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
        border-radius: 10px;
        padding: 12px;
        margin: 0 1rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .sidebar-footer p {
        margin: 3px 0;
        font-size: 12px;
        color: #6b7280;
    }
    
    .sidebar-footer strong {
        color: #1e3c72;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    svg_path = Path('assets/dashboard-svgrepo-com.svg')
    
    if svg_path.exists():
        svg_base64 = get_svg_as_base64(svg_path)
        if svg_base64:
            st.sidebar.markdown(f"""
            <div style="text-align: center; padding: 20px 0 10px 0;">
                <a href="/" target="_self" style="text-decoration: none;">
                    <div style="
                        display: inline-block;
                        padding: 15px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 15px;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                        transition: transform 0.2s ease, box-shadow 0.2s ease;
                        cursor: pointer;
                    " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 6px 20px rgba(102, 126, 234, 0.4)';" 
                       onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 4px 15px rgba(102, 126, 234, 0.3)';">
                        <img src="data:image/svg+xml;base64,{svg_base64}" 
                             width="50" height="50" 
                             style="display: block; filter: brightness(0) invert(1);">
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.sidebar.button("🏠 Página Inicial", use_container_width=True, type="secondary"):
                if 'df' in st.session_state:
                    del st.session_state['df']
                if 'company' in st.session_state:
                    del st.session_state['company']
                st.rerun()
    else:
        if st.sidebar.button("🏠 Página Inicial", use_container_width=True, type="secondary"):
            if 'df' in st.session_state:
                del st.session_state['df']
            if 'company' in st.session_state:
                del st.session_state['company']
            st.rerun()
    
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("Fonte de Dados")
    
    data_option = st.sidebar.radio(
        "Selecionar dataset",
        ["Usar dados de exemplo", "Upload de arquivo CSV"]
    )
    
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
                df = load_csv_robust(uploaded_file)
                df = process_dataframe(df)
                st.session_state['df'] = df
                st.session_state['company'] = company_name
                st.success("Arquivo carregado e processado.")
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
                return None, company_name
        else:
            if 'df' in st.session_state:
                df = st.session_state['df']
                company_name = st.session_state.get('company', company_name)
    
    st.sidebar.markdown("<div style='padding-bottom: 100px;'></div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        <div class="sidebar-footer-content">
            <p><strong>📊 Dashboard SIG</strong></p>
            <p>IFAL • 2025</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return df, company_name