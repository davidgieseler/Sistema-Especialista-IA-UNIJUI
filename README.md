# 🩺 Sistema Especialista para Triagem Médica Básica

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)  
![Status](https://img.shields.io/badge/Status-Projeto%20Educacional-orange)

Este repositório contém um **sistema especialista didático**, desenvolvido em **Python**, para realizar uma **triagem médica inicial**.  
O projeto demonstra, de forma prática, como os **sistemas baseados em regras** da Inteligência Artificial podem ser aplicados em um problema real.

> ⚠️ **Aviso Importante:** Este sistema é apenas uma **ferramenta educacional** e **NÃO** deve ser utilizado para diagnóstico médico real.  
> Não substitui a avaliação, diagnóstico ou tratamento por um profissional de saúde.

---

## ✨ Funcionalidades

- **Base de Conhecimento Flexível:** regras médicas com pesos, permitindo que alguns sintomas tenham maior ou menor influência.  
- **Motor de Inferência Explicável:** além de sugerir possíveis condições, o sistema mostra *por que* chegou a cada sugestão.  
- **Bandeiras Vermelhas (Red Flags):** combinações de sintomas que sugerem **emergência médica** disparam alertas automáticos.  
- **Arquitetura Didática e Modular:** dividido em três arquivos principais (`base_conhecimento.py`, `motor_inferencia.py`, `main.py`).  

---

## ⚙️ Como Funciona

O sistema segue a arquitetura clássica de um **sistema especialista**, composta por:

1. **`base_conhecimento.py` – Base de Conhecimento**  
   Contém:
   - Lista de **condições médicas** (ex.: gripe, resfriado, COVID-19).  
   - Dicionário de **sintomas** e seus **pesos**.  
   - **Bandeiras vermelhas** para situações de risco imediato.

2. **`motor_inferencia.py` – Motor de Inferência**  
   - Recebe os sintomas informados.  
   - Aplica **encadeamento para frente** (*forward chaining*).  
   - Calcula pontuações para cada condição e gera sugestões ordenadas.

3. **`main.py` – Interface com o Usuário**  
   - Faz perguntas ao usuário no terminal.  
   - Coleta as respostas (`s` / `n`).  
   - Apresenta o resultado final com explicações e alertas.  

---

## 📂 Estrutura do Projeto

```
/
├── 📄 base/base_conhecimento.py   # Define sintomas, regras e alertas
├── 📄 motor/motor_inferencia.py    # Lógica de análise e inferência
└── 📄 main.py                # Interface de execução (CLI)
```

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7 ou superior.

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```

2. **Acesse a pasta**
   ```bash
   cd seu-repositorio
   ```

3. **Execute o programa**
   ```bash
   python main.py
   ```
   > O sistema iniciará no terminal.  
   > Responda `s` para **sim**, `n` para **não**, ou pressione **ENTER** para pular.

---

## 📝 Exemplo de Uso

Usuário responde "sim" para **febre**, **tosse** e **dor muscular**.

### Entrada (no terminal)
```
================================================== Sistema Especialista de Triagem Médica (Demo)

Responda com 's' (sim) ou 'n' (não). ENTER para pular.

Você está com febre? (s/n) s
Está com tosse? (s/n) s
Sente dor de garganta? (s/n) n
Seu nariz está escorrendo ou entupido? (s/n) n
Sente dores no corpo ou músculos? (s/n) s
...
```

### Saída esperada
```
-------------------- ANÁLISE COMPLETA --------------------
Sintomas informados: febre, tosse, dor_muscular
Nível de urgência sugerido: ROTINA

--- Sugestões ---
[+] Condição: Gripe (Influenza) (Pontuação: 4.4)
    Evidências: febre, dor_muscular, tosse
    Conselho: Repouso, hidratação, antitérmicos. Procure serviço de saúde se houver falta de ar ou dor no peito.

[+] Condição: COVID-19 (Suspeita) (Pontuação: 2.4)
    Evidências: febre, tosse
    Conselho: Considere teste e isolamento conforme normas locais. Procure urgência se houver dispneia.

==================================================
IMPORTANTE: Este sistema é apenas para fins educacionais.
NÃO substitui uma avaliação médica profissional.
```

---

## ⚠️ Aviso Legal

Este projeto é uma **demonstração técnica** de um sistema especialista.  
As regras e pesos foram simplificados para fins educacionais e **não possuem validação clínica**.  

**Não utilize este projeto para autodignóstico.**  
Sempre procure orientação médica profissional em casos de saúde.
