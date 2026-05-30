// performance.js — Testes de Desempenho com explain()
// Compara queries COM e SEM indice

db = db.getSiblingDB("ecommerce_catalog");

// ── TESTE 1: COM indice (category.slug + price.final) ────────
print("===== TESTE 1: Query COM indice composto =====");
var t1 = db.products.find(
  {"category.slug": "laptops", "price.final": {$lt: 500}}
).explain("executionStats").executionStats;
print("Tempo: " + t1.executionTimeMillis + "ms");
print("Docs examinados: " + t1.totalDocsExamined);
print("Docs retornados: " + t1.nReturned);
print("Stage: " + t1.executionStages.stage);

// ── TESTE 2: SEM indice (forcar COLLSCAN) ────────────────────
print("\n===== TESTE 2: Query SEM indice (COLLSCAN) =====");
var t2 = db.products.find(
  {"brand": "Samsung", "condition": "novo"}
).explain("executionStats").executionStats;
print("Tempo: " + t2.executionTimeMillis + "ms");
print("Docs examinados: " + t2.totalDocsExamined);
print("Docs retornados: " + t2.nReturned);
print("Stage: " + t2.executionStages.stage);

// ── TESTE 3: Pesquisa full-text COM indice ───────────────────
print("\n===== TESTE 3: Full-Text Search COM indice =====");
var t3 = db.products.find(
  {$text: {$search: "Samsung"}, "is_active": true}
).explain("executionStats").executionStats;
print("Tempo: " + t3.executionTimeMillis + "ms");
print("Docs examinados: " + t3.totalDocsExamined);
print("Docs retornados: " + t3.nReturned);

// ── TESTE 4: Ordenacao por rating COM indice ─────────────────
print("\n===== TESTE 4: Ordenacao por rating COM indice =====");
var t4 = db.products.find(
  {"is_active": true}
).sort({"rating.average": -1}).limit(10).explain("executionStats").executionStats;
print("Tempo: " + t4.executionTimeMillis + "ms");
print("Docs examinados: " + t4.totalDocsExamined);
print("Docs retornados: " + t4.nReturned);

print("\n===== TESTES DE DESEMPENHO CONCLUIDOS =====");
