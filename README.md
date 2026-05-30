# Projecto SGBD II — Catalogo de Produtos NoSQL

## Descricao
Implementacao de uma camada de persistencia para um ecossistema de e-commerce
utilizando MongoDB como SGBD NoSQL. Subdominio: Catalogo de Produtos Dinamico.

## Requisitos
- Docker Desktop
- Python 3.x
- Bibliotecas: pymongo, faker, python-dotenv

## Instalacao das dependencias Python

@'
# Projecto SGBD II — Catalogo de Produtos NoSQL

## Descricao
Implementacao de uma camada de persistencia para um ecossistema de e-commerce
utilizando MongoDB como SGBD NoSQL. Subdominio: Catalogo de Produtos Dinamico.

## Requisitos
- Docker Desktop
- Python 3.x
- Bibliotecas: pymongo, faker, python-dotenv

## Instalacao das dependencias Python
## Como levantar o ambiente

### 1. Iniciar o MongoDB com Docker
### 2. Verificar que esta a correr
### 3. Povoar a base de dados (100.000+ documentos)
### 4. Executar as 5 consultas avancadas
### 5. Executar os testes de desempenho
## Estrutura do Projecto
## Collections
| Collection   | Documentos |
|-------------|------------|
| products    | 100.000    |
| categories  | 30         |
| users       | 1.000      |
| reviews     | 50.000     |

## Indices criados
- idx_text_search — Full-text search em name, description, tags
- idx_category_price — Filtro por categoria + preco
- idx_geo_location — Consultas geoespaciais
- idx_rating — Ordenacao por rating
- idx_active_recent — Produtos activos por data

## Resultados de Desempenho
| Query | COM indice | SEM indice | Melhoria |
|-------|-----------|-----------|---------|
| Categoria + Preco | 8ms / 726 docs | 87ms / 100.000 docs | 10x mais rapido |

## Interface Web
Mongo Express disponivel em: http://localhost:8081
