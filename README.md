# 📊 Sistema de Informações Gerenciais para E-commerce

**Disciplina:** Sistemas de Informações Gerenciais  
**Instituição:** IFAL - Instituto Federal de Alagoas  
**Período:** 2025.1  
**Autoras:** Ingrid Mônica da Silva Bezerra e Karla Cristina de Sousa Araújo  
**Professora:** Wladia Bessa

---

## Descrição do Projeto

Dashboard analítico que aplica conceitos de Sistema de Informação Gerencial (SIG) através da análise de dados de e-commerce, transformando dados brutos em informações estratégicas para apoio à tomada de decisão empresarial.

---

## 🎯 Objetivos

### Objetivo Geral
Desenvolver um Dashboard Analítico utilizando tecnologias modernas para simular o processo de transformação de dados em informações estratégicas.

### Objetivos Específicos
1. Implementar um SIG completo com coleta, processamento e apresentação de dados
2. Calcular e apresentar KPIs essenciais para gestão de e-commerce
3. Desenvolver visualizações gerenciais interativas
4. Gerar insights automatizados para apoio à decisão estratégica

---

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação
- **Streamlit** - Framework para interface web
- **Pandas** - Processamento e análise de dados
- **Plotly** - Visualizações interativas
- **NumPy** - Computação numérica

---

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior instalado
- pip (gerenciador de pacotes Python)

### Passo 1: Clone ou baixe o projeto

```bash
# Se estiver usando Git
git clone [url-do-repositorio]
cd sig-ecommerce

# Ou simplesmente baixe e extraia os arquivos
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

## 🎮 Como Executar

### Método 1: Execução Direta

```bash
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`

### Método 2: Especificando porta

```bash
streamlit run app.py --server.port 8080
```

---

## 📊 Funcionalidades

### Requisitos Funcionais Implementados

| Código | Descrição | Status |
|--------|-----------|--------|
| RF01 | Permitir upload de arquivo CSV padronizado | ✅ |
| RF02 | Validar colunas obrigatórias do arquivo | ✅ |
| RF03 | Calcular KPIs principais (pedidos, receita, clientes, ticket médio) | ✅ |
| RF04 | Exibir dashboards interativos | ✅ |
| RF05 | Gerar insights automáticos | ✅ |
| RF06 | Permitir uso de dados de exemplo | ✅ |

### 📈 KPIs Disponíveis

1. **Total de Pedidos** - Quantidade total de transações
2. **Receita Total** - Valor agregado de todas as vendas
3. **Clientes Únicos** - Número de clientes diferentes
4. **Ticket Médio** - Valor médio por transação

### Visualizações

- **Vendas no Tempo** - Gráfico de linha com evolução temporal
- **Métodos de Pagamento** - Gráfico de pizza com distribuição
- **Top Categorias** - Gráfico de barras com categorias mais rentáveis
- **Distribuição Geográfica** - Análise por estado

### 💡 Insights Automáticos

O sistema gera automaticamente:
- Análise de concentração geográfica
- Performance de categorias vs média
- Tendências de crescimento/queda
- Taxa de recorrência de clientes
- Padrões de pagamento

---

## 📁 Estrutura de Arquivos

```
sig-ecommerce/
│
├── app.py                 # Aplicação principal
├── requirements.txt       # Dependências do projeto
├── README.md             # Este arquivo
│
├── data/                # Pasta para arquivos CSV
│   └── exemplo.csv
│
└── docs/                 # Documentação do projeto
    ├── Estudo de Viabilidade.pdf
    └── Levantamento de Requisitos.pdf
