Aqui está o documento Markdown completo e estruturado. Você pode copiá-lo diretamente para o seu `README.md` no GitHub ou para o seu Obsidian. Ele foi redigido de forma técnica e didática, ideal para apoiar a sua fala durante o vídeo do minicurso.

---

```markdown
# 🗂️ Modelagem Conceitual NoSQL: Cloud Firestore

Este documento detalha a arquitetura de dados adotada para a migração do modelo relacional "Copa do Mundo de Futebol" (MySQL) para o paradigma Orientado a Documentos (Google Cloud Firestore). 

Diferente dos bancos relacionais que utilizam tabelas rígidas e Chaves Estrangeiras (FKs) para garantir a integridade e o relacionamento dos dados, o Firestore utiliza **Coleções** e **Documentos JSON**. Para otimizar as consultas e reduzir a latência, aplicamos duas estratégias principais do universo NoSQL: **Aninhamento (Embedding)** e **Referência/Desnormalização**.

Abaixo, apresentamos o detalhamento visual e as justificativas arquiteturais para as duas coleções principais do nosso sistema.

---

## 1. Coleção: `selecoes` (Estratégia de Aninhamento)

No modelo relacional original, existia uma relação de 1:N entre as tabelas `selecoes` e `jogadores`. No Firestore, optamos por eliminar a coleção de jogadores e **aninhar** seus dados diretamente dentro do documento da respectiva seleção.

### 📌 Justificativa
Como uma seleção de futebol possui um limite fixo e relativamente pequeno de convocados (ex: 26 jogadores), o *embedding* (aninhamento) é a abordagem ideal. Isso nos permite carregar a seleção e todo o seu elenco com uma única requisição de leitura (Read), eliminando a necessidade de operações custosas análogas aos `JOINs` do SQL.

### 📄 Estrutura Visual do Documento (JSON)
```json
{
  "nome_selecao": "Brasil",
  "continente": "América do Sul",
  "tecnico": "Dorival Júnior",
  "titulos": 5,
  "jogadores": [
    {
      "nome_jogador": "Vinícius Júnior",
      "posicao": "Atacante",
      "numero_camisa": 7,
      "data_nascimento": "2000-07-12"
    },
    {
      "nome_jogador": "Alisson Becker",
      "posicao": "Goleiro",
      "numero_camisa": 1,
      "data_nascimento": "1992-10-02"
    }
  ]
}

```

---

## 2. Coleção: `partidas` (Estratégia de Referência e Desnormalização)

No modelo relacional, a tabela `partidas` funcionava como uma entidade associativa complexa, ligando as seleções (seleção 1 e seleção 2) e o estádio. No Firestore, resolvemos isso combinando referências por ID e dados embutidos.

### 📌 Justificativa

* **Referência (Seleções):** Mantemos apenas os `IDs` das seleções envolvidas e o `ID` da seleção vencedora. Como os dados de uma seleção podem ser atualizados (ex: troca de técnico), a referência garante que a partida sempre aponte para a versão mais atualizada da seleção.
* 
**Desnormalização (Estádio):** Ao invés de criar uma coleção separada apenas para `estadios`, optamos por desnormalizar e embutir os dados do estádio diretamente na partida. Como as informações estruturais de um estádio (nome, cidade, capacidade)  são estáticas e raramente sofrem mutações, salvá-las no documento da partida reduz a quantidade de coleções no banco e acelera a consulta.



### 📄 Estrutura Visual do Documento (JSON)

```json
{
  "data_partida": "2026-06-20",
  "selecao_1_id": "8fB2xY...", 
  "selecao_2_id": "9jK4wZ...", 
  "quantidade_gols_selecao_1": 2,
  "quantidade_gols_selecao_2": 1,
  "vencedor_id": "8fB2xY...", 
  "estadio": {
    "nome_estadio": "Maracanã",
    "cidade": "Rio de Janeiro",
    "pais": "Brasil",
    "capacidade": 78838
  }
}

```

---

## ⚖️ Comparativo de Relacionamentos: MySQL x Firestore

Para consolidar o aprendizado , elaboramos o comparativo abaixo evidenciando como os dados se comportam em ambos os paradigmas durante o nosso projeto:

| Característica | MySQL (Relacional) | Firestore (NoSQL - Documentos) |
| --- | --- | --- |
| **Esquema (Schema)** | Rígido. Colunas e tipos de dados estritamente definidos na criação da tabela. | Flexível. Documentos na mesma coleção podem ter campos e estruturas diferentes. |
| **Relacionamentos** | Feitos via **Chaves Estrangeiras (FK)**. Dependência direta entre tabelas.

 | Feitos via **Aninhamento (Arrays/Mapas)** ou **Referências (ObjectIDs)**.

 |
| **Consultas Combinadas** | Utiliza a cláusula `JOIN` para unir dados de múltiplas tabelas em tempo de execução. | Não possui `JOIN` nativo. Resolve-se buscando dados separadamente ou através da desnormalização prévia. |
| **Escalabilidade** | Majoritariamente Vertical (aumentar hardware do servidor). | Majoritariamente Horizontal (distribuição automática de documentos em nuvem). |

```

```