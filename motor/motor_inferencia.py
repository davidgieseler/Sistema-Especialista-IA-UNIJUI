"""
================================================================
ARQUIVO: motor_inferencia.py
DESCRIÇÃO: Contém a lógica principal (o "cérebro") do sistema.
           Recebe os sintomas e aplica as regras para gerar um resultado.
================================================================
"""

# Importa as regras e estruturas da nossa base de conhecimento
from base.base_conhecimento import REGRAS_DIAGNOSTICO, BANDEIRAS_VERMELHAS, RegraCondicao
from dataclasses import dataclass
from typing import List, Dict, Iterable

# ----------------------------------------------------------------------------
# 1. ESTRUTURA PARA O RESULTADO DA INFERÊNCIA
#    Organiza os dados que serão retornados após a análise.
# ----------------------------------------------------------------------------
@dataclass
class ResultadoSugerido:
    """Armazena uma única sugestão de diagnóstico com sua explicação."""
    condicao: str
    pontuacao: float
    sintomas_combinados: List[str]
    explicacao_calculo: List[str]
    conselho: str

# ----------------------------------------------------------------------------
# 2. CLASSE PRINCIPAL DO MOTOR DE INFERÊNCIA
# ----------------------------------------------------------------------------
class MotorSistemaEspecialista:
    """
    Esta classe implementa o Motor de Inferência.
    Ela usa uma estratégia de encadeamento para frente (forward-chaining)
    para chegar a uma conclusão a partir dos fatos (sintomas).
    """
    def __init__(self, regras: Iterable[RegraCondicao] = REGRAS_DIAGNOSTICO):
        self.regras = list(regras)

    def analisar(self, sintomas_informados: Iterable[str]) -> Dict:
        """
        Função principal que executa a análise.
        Recebe uma lista de sintomas e retorna um dicionário com o resultado completo.
        """
        # Converte a lista de sintomas para um conjunto (set) para buscas mais rápidas
        sintomas_usuario = set(sintomas_informados)
        resultados_finais: List[ResultadoSugerido] = []

        # ETAPA 1: Calcular a pontuação para cada regra de diagnóstico
        for regra in self.regras:
            pontuacao_atual = regra.pontuacao_base
            sintomas_encontrados = []
            explicacao_parcial = [f"Pontuação base: +{regra.pontuacao_base:.1f}"]

            # Itera sobre as evidências (sintomas e pesos) de cada regra
            for sintoma_regra, peso in regra.evidencias.items():
                if sintoma_regra in sintomas_usuario:
                    # Se o usuário tem o sintoma, adiciona o peso à pontuação
                    pontuacao_atual += peso
                    sintomas_encontrados.append(sintoma_regra)
                    explicacao_parcial.append(f"'{sintoma_regra}': +{peso:.1f}")

                # Lógica para evidência negativa: a AUSÊNCIA de um sintoma pode apoiar um diagnóstico
                elif peso < 0 and sintoma_regra not in sintomas_usuario:
                    # Adiciona parte do peso negativo como bônus (ausência de sintoma que descarta)
                    bonus_ausencia = -peso * 0.5  # Bônus moderado
                    pontuacao_atual += bonus_ausencia
                    explicacao_parcial.append(f"Ausência de '{sintoma_regra}': +{bonus_ausencia:.1f}")

            # A regra só é válida se o número mínimo de sintomas for atendido
            if len(sintomas_encontrados) >= regra.min_sintomas:
                resultados_finais.append(
                    ResultadoSugerido(
                        condicao=regra.nome,
                        pontuacao=round(pontuacao_atual, 2),
                        sintomas_combinados=sintomas_encontrados,
                        explicacao_calculo=explicacao_parcial,
                        conselho=regra.conselho
                    )
                )

        # Ordena os resultados da maior pontuação para a menor
        resultados_finais.sort(key=lambda r: r.pontuacao, reverse=True)

        # ETAPA 2: Verificar as "Bandeiras Vermelhas" (Regras de Emergência)
        alertas_acionados = []
        nivel_urgencia = "rotina"  # Começa com o nível mais baixo
        for nome_alerta, sintomas_necessarios, mensagem in BANDEIRAS_VERMELHAS:
            # `all(...)` verifica se TODOS os sintomas necessários estão presentes
            if all(s in sintomas_usuario for s in sintomas_necessarios):
                alertas_acionados.append({"alerta": nome_alerta, "mensagem": mensagem})
                nivel_urgencia = "emergência" # Eleva a urgência ao máximo

        # ETAPA 3: Montar o dicionário de saída final para o usuário
        # Transforma os objetos ResultadoSugerido em dicionários para facilitar o uso
        sugestoes_formatadas = [
            r.__dict__ for r in resultados_finais[:5] # Limita a 5 sugestões
        ]

        return {
            "sintomas_informados": sorted(list(sintomas_usuario)),
            "sugestoes": sugestoes_formatadas,
            "alertas": alertas_acionados,
            "urgencia": nivel_urgencia,
            "aviso_legal": (
                "IMPORTANTE: Este é um sistema para fins educacionais e NÃO substitui uma avaliação "
                "médica profissional. Em caso de dúvida, procure um serviço de saúde."
            ),
        }