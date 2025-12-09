import streamlit as st
from datetime import datetime

def insight_card(title, description, icon="💡", color="#1e3c72"):
    """Gera HTML para um card de insight"""
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

def render_insights_section(df_filtered, company_name):
    """Renderiza a seção de insights automáticos"""
    st.markdown("---")
    st.markdown("### 🔎 Insights Automáticos")
    
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
        st.markdown(
            insight_card(
                "Categoria Líder de Vendas",
                f"A categoria {top_cat} foi a mais vendida no período, com {count_top} vendas.",
                icon="🏆",
                color="#4CAF50"
            ),
            unsafe_allow_html=True
        )
    
    with c2:
        st.markdown(
            insight_card(
                "Categoria com Menor Desempenho",
                f"A categoria {bottom_cat} teve o menor volume, com apenas {count_bottom} vendas.",
                icon="📉",
                color="#E53935"
            ),
            unsafe_allow_html=True
        )
    
    with c1:
        st.markdown(
            insight_card(
                "Concentração de Vendas",
                f"A categoria líder representa {concentration:.1f}% de todas as vendas analisadas.",
                icon="🎯",
                color="#FF9800"
            ),
            unsafe_allow_html=True
        )
    
    with c2:
        st.markdown(
            insight_card(
                "Diversidade no Mix de Produtos",
                f"O dataset possui {categories_count} categorias diferentes vendidas.",
                icon="📦",
                color="#3F51B5"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    st.markdown(
        f"<div style='text-align:center;color:var(--muted)'>"
        f"Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} • {company_name}"
        f"</div>",
        unsafe_allow_html=True
    )