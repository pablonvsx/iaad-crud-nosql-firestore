# ==========================================
# IMPORTAÇÕES NECESSÁRIAS
# ==========================================
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# ==========================================
# 0. CONFIGURAÇÃO E CONEXÃO
# ==========================================
def conectar_firestore():
    print("Iniciando conexão com o Firestore...")
    # Aponta para o arquivo JSON com as chaves de serviço
    cred = credentials.Certificate("iaad-projeto-copa-do-mundo-firebase-adminsdk-fbsvc-ce1cc53869.json")
    
    # Verifica se o app já foi inicializado para evitar erros ao rodar múltiplas vezes
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
        
    # Inicializa o cliente padrão sem passar o database_id (evita erro em versões antigas)
    db = firestore.client()
    
    # ⚠️ CORREÇÃO: Força o mapeamento direto para o banco "copa-do-mundo" do seu projeto
    db._database_string_internal = "projects/iaad-projeto-copa-do-mundo/databases/copa-do-mundo"
    
    print("Conexão estabelecida com sucesso!\n")
    return db

# ==========================================
# 1. CREATE (Armazenamento/Carga)
# ==========================================
def criar_dados(db):
    print("--- EXECUTANDO CREATE ---")
    
    # Inserindo Seleção com ID manual (.set) e aninhamento de jogadores
    dados_brasil = {
        "nome_selecao": "Brasil",
        "continente": "América do Sul",
        "tecnico": "Dorival Júnior",
        "titulos": 5,
        "jogadores": [
            {"nome_jogador": "Vinícius Júnior", "posicao": "Atacante", "numero_camisa": 7},
            {"nome_jogador": "Alisson Becker", "posicao": "Goleiro", "numero_camisa": 1}
        ]
    }
    db.collection("selecoes").document("brasil").set(dados_brasil)
    print("Documento 'brasil' criado na coleção 'selecoes'.")

    # Inserindo Partida com ID automático (.add) e desnormalização do estádio
    dados_partida = {
        "data_partida": "2026-06-20",
        "selecao_1_id": "brasil", # Fazendo referência ao ID que criamos acima
        "selecao_2_id": "franca",
        "quantidade_gols_selecao_1": 2,
        "quantidade_gols_selecao_2": 1,
        "vencedor_id": "brasil",
        "estadio": {
            "nome_estadio": "Maracanã",
            "cidade": "Rio de Janeiro",
            "pais": "Brasil",
            "capacidade": 78838
        }
    }
    # O .add() retorna uma tupla onde o segundo elemento é a referência do documento gerado
    _, doc_ref = db.collection("partidas").add(dados_partida)
    print(f"Partida criada com sucesso! ID gerado automaticamente: {doc_ref.id}\n")

# ==========================================
# 2. READ (Leitura e Consultas)
# ==========================================
def ler_dados(db):
    print("--- EXECUTANDO READ ---")
    
    # Exemplo 1: Buscando um documento específico pelo ID
    doc_brasil = db.collection("selecoes").document("brasil").get()
    if doc_brasil.exists:
        print(f"Dados do Brasil: {doc_brasil.to_dict()}")
    
    # Exemplo 2: Consulta (Query) análoga ao "WHERE continente = 'América do Sul'"
    print("\nBuscando seleções da América do Sul:")
    query = db.collection("selecoes").where("continente", "==", "América do Sul").stream()
    for doc in query:
        print(f"- {doc.id} => {doc.to_dict()['nome_selecao']}")
    print("")

# ==========================================
# 3. UPDATE (Atualização)
# ==========================================
def atualizar_dados(db):
    print("--- EXECUTANDO UPDATE ---")
    
    # Atualizando apenas o campo do técnico e incrementando os títulos
    doc_ref = db.collection("selecoes").document("brasil")
    doc_ref.update({
        "tecnico": "Novo Técnico Contratado",
        "titulos": firestore.Increment(1) # Operador nativo do Firestore para somar +1
    })
    print("Dados da seleção brasileira atualizados (Técnico e Títulos).\n")

# ==========================================
# 4. DELETE (Remoção)
# ==========================================
def deletar_dados(db):
    print("--- EXECUTANDO DELETE ---")
    
    # Deletando o documento inteiro
    db.collection("selecoes").document("brasil").delete()
    print("Documento 'brasil' deletado com sucesso do banco de dados.\n")

# ==========================================
# EXECUÇÃO DO SCRIPT
# ==========================================
if __name__ == "__main__":
    # Inicializa o banco
    banco_firestore = conectar_firestore()
    
    # Você pode comentar as linhas abaixo para executar passo a passo durante a gravação
    criar_dados(banco_firestore)
    ler_dados(banco_firestore)
    atualizar_dados(banco_firestore)
    deletar_dados(banco_firestore)
