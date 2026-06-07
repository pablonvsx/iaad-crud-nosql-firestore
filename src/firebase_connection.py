"""
Módulo de conexão com Firebase Firestore
"""
import json
import os
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreConnection:
    """Classe para gerenciar conexão com Firebase Firestore"""
    
    _instance: Optional['FirestoreConnection'] = None
    _db = None
    
    def __new__(cls, json_path: str = None):
        """Implementa singleton pattern"""
        if cls._instance is None:
            cls._instance = super(FirestoreConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, json_path: str = None, database: str = "copa-do-mundo"):
        """Inicializa a conexão com Firestore
        
        Args:
            json_path: Caminho para o arquivo JSON de credenciais.
                      Se não fornecido, procura na pasta raiz.
            database: ID do banco de dados Firestore. Padrão: "copa-do-mundo"
        """
        if self._db is None:
            self._initialize_firestore(json_path, database)
    
    def _initialize_firestore(self, json_path: str = None, database: str = "copa-do-mundo") -> None:
        """Inicializa a conexão com Firebase Firestore"""
        try:
            # Verificar se Firebase já foi inicializado
            firebase_admin.get_app()
            print("✅ Firebase já estava inicializado!")
            self._db = firestore.client(database_id=database)
            return
        except ValueError:
            # Firebase ainda não foi inicializado
            pass
        
        # Encontrar arquivo JSON de credenciais
        if json_path is None:
            # Locais para procurar
            search_paths = [
                '../config',  # Pasta config do projeto raiz
                '..',         # Pasta raiz do projeto
                '.',          # Diretório atual (src)
                'config',     # Alternativa relativa
            ]
            
            for search_dir in search_paths:
                if os.path.exists(search_dir):
                    try:
                        for file in os.listdir(search_dir):
                            if file.endswith('.json') and 'firebase' in file.lower() and 'adminsdk' in file.lower():
                                json_path = os.path.join(search_dir, file)
                                break
                    except PermissionError:
                        continue
                
                if json_path:
                    break
        
        if json_path is None:
            raise FileNotFoundError(
                "❌ Arquivo JSON de credenciais não encontrado!\n"
                "Procure em: ../config/, ../, ., ou config/\n"
                "Coloque o arquivo JSON baixado do Firebase Console em uma dessas pastas."
            )
        
        try:
            cred = credentials.Certificate(json_path)
            firebase_admin.initialize_app(cred)
            self._db = firestore.client(database_id=database)
            print(f"✅ Conectado ao Firebase Firestore usando: {json_path}")
            print(f"   Banco de dados: {database}")
        except FileNotFoundError:
            raise FileNotFoundError(f"❌ Arquivo não encontrado: {json_path}")
        except Exception as e:
            raise Exception(f"❌ Erro ao conectar ao Firebase: {str(e)}")
    
    def get_db(self):
        """Retorna a instância do cliente Firestore"""
        return self._db
    
    def add_document(self, collection: str, data: Dict[str, Any]) -> str:
        """
        Adiciona um novo documento a uma coleção
        
        Args:
            collection: Nome da coleção
            data: Dados do documento
            
        Returns:
            ID do documento criado
        """
        _, doc_ref = self._db.collection(collection).add(data)
        doc_id = doc_ref.id
        print(f"✅ Documento criado: {doc_id}")
        return doc_id
    
    def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém um documento específico
        
        Args:
            collection: Nome da coleção
            doc_id: ID do documento
            
        Returns:
            Dados do documento ou None se não existir
        """
        doc = self._db.collection(collection).document(doc_id).get()
        return doc.to_dict() if doc.exists else None
    
    def get_all_documents(self, collection: str) -> list:
        """
        Obtém todos os documentos de uma coleção
        
        Args:
            collection: Nome da coleção
            
        Returns:
            Lista de documentos com seus IDs
        """
        docs = self._db.collection(collection).stream()
        result = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id
            result.append(doc_data)
        return result
    
    def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """
        Atualiza um documento existente
        
        Args:
            collection: Nome da coleção
            doc_id: ID do documento
            data: Dados a atualizar
            
        Returns:
            True se bem-sucedido
        """
        self._db.collection(collection).document(doc_id).update(data)
        print(f"✅ Documento {doc_id} atualizado!")
        return True
    
    def delete_document(self, collection: str, doc_id: str) -> bool:
        """
        Deleta um documento
        
        Args:
            collection: Nome da coleção
            doc_id: ID do documento
            
        Returns:
            True se bem-sucedido
        """
        self._db.collection(collection).document(doc_id).delete()
        print(f"✅ Documento {doc_id} deletado!")
        return True


def get_firestore_client(json_path: str = None, database: str = "copa-do-mundo"):
    """
    Função auxiliar para obter o cliente Firestore
    
    Args:
        json_path: Caminho para o arquivo JSON de credenciais
        database: ID do banco de dados Firestore
    
    Returns:
        Cliente Firestore
    """
    connection = FirestoreConnection(json_path, database)
    return connection.get_db()
