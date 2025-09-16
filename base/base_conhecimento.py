"""
================================================================
ARQUIVO: base_conhecimento.py
DESCRIÇÃO: Define a Base de Conhecimento do Sistema Especialista.
           Contém as regras, sintomas, e alertas de emergência.
================================================================
"""

# Importações necessárias para estruturar os dados de forma clara
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------------
# 1. DEFINIÇÃO DOS SINTOMAS CONHECIDOS PELO SISTEMA
#    Cada sintoma é uma chave única para evitar erros de digitação.
# ----------------------------------------------------------------------------
SINTOMAS_VALIDOS = [
    "febre", "tosse", "dor_de_garganta", "coriza", "espirros", "fadiga",
    "dor_de_cabeca", "perda_de_olfato", "dor_muscular", "nausea", "vomito", "diarreia",
    "dor_abdominal", "dor_no_peito", "falta_de_ar", "rigidez_na_nuca",
    "dor_ao_urinar", "miccao_frequente", "dor_nas_costas", "erupcao_cutanea",
    "coceira_nos_olhos", "chiado_no_peito",
]

# ----------------------------------------------------------------------------
# 2. ESTRUTURA DAS REGRAS DE DIAGNÓSTICO
#    Usamos um `dataclass` para organizar cada regra de forma limpa.
# ----------------------------------------------------------------------------
@dataclass
class RegraCondicao:
    """Representa uma regra para diagnosticar uma condição médica."""
    nome: str                                    # Nome da condição (ex: "Gripe")
    # Dicionário de "sintoma -> peso". O peso indica a força da evidência.
    # Pesos positivos: sintoma presente apoia o diagnóstico.
    # Pesos negativos: sintoma presente enfraquece o diagnóstico.
    evidencias: Dict[str, float]
    # Pontuação base para a condição (bias).
    pontuacao_base: float = 0.0
    # Conselho padrão a ser exibido se esta for a condição sugerida.
    conselho: str = ""
    # Número mínimo de sintomas correspondentes para que a regra seja considerada.
    min_sintomas: int = 1

# ----------------------------------------------------------------------------
# 3. LISTA DE REGRAS (A Base de Conhecimento em si)
#    Aqui está o "conhecimento do especialista" codificado.
# ----------------------------------------------------------------------------
REGRAS_DIAGNOSTICO: List[RegraCondicao] = [
    RegraCondicao(
        nome="Resfriado Comum",
        evidencias=dict(coriza=1.5, espirros=1.2, dor_de_garganta=1.0, tosse=0.8, dor_de_cabeca=0.4, fadiga=0.6),
        pontuacao_base=0.3,
        conselho="Mantenha-se hidratado, descanse e use analgésicos leves. Procure um médico se os sintomas piorarem ou durarem mais de 10 dias."
    ),
    RegraCondicao(
        nome="Gripe (Influenza)",
        evidencias=dict(febre=1.8, dor_muscular=1.5, fadiga=1.2, dor_de_cabeca=0.8, tosse=0.8, dor_de_garganta=0.5),
        pontuacao_base=0.2,
        conselho="Repouso, hidratação e antitérmicos. Procure um serviço de saúde se sentir falta de ar, dor no peito ou confusão mental."
    ),
    RegraCondicao(
        nome="COVID-19 (Suspeita)",
        evidencias=dict(febre=1.3, tosse=1.0, perda_de_olfato=2.5, fadiga=0.8, dor_de_cabeca=0.6, falta_de_ar=1.5),
        pontuacao_base=0.1,
        conselho="Considere realizar um teste e seguir as normas de isolamento locais. Procure atendimento de urgência se tiver falta de ar ou baixa saturação de oxigênio."
    ),
    RegraCondicao(
        nome="Faringite/Amigdalite",
        # A ausência de tosse e coriza são evidências que fortalecem o diagnóstico
        evidencias=dict(dor_de_garganta=2.0, febre=1.0, dor_de_cabeca=0.5, tosse=-0.8, coriza=-0.6),
        pontuacao_base=0.4,
        min_sintomas=1,
        conselho="Faça gargarejos com água morna e sal, use analgésicos. Procure um profissional se a febre for alta, persistente ou se houver placas de pus."
    ),
    RegraCondicao(
        nome="Rinite Alérgica",
        evidencias=dict(espirros=1.8, coriza=1.5, coceira_nos_olhos=1.5, chiado_no_peito=0.5, dor_de_cabeca=0.2),
        pontuacao_base=0.2,
        conselho="Evite o contato com alérgenos conhecidos, faça lavagem nasal. Um médico pode orientar o uso de anti-histamínicos."
    ),
    RegraCondicao(
        nome="Gastroenterite Aguda (Infecção Intestinal)",
        evidencias=dict(nausea=1.2, vomito=1.4, diarreia=1.6, dor_abdominal=1.0, febre=0.4),
        pontuacao_base=0.1,
        conselho="Beba muito líquido (reidratação oral), faça uma dieta leve. Procure atendimento se houver sangue nas fezes, febre alta ou sinais de desidratação."
    ),
    RegraCondicao(
        nome="Infecção Urinária (ITU)",
        evidencias=dict(dor_ao_urinar=2.0, miccao_frequente=1.5, dor_nas_costas=0.8, febre=0.5, nausea=0.3),
        pontuacao_base=0.2,
        conselho="Aumente a ingestão de líquidos. Procure um médico para realizar um exame de urina e obter o tratamento adequado."
    ),
]

# ----------------------------------------------------------------------------
# 4. REGRAS DE ALERTA (BANDEIRAS VERMELHAS / RED FLAGS)
#    Estas regras têm prioridade máxima. Se uma combinação de sintomas
#    for detectada, a urgência é elevada para "emergência".
#    Formato: (Nome do Alerta, [Lista de sintomas obrigatórios], Mensagem de alerta)
# ----------------------------------------------------------------------------
BANDEIRAS_VERMELHAS: List[Tuple[str, List[str], str]] = [
    (
        "Sinais de Emergência Respiratória",
        ["falta_de_ar", "dor_no_peito"],
        "Procure uma emergência IMEDIATAMENTE (SAMU 192). A combinação de falta de ar e dor no peito pode indicar uma condição grave."
    ),
    (
        "Sinais Sugestivos de Meningite",
        ["febre", "rigidez_na_nuca", "dor_de_cabeca"],
        "Febre alta, rigidez na nuca e dor de cabeça forte são sinais de alerta. Procure uma emergência IMEDIATAMENTE."
    ),
    (
        "Sinais Sugestivos de Pneumonia",
        ["febre", "tosse", "falta_de_ar"],
        "A combinação de febre, tosse e falta de ar requer avaliação médica urgente."
    ),
]