# 🔧 Troubleshooting - Problema de Upload

## ❌ Problema: "Fica carregando infinitamente ao importar CSV"

### ✅ **CORREÇÕES IMPLEMENTADAS:**

1. **Melhor Tratamento de Encodings**
   - Tenta 4 encodings: UTF-8, Latin1, ISO-8859-1, CP1252
   - Testa 4 separadores: `,` `;` `\t` `|`
   - Total: 16 combinações diferentes

2. **Validação Aprimorada**
   - Limpa espaços em branco dos nomes de colunas
   - Converte valores numéricos com erro handling
   - Remove apenas registros com problemas críticos
   - Mostra mensagens de aviso claras

3. **Modo Debug Adicionado**
   - Ative na sidebar: "🔧 Debug (Desenvolvedores)"
   - Mostra informações do dataset carregado
   - Identifica problemas de tipo de dados

4. **Logs Detalhados**
   - Mostra qual encoding/separador funcionou
   - Exibe quantos registros foram removidos
   - Traceback completo em caso de erro

---

## 🩺 **DIAGNÓSTICO DO PROBLEMA**

### Possíveis Causas do Loop Infinito

1. **Problema de Encoding/Separador**
   - ✅ **CORRIGIDO**: Agora tenta múltiplas combinações

2. **Datas Inválidas**
   - ✅ **CORRIGIDO**: Usa `dayfirst=True` e `errors='coerce'`
   - Remove apenas registros com data inválida

3. **Valores Numéricos com Formato Incorreto**
   - ✅ **CORRIGIDO**: Converte com `errors='coerce'`
   - Aceita vírgula e ponto como decimal

4. **Colunas com Espaços**
   - ✅ **CORRIGIDO**: `.str.strip()` remove espaços

5. **Arquivo Vazio ou Mal Formado**
   - ✅ **CORRIGIDO**: Verifica `len(df) > 0`

---

## 🔍 **COMO DEBUGAR**

### Passo 1: Ativar Modo Debug

1. Faça upload do arquivo
2. Na sidebar, expanda "🔧 Debug (Desenvolvedores)"
3. Marque "Ativar modo debug"
4. Veja as informações do dataset

### Passo 2: Verificar Mensagens de Erro

Agora o sistema mostra:

- ✅ Qual encoding funcionou
- ⚠️ Quantos registros foram removidos
- ❌ Erro detalhado com traceback

### Passo 3: Validar seu CSV

Execute este checklist no seu arquivo:

```python
import pandas as pd

# Testar leitura
df = pd.read_csv('seu_arquivo.csv', sep=';', encoding='latin1')

# Verificar colunas
print("Colunas:", df.columns.tolist())

# Verificar tamanho
print(f"Linhas: {len(df)}, Colunas: {len(df.columns)}")

# Verificar primeiras linhas
print(df.head())

# Verificar tipos
print(df.dtypes)

# Verificar datas
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
print(f"Datas inválidas: {df['order_date'].isna().sum()}")
```

---

## 📋 **FORMATO CORRETO DO CSV**

### Exemplo de CSV Válido

```csv
order_id,customer_id,order_date,product_category,product_price,quantity,total_value,customer_state,customer_city,payment_method
ORD_001,CUST_001,2024-01-15,Eletrônicos,299.90,1,299.90,SP,São Paulo,Cartão de Crédito
ORD_002,CUST_002,2024-01-16,Moda,89.50,2,179.00,RJ,Rio de Janeiro,PIX
```

### ⚠️ **ERROS COMUNS:**

#### ❌ Erro 1: Colunas com Espaços

```csv
order_id , customer_id , order_date  # ERRADO
order_id,customer_id,order_date     # CORRETO
```

#### ❌ Erro 2: Datas Inválidas

```csv
order_date
32/13/2024  # ERRADO (mês 13 não existe)
2024-01-32  # ERRADO (dia 32 não existe)
2024-01-15  # CORRETO
```

#### ❌ Erro 3: Valores Numéricos como Texto

```csv
product_price
"R$ 299,90"  # ERRADO
299.90       # CORRETO
299,90       # CORRIGIDO automaticamente
```

#### ❌ Erro 4: Separador Errado

```csv
# Se seu CSV usa ponto-e-vírgula, certifique-se:
order_id;customer_id;order_date  # OK
```

