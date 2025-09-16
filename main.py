"""
================================================================
ARQUIVO: main.py
DESCRIÇÃO: Ponto de entrada do programa.
           Gerencia a interface com o usuário (faz as perguntas)
           e exibe os resultados da análise.
================================================================
"""

# Importa o nosso motor de inferência
from motor.motor_inferencia import MotorSistemaEspecialista

# ----------------------------------------------------------------------------
# 1. LISTA DE PERGUNTAS
#    Formato: (chave_do_sintoma, "Texto da pergunta")
# ----------------------------------------------------------------------------
PERGUNTAS = [
    ("febre", "Você está com febre? (s/n) "),
    ("tosse", "Está com tosse? (s/n) "),
    ("dor_de_garganta", "Sente dor de garganta? (s/n) "),
    ("coriza", "Seu nariz está escorrendo ou entupido? (s/n) "),
    ("espirros", "Está espirrando com frequência? (s/n) "),
    ("fadiga", "Sente um cansaço ou fadiga fora do comum? (s/n) "),
    ("dor_de_cabeca", "Está com dor de cabeça? (s/n) "),
    ("perda_de_olfato", "Você notou perda de olfato ou paladar? (s/n) "),
    ("dor_muscular", "Sente dores no corpo ou nos músculos? (s/n) "),
    ("nausea", "Está com náusea? (s/n) "),
    ("vomito", "Teve episódios de vômito? (s/n) "),
    ("diarreia", "Está com diarreia? (s/n) "),
    ("dor_abdominal", "Sente dor na região abdominal? (s/n) "),
    ("dor_no_peito", "Está sentindo dor ou aperto no peito? (s/n) "),
    ("falta_de_ar", "Está com dificuldade para respirar ou falta de ar? (s/n) "),
    ("rigidez_na_nuca", "Sente o pescoço rígido, com dificuldade de movê-lo? (s/n) "),
    ("dor_ao_urinar", "Sente dor ou ardência ao urinar? (s/n) "),
    ("miccao_frequente", "Está urinando com uma frequência muito maior que o normal? (s/n) "),
    ("dor_nas_costas", "Sente dor na região lombar (fundo das costas)? (s/n) "),
    ("erupcao_cutanea", "Apareceu alguma erupção ou mancha na pele? (s/n) "),
    ("coceira_nos_olhos", "Seus olhos estão coçando? (s/n) "),
    ("chiado_no_peito", "Você ouve um chiado ao respirar? (s/n) "),
]

# ----------------------------------------------------------------------------
# 2. VALIDAÇÃO DE ENTRADA
# ----------------------------------------------------------------------------
# Conjuntos de respostas válidas
RESPOSTAS_SIM = {"s", "sim", "y", "yes"}
RESPOSTAS_NAO = {"n", "nao", "não", "no"}

def perguntar_sim_nao(texto_pergunta: str) -> bool | None:
    """
    Faz uma pergunta sim/não e valida a entrada.

    Retorna:
      - True  -> usuário respondeu SIM
      - False -> usuário respondeu NÃO
      - None  -> usuário pressionou ENTER para pular

    Também aceita:
      - 'q', 'quit', 'sair' -> encerra a entrevista imediatamente.
    """
    while True:
        try:
            resp = input(texto_pergunta).strip().lower()
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário. Encerrando…")
            raise SystemExit(130)

        # ENTER (vazio) = pular
        if resp == "":
            return None

        # Sair antecipadamente
        if resp in {"q", "quit", "sair"}:
            print("Entrevista encerrada pelo usuário.")
            raise SystemExit(0)

        if resp in RESPOSTAS_SIM:
            return True
        if resp in RESPOSTAS_NAO:
            return False

        print("Resposta inválida. Digite 's' (sim), 'n' (não), ENTER para pular ou 'q' para sair.")

# ----------------------------------------------------------------------------
# 3. FUNÇÃO PRINCIPAL QUE EXECUTA O PROGRAMA
# ----------------------------------------------------------------------------
def executar_triagem():
    """Conduz a entrevista com o usuário e exibe os resultados."""
    print("=" * 50)
    print("   Sistema Especialista de Triagem Médica")
    print("=" * 50)
    print("Responda às perguntas com 's' (sim) ou 'n' (não).")
    print("Pressione ENTER para pular. Digite 'q' para encerrar.\n")

    # Coleta os fatos (sintomas) do usuário
    sintomas_coletados = []
    for chave_sintoma, texto_pergunta in PERGUNTAS:
        valor = perguntar_sim_nao(texto_pergunta)
        if valor is True:
            sintomas_coletados.append(chave_sintoma)
        # False ou None -> não adiciona (negou ou pulou)

    # Cria uma instância do motor e executa a análise
    motor = MotorSistemaEspecialista()
    resultado = motor.analisar(sintomas_coletados)

    # Exibe os resultados de forma organizada
    print("\n" + "-" * 20 + " ANÁLISE COMPLETA " + "-" * 20)

    # Mostra os sintomas que o sistema considerou
    sintomas_informados_str = ", ".join(resultado["sintomas_informados"]) or "(Nenhum sintoma informado)"
    print(f"Sintomas Informados: {sintomas_informados_str}")

    # Exibe o nível de urgência e os alertas
    print(f"Nível de Urgência Sugerido: {resultado['urgencia'].upper()}")
    if resultado["alertas"]:
        print("\n" + "!" * 10 + " ATENÇÃO: SINAIS DE ALERTA DETECTADOS " + "!" * 10)
        for alerta in resultado["alertas"]:
            print(f"-> {alerta['alerta']}: {alerta['mensagem']}")
        print("!" * 56)

    # Mostra as sugestões de diagnóstico
    print("\n--- Sugestões de Possíveis Condições ---")
    if not resultado["sugestoes"]:
        print("Não há sugestões suficientes com base nos sintomas informados.")
    else:
        for sugestao in resultado["sugestoes"]:
            print(f"\n[+] Condição: {sugestao['condicao']} (Pontuação: {sugestao['pontuacao']})")
            print(f"    | Evidências: {', '.join(sugestao['sintomas_combinados']) or '(sem evidências suficientes)'}")
            print(f"    | Cálculo: {'; '.join(sugestao['explicacao_calculo'])}")
            print(f"    | Conselho: {sugestao['conselho']}")

    # Exibe o aviso legal final
    print("\n" + "=" * 50)
    print(resultado["aviso_legal"])
    print("=" * 50)

# ----------------------------------------------------------------------------
# PONTO DE ENTRADA: Garante que o programa só execute quando este
# arquivo (`main.py`) for rodado diretamente.
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    executar_triagem()
