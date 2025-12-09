def get_custom_css():
    """Retorna o CSS customizado da aplicação"""
    return """
    <style>
    :root{
    --accent:#1e3c72;
    --accent-2:#2a5298;
    --muted:#6b7280;
    --card-bg: rgba(255,255,255,0.85);
    --card-border: rgba(0,0,0,0.06);
    }

    [data-theme="dark"] { 
    --text-color: #e6eef9; 
    --card-bg: rgba(8,14,30,0.45); 
    --card-border: rgba(255,255,255,0.06); 
    }

    .block-container {
    padding-top: 1.2rem;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
    max-width: 1500px;
    }

    .topbar {
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
    color: white;
    padding: 16px;
    border-radius: 10px;
    box-shadow: 0 6px 18px rgba(20,30,60,0.08);
    }

    .section-title { 
    color: var(--accent); 
    font-weight:800; 
    margin-bottom:8px; 
    }

    .small-muted { 
    color: var(--muted); 
    font-size:13px; 
    }
    </style>
    """