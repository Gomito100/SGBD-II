// ============================================================
// queries.js — 5 Consultas Avancadas
// Projecto: Catalogo de Produtos Dinamico (SGBD II 2025/2026)
// Executar: mongosh mongodb://127.0.0.1:27017/ecommerce_catalog queries.js
// ============================================================

db = db.getSiblingDB("ecommerce_catalog");

// ── QUERY 1: Pesquisa Full-Text com filtros e ordenacao ──────
print("\n===== QUERY 1: Pesquisa Full-Text =====");
var q1 = db.products.find(
  { $text: { $search: "Samsung laptop" }, "is_active": true },
  { score: { $meta: "textScore" }, name: 1, "price.final": 1, "category.name": 1 }
).sort({ score: { $meta: "textScore" } }).limit(5);
q1.forEach(printjson);

// ── QUERY 2: Aggregation Pipeline — Top 5 marcas por receita ─
print("\n===== QUERY 2: Top 5 Marcas por Receita Total =====");
var q2 = db.products.aggregate([
  { $match: { "is_active": true } },
  { $group: {
      _id: "$brand",
      total_receita: { $sum: "$price.final" },
      total_produtos: { $count: {} },
      preco_medio: { $avg: "$price.final" },
      rating_medio: { $avg: "$rating.average" }
  }},
  { $sort: { total_receita: -1 } },
  { $limit: 5 },
  { $project: {
      marca: "$_id",
      total_receita: { $round: ["$total_receita", 2] },
      total_produtos: 1,
      preco_medio: { $round: ["$preco_medio", 2] },
      rating_medio: { $round: ["$rating_medio", 1] }
  }}
]);
q2.forEach(printjson);

// ── QUERY 3: Actualizacao parcial — adicionar tag a produtos ─
print("\n===== QUERY 3: Actualizacao Parcial (array update) =====");
var q3result = db.products.updateMany(
  { "price.discount_pct": { $gte: 30 }, "is_active": true },
  { $addToSet: { tags: "super-promocao" },
    $set: { "updated_at": new Date() } }
);
print("Produtos actualizados: " + q3result.modifiedCount);

// Verificar resultado
var exemplo = db.products.findOne({ tags: "super-promocao" }, { name:1, tags:1, "price.discount_pct":1 });
printjson(exemplo);

// ── QUERY 4: Consulta Geoespacial — produtos perto de Luanda ─
print("\n===== QUERY 4: Consulta Geoespacial (perto de Luanda) =====");
var q4 = db.products.aggregate([
  { $geoNear: {
      near: { type: "Point", coordinates: [13.2343, -8.8368] },
      distanceField: "distancia_metros",
      maxDistance: 100000,
      spherical: true,
      query: { "is_active": true }
  }},
  { $limit: 5 },
  { $project: {
      name: 1,
      "stock.warehouse": 1,
      "price.final": 1,
      distancia_km: { $round: [{ $divide: ["$distancia_metros", 1000] }, 2] }
  }}
]);
q4.forEach(printjson);

// ── QUERY 5: Aggregation complexa — categorias com mais reviews
print("\n===== QUERY 5: Categorias com Melhor Rating Medio =====");
var q5 = db.products.aggregate([
  { $match: { "rating.count": { $gt: 100 } } },
  { $group: {
      _id: "$category.name",
      rating_medio: { $avg: "$rating.average" },
      total_produtos: { $count: {} },
      total_avaliacoes: { $sum: "$rating.count" },
      preco_medio: { $avg: "$price.final" }
  }},
  { $sort: { rating_medio: -1 } },
  { $limit: 10 },
  { $project: {
      categoria: "$_id",
      rating_medio: { $round: ["$rating_medio", 2] },
      total_produtos: 1,
      total_avaliacoes: 1,
      preco_medio: { $round: ["$preco_medio", 2] }
  }}
]);
q5.forEach(printjson);

print("\n===== TODAS AS QUERIES EXECUTADAS COM SUCESSO =====");
