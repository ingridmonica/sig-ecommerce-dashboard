# components/header.py

import streamlit as st

def render_header():
    """Renderiza o cabeçalho principal do dashboard"""
    st.markdown("""
    <div class="topbar">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <h2 style='margin:0; color: white;'>
            📊 Sistema de Informações Gerenciais para E-commerce
          </h2>
          <div style="font-size:13px; opacity:0.95; color: rgba(255,255,255,0.92);">
            Dashboard Gerencial - SIG
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:13px; color:rgba(255,255,255,0.9);">IFAL • 2025</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)