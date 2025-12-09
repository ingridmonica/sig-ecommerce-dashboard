import streamlit as st

def render_kpi_cards(kpis: dict):
    """Renderiza os cards de KPIs principais"""
    if kpis is None:
        st.error("❌ Erro ao calcular KPIs. Verifique os dados carregados.")
        return
    
    st.markdown("### 📊 Indicadores Principais")
    
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
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_orders = kpis.get('total_orders', 0)
    total_revenue = kpis.get('total_revenue', 0.0)
    total_customers = kpis.get('total_customers', 0)
    total_items = kpis.get('total_items', 0)
    avg_ticket = kpis.get('avg_ticket', 0.0)
    
    with col1:
        st.markdown(
            card_html.format(
                icon="🛒",
                title="Total de Pedidos",
                value=f"{total_orders:,}"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        revenue_formatted = f"R$ {total_revenue:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(
            card_html.format(
                icon="💰",
                title="Receita Total",
                value=revenue_formatted
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            card_html.format(
                icon="👥",
                title="Clientes Únicos",
                value=f"{total_customers:,}"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            card_html.format(
                icon="📦",
                title="Itens Vendidos",
                value=f"{total_items:,}"
            ),
            unsafe_allow_html=True
        )
    
    with col5:
        ticket_formatted = f"R$ {avg_ticket:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(
            card_html.format(
                icon="🎯",
                title="Ticket Médio",
                value=ticket_formatted
            ),
            unsafe_allow_html=True
        )