# 📊 Sistema de Informações Gerenciais para E-commerce

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![IFAL](https://img.shields.io/badge/IFAL-2025.1-orange.svg)](https://www2.ifal.edu.br/)

> Dashboard analítico empresarial completo para análise de dados de e-commerce com geração automática de insights e visualizações interativas.

![Dashboard Preview](assets/dashboard-preview.png)

## 🎯 Sobre o Projeto

Este Sistema de Informações Gerenciais (SIG) foi desenvolvido como projeto final da disciplina de Sistemas de Informações Gerenciais do **IFAL - Instituto Federal de Alagoas**, sob orientação da **Professora Wladia Bessa**.

O sistema transforma dados brutos de vendas em informações estratégicas através de dashboards interativos, KPIs em tempo real e insights automáticos com recomendações acionáveis.

### 👥 Autoras

- **Ingrid Mônica da Silva Bezerra**
- **Karla Cristina de Sousa Araújo**

**Instituição:** IFAL - Instituto Federal de Alagoas  
**Período:** 2025.1  
**Disciplina:** Sistemas de Informações Gerenciais

---

## Funcionalidades

### 📊 Análises Completas

- **5 KPIs Principais:** Pedidos, Receita, Clientes, Itens Vendidos, Ticket Médio
- **4 Métricas Complementares:** Recorrência, Crescimento, Itens/Pedido, Valor/Item
- **Evolução Temporal:** Gráficos de linha e barras com tendências mensais
- **Análise de Produtos:** Top categorias, participação percentual, preço médio
- **Distribuição Geográfica:** Análise por estado e cidade com mapas de calor
- **Métodos de Pagamento:** Distribuição e receita por método

### 💡 Insights Automáticos

- **Crescimento/Queda:** Detecta variações significativas nas vendas
- **Concentração Geográfica:** Identifica oportunidades de expansão
- **Performance de Produtos:** Destaca categorias líderes
- **Oportunidades de Ticket:** Sugere estratégias de upselling
- **Taxa de Recorrência:** Alerta sobre fidelização de clientes
- **Preferências de Pagamento:** Análise de métodos dominantes

### 🔍 Recursos Avançados

- **Filtros Dinâmicos:** Por período e estado com atualização em tempo real
- **Upload Flexível:** Suporte a múltiplos formatos (UTF-8, Latin1, ISO-8859-1)
- **Histórico de Uploads:** Rastreamento de todas as importações
- **Modo Debug:** Ferramenta para desenvolvedores identificarem problemas
- **Interface Empresarial:** Design profissional com gradientes e cards coloridos
- **Responsivo:** Funciona em desktop, tablet e mobile

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.8+ | Linguagem principal |
| **Streamlit** | 1.31.0 | Framework web para dashboards |
| **Pandas** | 2.1.4 | Processamento e análise de dados |
| **Plotly** | 5.18.0 | Visualizações interativas |
| **NumPy** | 1.26.3 | Computação numérica |

---

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clone o repositório

```bash
git clone https://github.com/seu-usuario/sig-ecommerce-dashboard.git
cd sig-ecommerce-dashboard
```

### Passo 2: Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🎮 Como Usar

### Método 1: Execução Local

```bash
streamlit run app.py
```

O dashboard abrirá automaticamente em `http://localhost:8501`

### Método 2: Com Porta Específica

```bash
streamlit run app.py --server.port 8080
```

### Método 3: Modo Headless (Servidor)

```bash
streamlit run app.py --server.headless true
```

---

## 📊 Formato dos Dados

### Colunas Obrigatórias

O sistema aceita arquivos CSV com as seguintes colunas:

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `order_id` | String | ID único do pedido | ORD_001 |
| `customer_id` | String | ID do cliente | CUST_001 |
| `order_date` | Date | Data do pedido | 2024-01-15 |
| `product_category` | String | Categoria do produto | Eletrônicos |
| `product_price` | Float | Preço unitário | 299.90 |
| `quantity` | Integer | Quantidade | 2 |
| `total_value` | Float | Valor total | 599.80 |
| `customer_state` | String | Estado (UF) | SP |
| `customer_city` | String | Cidade | São Paulo |
| `payment_method` | String | Método de pagamento | Cartão de Crédito |

### Exemplo de CSV

```csv
order_id,customer_id,order_date,product_category,product_price,quantity,total_value,customer_state,customer_city,payment_method
ORD_001,CUST_001,2024-01-15,Eletrônicos,299.90,1,299.90,SP,São Paulo,Cartão de Crédito
ORD_002,CUST_002,2024-01-16,Moda,89.50,2,179.00,RJ,Rio de Janeiro,PIX
ORD_003,CUST_003,2024-01-17,Casa e Decoração,149.90,1,149.90,MG,Belo Horizonte,Boleto
```

### Formatos Aceitos

- **Separadores:** `,` (vírgula), `;` (ponto-e-vírgula), `\t` (tab), `|` (pipe)
- **Encodings:** UTF-8, Latin1, ISO-8859-1, CP1252
- **Formatos de Data:** YYYY-MM-DD, DD/MM/YYYY

---

## 🎯 Exemplos de Uso

### 1. Carregar Dados de Exemplo

```python
# No dashboard, clique em:
"🧪 Usar Dados de Exemplo"
```

Isso carregará 5.000 registros fictícios para demonstração.

### 2. Upload de CSV

1. Na sidebar, insira o nome da empresa
2. Clique em "Selecione o arquivo CSV"
3. Escolha seu arquivo
4. Aguarde o processamento (2-5 segundos)
5. Dashboard será exibido automaticamente

### 3. Aplicar Filtros

```python
# Expanda "🔍 Filtros Avançados"
# Selecione:
- Período: Data início e data fim
- Estados: Um ou múltiplos estados
```

Os gráficos e KPIs atualizam automaticamente.

---

## 📁 Estrutura do Projeto

```
sig-ecommerce-dashboard/
│
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências
├── README.md                       # Este arquivo
├── LICENSE                         # Licença MIT
│
├── assets/                         # Recursos visuais
│   ├── dashboard-preview.png
│   └── logo-ifal.png
│
└── .gitignore                      # Arquivos ignorados pelo Git
```

---

## 🎓 Fundamentação Teórica

### O que é um SIG?

Um **Sistema de Informações Gerenciais** é um processo de transformação de dados em informações utilizadas na estrutura decisória da empresa, proporcionando sustentação administrativa para otimizar resultados e alcançar metas.

### Características Implementadas

✅ **Banco de dados integrados** - Consolida múltiplas dimensões de análise  
✅ **Interface amigável** - Dashboard intuitivo com visualizações claras  
✅ **Apoio ao planejamento** - KPIs e métricas para monitoramento  
✅ **Suporte à decisão** - Insights automáticos com recomendações

### Etapas do SIG

1. **Coleta de Dados** → Upload de CSV padronizado
2. **Processamento** → Validação, limpeza e transformação
3. **Armazenamento** → Estrutura em memória otimizada
4. **Distribuição** → Dashboards e visualizações interativas
5. **Tomada de Decisão** → Insights automáticos acionáveis

---

## 🐛 Troubleshooting

### Problema: "Erro ao carregar CSV"

**Solução:**

1. Verifique se o arquivo tem todas as colunas obrigatórias
2. Confirme o formato das datas (YYYY-MM-DD)
3. Remova caracteres especiais dos nomes das colunas
4. Consulte: `docs/TROUBLESHOOTING_UPLOAD.md`

### Problema: "Fica carregando infinitamente"

**Solução:**

1. Ative o modo debug na sidebar
2. Verifique se há registros com datas inválidas
3. Teste com o CSV de exemplo primeiro
4. Veja logs detalhados no terminal

### Problema: "Gráficos não aparecem"

**Solução:**

```bash
pip uninstall plotly
pip install plotly==5.18.0
streamlit cache clear
```

---

## 📊 Exemplos de Análises

### Análise 1: Identificar Principais Mercados

1. Acesse a aba "🗺️ Geografia"
2. Veja o gráfico "Top Estados por Receita"
3. Identifique concentração geográfica
4. Use insights para planejar expansão

### Análise 2: Avaliar Performance de Produtos

1. Acesse a aba "🏆 Produtos"
2. Analise "Top Categorias por Receita"
3. Compare participação percentual
4. Identifique oportunidades de cross-selling

### Análise 3: Monitorar Crescimento

1. Acesse "📈 Evolução Temporal"
2. Observe tendência mensal
3. Verifique crescimento percentual
4. Compare ticket médio ao longo do tempo

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

### Diretrizes

- Siga o padrão PEP 8 para código Python
- Adicione docstrings para funções novas
- Teste suas alterações antes de submeter
- Atualize a documentação se necessário

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📚 Referências

- **ABComm** - Associação Brasileira de Comércio Eletrônico. [Relatório Setorial 2023](https://ecommercebrasil.com.br/noticias/compras-on-line-atingem-r-1857-bilhoes-no-brasil-em-2023-revela-abcomm)
- **Dataset Olist** - Brazilian E-Commerce Public Dataset. [Kaggle](https://www.kaggle.com/olistbr)
- **Streamlit Documentation** - [docs.streamlit.io](https://docs.streamlit.io)
- **Plotly Python** - [plotly.com/python](https://plotly.com/python/)

---

## Contato

**Ingrid Mônica da Silva Bezerra**  
GitHub: [@ingridmonica](https://github.com/ingridmonica)

**Karla Cristina de Sousa Araújo**  
GitHub: [@karlaaraujo](https://github.com/karlaaraujo)

**Instituição:**  
IFAL - Instituto Federal de Alagoas  
[www2.ifal.edu.br](https://www2.ifal.edu.br/)

---

## 🌟 Mostre seu apoio

Se este projeto foi útil para você, considere dar uma ⭐️!

---

<div align="center">

**Desenvolvido por Ingrid Mônica e Karla Cristina**

**IFAL - Sistemas de Informações Gerenciais - 2025.1**

[![IFAL](https://img.shields.io/badge/IFAL-Instituto%20Federal%20de%20Alagoas-green)](https://www2.ifal.edu.br/)

</div>