```

---

## 📝 Formato do Arquivo CSV

### Colunas Obrigatórias

```csv
order_id,order_date,customer_id,total_value,payment_method
ORD00001,2024-01-15,CUST0001,1500.00,Cartão de Crédito
ORD00002,2024-01-16,CUST0002,500.00,PIX
```

### Colunas Opcionais (para análises avançadas)

- `customer_state` - Estado do cliente (ex: SP, RJ, MG)
- `customer_city` - Cidade do cliente
- `product_category` - Categoria do produto
- `product_price` - Preço unitário
- `quantity` - Quantidade

### Exemplo Completo

```csv
order_id,order_date,customer_id,customer_state,customer_city,product_category,product_price,quantity,total_value,payment_method
ORD00001,2024-01-15,CUST0001,SP,São Paulo,Eletrônicos,1500.00,1,1500.00,Cartão de Crédito
ORD00002,2024-01-16,CUST0002,RJ,Rio de Janeiro,Moda,250.00,2,500.00,PIX
ORD00003,2024-01-17,CUST0003,MG,Belo Horizonte,Casa e Decoração,800.00,1,800.00,Boleto
```

---

## Como Usar o Sistema

### 1. Iniciando

1. Execute o comando `streamlit run app.py`
2. O navegador abrirá automaticamente

### 2. Carregando Dados

**Opção A - Dados de Exemplo:**
- Na barra lateral, selecione "Usar dados de exemplo"
- Clique em "Carregar Dados de Exemplo"
- 150 registros fictícios serão carregados automaticamente

**Opção B - Upload de CSV:**
- Na barra lateral, selecione "Upload de arquivo CSV"
- Clique em "Browse files" e selecione seu arquivo
- O sistema validará as colunas automaticamente

### 3. Aplicando Filtros

- **Período**: Selecione data início e data fim
- **Estado**: Filtre por estado específico ou veja todos
- **Limpar Filtros**: Restaura visualização completa

### 4. Navegando pelas Abas

**📈 Visão Geral:**
- Visualize KPIs principais
- Analise gráficos interativos
- Explore tendências temporais

**💡 Insights:**
- Veja análises automáticas
- Receba recomendações estratégicas
- Entenda os critérios de geração

---

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError"

```bash
# Certifique-se de instalar as dependências
pip install -r requirements.txt
```

### Erro: "Port already in use"

```bash
# Use outra porta
streamlit run app.py --server.port 8080
```

### Erro ao carregar CSV

- Verifique se o arquivo está no formato UTF-8
- Confirme que as colunas obrigatórias estão presentes
- Certifique-se de usar vírgula (,) como separador

---

## 📊 Exemplos de Análise

### Cenário 1: Identificar Principais Mercados
1. Carregue os dados
2. Vá para "Visão Geral"
3. Analise o gráfico "Distribuição por Estado"
4. Verifique os insights geográficos

### Cenário 2: Avaliar Crescimento
1. Filtre por período específico
2. Observe o gráfico "Vendas no Tempo"
3. Vá para aba "Insights"
4. Veja análise de crescimento/queda

### Cenário 3: Otimizar Mix de Produtos
1. Analise "Top Categorias"
2. Compare ticket médio por categoria
3. Use insights para priorizar investimentos

---

## 📚 Referências

- **ABComm** - Associação Brasileira de Comércio Eletrônico
- **Dataset Olist** - Brazilian E-Commerce Public Dataset
- **Streamlit Documentation** - https://docs.streamlit.io
- **Plotly Python** - https://plotly.com/python/

---

## 👥 Autoras

**Ingrid Mônica da Silva Bezerra**  
**Karla Cristina de Sousa Araújo**

IFAL - Instituto Federal de Alagoas  
Curso: Sistemas de Informação
Disciplina: Sistemas de Informações Gerenciais  - SIGE
Professora: Wladia Bessa  
Período: 2025.1

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos como requisito da disciplina de Sistemas de Informações Gerenciais do IFAL.

---

## 🆘 Suporte

Para dúvidas ou problemas:
1. Consulte este README
2. Verifique a documentação do Streamlit
3. Entre em contato com as autoras

---

**Última atualização:** Dezembro 2025
**Versão:** 1.0