---

## 🛠️ **SOLUÇÕES PRÁTICAS**

### Solução 1: Corrigir CSV no Excel

1. Abra o arquivo no Excel
2. **Arquivo → Salvar Como**
3. Escolha: **CSV UTF-8 (delimitado por vírgula)**
4. Salve e tente fazer upload novamente

### Solução 2: Limpar Dados com Python

```python
import pandas as pd

# Ler CSV com problemas
df = pd.read_csv('arquivo_original.csv', sep=';', encoding='latin1')

# Limpar colunas
df.columns = df.columns.str.strip()

# Converter datas
df['order_date'] = pd.to_datetime(df['order_date'], format='%d/%m/%Y', errors='coerce')

# Remover linhas com problemas
df = df.dropna(subset=['order_date', 'total_value'])

# Salvar limpo
df.to_csv('arquivo_limpo.csv', index=False, sep=',', encoding='utf-8')
```

### Solução 3: Usar Dados de Exemplo Primeiro

1. Clique em "🧪 Usar Dados de Exemplo"
2. Se funcionar: problema está no seu CSV
3. Compare seu CSV com o exemplo
4. Corrija as diferenças

---

## 📞 **CHECKLIST DE VERIFICAÇÃO**

Antes de fazer upload, verifique:

- [ ] Arquivo tem exatamente 10 colunas obrigatórias
- [ ] Nomes de colunas sem espaços no início/fim
- [ ] Datas no formato YYYY-MM-DD ou DD/MM/YYYY
- [ ] Valores numéricos sem símbolos (R$, %, etc)
- [ ] Arquivo não está vazio
- [ ] Separador consistente (todo vírgula ou todo ponto-e-vírgula)
- [ ] Encoding UTF-8 ou Latin1
- [ ] Sem linhas em branco no meio
- [ ] Todas as linhas têm o mesmo número de colunas

---

## 🎯 **TESTE RÁPIDO**

Execute este teste para verificar se o sistema está funcionando:

1. **Teste 1: Dados de Exemplo**
   - Clique em "🧪 Usar Dados de Exemplo"
   - ✅ Deve carregar 5.000 registros
   - ✅ Dashboard deve aparecer

2. **Teste 2: CSV Simples**
   - Crie um CSV com 3 linhas
   - Use o exemplo da seção "Formato Correto"
   - Faça upload
   - ✅ Deve carregar sem erros

3. **Teste 3: Seu CSV**
   - Faça upload do seu arquivo
   - ✅ Observe as mensagens
   - ⚠️ Anote os avisos
   - ❌ Leia os erros detalhados

---

## 💡 **DICAS EXTRAS**

### Dica 1: Tamanho do Arquivo

- Arquivos > 50 MB podem demorar
- Teste primeiro com amostra menor
- Use `df.head(1000).to_csv()` para criar amostra

### Dica 2: Caracteres Especiais

- Evite: `ç`, `ã`, `õ`, `é` nos **nomes das colunas**
- OK usar em dados: "São Paulo", "José"

### Dica 3: Excel x CSV

- Excel pode alterar formatos
- Melhor: gerar CSV direto do sistema
- Ou usar LibreOffice Calc

---

## 🆘 **AINDA NÃO FUNCIONA?**

Se após todas as correções ainda houver problema:

1. **Exporte o erro completo**
   - Tire screenshot do traceback
   - Copie a mensagem de erro

2. **Compartilhe amostra dos dados**
   - Primeiras 5 linhas do CSV
   - Liste os nomes das colunas

3. **Informações do ambiente**
   - Versão do Python: `python --version`
   - Versão do Streamlit: `streamlit --version`
   - Versão do Pandas: `pip show pandas`

---

## ✅ **VERIFICAÇÃO FINAL**

Após correções, o sistema deve:

1. ✅ Ler arquivo em < 5 segundos
2. ✅ Mostrar mensagem de sucesso
3. ✅ Exibir 5 KPIs
4. ✅ Renderizar 4 abas de gráficos
5. ✅ Gerar insights automáticos

**Se todos os ✅ aparecerem: SUCESSO! 🎉**

---

*Última atualização: Dezembro 2024*  
*Ingrid Mônica e Karla Cristina - IFAL 2025.1*
