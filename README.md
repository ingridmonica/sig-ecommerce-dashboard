# 📊 SIG E-commerce - Dashboard Gerencial

Sistema de Informações Gerenciais para análise de dados de e-commerce com insights automáticos e visualizações interativas.

![Dashboard Preview](assets/dashboard.png)

## Funcionalidades

### 📊 Análises Completas
- **KPIs em tempo real**: Receita, pedidos, clientes, ticket médio
- **Evolução temporal**: Gráficos mensais e diários
- **Análise geográfica**: Performance por estado
- **Performance de produtos**: Ranking de categorias

### 💡 Insights Automáticos
- Detecção de crescimento/queda
- Identificação de oportunidades
- Alertas estratégicos
- Recomendações baseadas em dados

### 🔍 Recursos
- Filtros avançados (período, estados)
- Gráficos interativos (Plotly)
- Suporte multi-empresa
- Interface responsiva


## 🌐 Deploy
Acesse: <https://dashboardgerencial.streamlit.app>

## Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/sig-ecommerce-dashboard.git
cd sig-ecommerce-dashboard
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
streamlit run app.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

## 📁 Estrutura do Projeto

```
sig-ecommerce-dashboard/
│
├── app.py                          # Arquivo principal
├── README.md                       # Documentação
├── requirements.txt                # Dependências
├── LICENSE                         # Licença
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configurações gerais
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # Carregamento de CSV
│   ├── data_processor.py           # Processamento de dados
│   └── sample_data.py              # Dados de exemplo
│
├── analytics/
│   ├── __init__.py
│   └── kpis.py                     # Cálculo de KPIs
│
├── components/
│   ├── __init__.py
│   ├── header.py                   # Cabeçalho
│   ├── sidebar.py                  # Barra lateral
│   ├── home_page.py                # Página inicial
│   ├── kpi_cards.py                # Cards de KPIs
│   ├── charts.py                   # Gráficos
│   └── insights_cards.py           # Cards de insights
│
├── styles/
│   ├── __init__.py
│   └── custom_css.py               # Estilos CSS
│
└── assets/
    └── dashboard.png               # Imagem de preview
```

## Formato do CSV

Seu arquivo CSV deve conter as seguintes colunas:

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `order_id` | Texto | ID único do pedido | ORD_000001 |
| `customer_id` | Texto | ID único do cliente | CUST_000123 |
| `order_date` | Data | Data do pedido | 2024-01-15 |
| `product_category` | Texto | Categoria do produto | Eletrônicos |
| `product_price` | Número | Preço unitário | 1299.90 |
| `quantity` | Inteiro | Quantidade | 2 |
| `total_value` | Número | Valor total | 2599.80 |
| `customer_state` | Texto | Estado (UF) | SP |
| `customer_city` | Texto | Cidade | São Paulo |
| `payment_method` | Texto | Forma de pagamento | PIX |

### Exemplo de CSV

```csv
order_id,customer_id,order_date,product_category,product_price,quantity,total_value,customer_state,customer_city,payment_method
ORD_000001,CUST_000123,2024-01-15,Eletrônicos,1299.90,2,2599.80,SP,São Paulo,PIX
ORD_000002,CUST_000456,2024-01-16,Moda,250.50,1,250.50,RJ,Rio de Janeiro,Cartão de Crédito
ORD_000003,CUST_000789,2024-01-17,Casa e Decoração,450.00,3,1350.00,MG,Belo Horizonte,Boleto
```

**Download**: Um arquivo de exemplo está disponível na página inicial do dashboard.

## 🛠️ Tecnologias Utilizadas

- **Streamlit** 1.41.1 - Framework web
- **Pandas** 2.2.3 - Manipulação de dados
- **Plotly** 5.15.0 - Visualizações interativas
- **NumPy** 1.26.4 - Computação numérica

## 💻 Desenvolvimento

### Estrutura Modular

O projeto foi desenvolvido com arquitetura modular para facilitar manutenção e escalabilidade:

- **config/**: Configurações centralizadas
- **utils/**: Utilitários reutilizáveis
- **analytics/**: Lógica de negócio e análises
- **components/**: Componentes visuais da interface
- **styles/**: Estilos e temas

### Executar em modo de desenvolvimento

```bash
streamlit run app.py --server.runOnSave true
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Autores

- **Ingrid Mônica** - *Desenvolvimento* - [GitHub](https://github.com/ingridmonica)
- **Karla Cristina** - *Desenvolvimento* - [GitHub](https://github.com/karlaaraujo)

## Contexto Acadêmico

Projeto desenvolvido para a disciplina de Sistemas de Informações Gerenciais do curso de Sistemas de Informação.

**Instituição**: Instituto Federal de Alagoas (IFAL)  
**Ano**: 2025

---
<div align="center">
Desenvolvido para o Projeto Final SIGE – IFAL 2025.1  <br>
**Sistema de Informações Gerenciais para E-commerce**
</div>
