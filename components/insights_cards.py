import streamlit as st
from datetime import datetime
from analytics.insights import generate_smart_insights  # ← ADICIONAR IMPORT

def insight_card(title, description, icon="💡", color="#1e3c72", action=None):
    """Gera HTML para um card de insight"""
    action_html = ""
    if action:
        action_html = f'<div style="font-size: 12px; margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(0,0,0,0.1); font-weight: 600;">💡 Ação: {action}</div>'
    
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
        <div style="display:flex; align-items:flex-start; gap:12px;">
            <div style="font-size: 32px; flex-shrink: 0;">{icon}</div>
            <div style="flex: 1;">
                <div style="font-size: 18px; font-weight: 600; margin-bottom:4px;">{title}</div>
                <div style="font-size: 14px; opacity: 0.85; line-height: 1.4;">{description}</div>
                {action_html}
            </div>
        </div>
    </div>
    """

def render_insights_section(df_filtered, company_name, kpis):  # ← ADICIONAR kpis
    """Renderiza a seção de insights automáticos"""
    st.markdown("---")
    st.markdown("###  Insights Automáticos")
    
    # Gerar insights inteligentes
    insights = generate_smart_insights(kpis, df_filtered)
    
    # Mapear cores por tipo
    color_map = {
        'success': '#4CAF50',
        'warning': '#FF9800',
        'info': '#2196F3',
        'danger': '#E53935'
    }
    
    # Renderizar insights em grid 2 colunas
    if len(insights) > 0:
        # Primeira linha (2 insights)
        if len(insights) >= 2:
            c1, c2 = st.columns(2)
            with c1:
                i = insights[0]
                st.markdown(
                    insight_card(
                        i['title'],
                        i['text'],
                        icon=i['icon'],
                        color=color_map.get(i['type'], '#1e3c72'),
                        action=i.get('action')
                    ),
                    unsafe_allow_html=True
                )
            with c2:
                i = insights[1]
                st.markdown(
                    insight_card(
                        i['title'],
                        i['text'],
                        icon=i['icon'],
                        color=color_map.get(i['type'], '#1e3c72'),
                        action=i.get('action')
                    ),
                    unsafe_allow_html=True
                )
        
        # Segunda linha (até 3 insights)
        remaining = insights[2:]
        if len(remaining) > 0:
            cols = st.columns(min(len(remaining), 3))
            for idx, i in enumerate(remaining[:3]):
                with cols[idx]:
                    st.markdown(
                        insight_card(
                            i['title'],
                            i['text'],
                            icon=i['icon'],
                            color=color_map.get(i['type'], '#1e3c72'),
                            action=i.get('action')
                        ),
                        unsafe_allow_html=True
                    )
    else:
        st.info("Nenhum insight significativo encontrado para o período selecionado.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align:center;color:var(--muted)'>"
        f"Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} • {company_name}"
        f"</div>",
        unsafe_allow_html=True
    )