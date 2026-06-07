# Firebase Firestore Connection - Copa do Mundo

Conexão simplificada e reutilizável com Firebase Firestore em Python.

## 🚀 Início Rápido

### 1. Instale as dependências
```bash
pip install -r requirements.txt
```

### 2. Coloque suas credenciais
Coloque o arquivo JSON de credenciais do Firebase na pasta raiz do projeto.

**Para obter:**
1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Projeto → **Project Settings** (engrenagem) → **Service Accounts**
3. Clique em **Generate New Private Key** e salve o JSON

### 3. Use no seu código
```python
from src.firebase_connection import FirestoreConnection

# Inicializar conexão
firestore = FirestoreConnection(database="copa-do-mundo")

# CREATE - Adicionar documento
doc_id = firestore.add_document("usuarios", {
    "nome": "João Silva",
    "email": "joao@example.com"
})

# READ - Obter um documento
usuario = firestore.get_document("usuarios", doc_id)

# READ ALL - Listar todos
usuarios = firestore.get_all_documents("usuarios")

# UPDATE - Atualizar
firestore.update_document("usuarios", doc_id, {"idade": 30})

# DELETE - Deletar
firestore.delete_document("usuarios", doc_id)
```

## 📁 Estrutura

```
.
├── src/
│   └── firebase_connection.py    # Módulo de conexão (reutilizável)
├── iaad-projeto-*-adminsdk-*.json  # Credenciais (não commitar)
├── requirements.txt              # Dependências
├── .gitignore                    # Protege credenciais
└── README.MD                     # Esta documentação
```

## ⚙️ Configuração

### Usar banco customizado
```python
firestore = FirestoreConnection(database="outro-banco")
```

### Usar arquivo JSON com caminho customizado
```python
firestore = FirestoreConnection(
    json_path="caminho/para/credenciais.json",
    database="copa-do-mundo"
)
```

## 🔒 Segurança

- ✅ `.gitignore` já protege `*-adminsdk-*.json`
- ✅ Nunca commitar credenciais
- ✅ Arquivo JSON é detectado automaticamente

## 📚 API Completa

| Método | Descrição |
|--------|-----------|
| `add_document(collection, data)` | Adiciona novo documento |
| `get_document(collection, doc_id)` | Obtém um documento |
| `get_all_documents(collection)` | Lista todos da coleção |
| `update_document(collection, doc_id, data)` | Atualiza documento |
| `delete_document(collection, doc_id)` | Deleta documento |
| `get_db()` | Retorna cliente Firestore direto |

## 🎯 Exemplo Completo

```python
from src.firebase_connection import FirestoreConnection

firestore = FirestoreConnection()

# Adicionar
usuarios_id = firestore.add_document("usuarios", {
    "nome": "Maria",
    "ativo": True
})

# Ler
usuario = firestore.get_document("usuarios", usuarios_id)
print(usuario)

# Listar
todos = firestore.get_all_documents("usuarios")
print(f"Total: {len(todos)}")

# Atualizar
firestore.update_document("usuarios", usuarios_id, {"ativo": False})

# Deletar
firestore.delete_document("usuarios", usuarios_id)
```

## ❓ Troubleshooting

| Erro | Solução |
|------|---------|
| `FileNotFoundError` | Coloque JSON na pasta raiz |
| `404 database not found` | Crie o banco em Firebase Console |
| `Permission denied` | Verifique as credenciais do Firebase |

---

**Pronto para usar! 🎉**
