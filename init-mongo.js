// init-mongo.js
// Este script é executado automaticamente pelo MongoDB na primeira inicialização.
// Cria um utilizador dedicado para a aplicação (com menos privilégios que o root).

db = db.getSiblingDB("ecommerce_catalog");

db.createUser({
  user: "app_user",
  pwd: "app_password_2025",
  roles: [
    {
      role: "readWrite",
      db: "ecommerce_catalog"
    }
  ]
});

// Criar as coleções principais antecipadamente (opcional, mas boas práticas)
db.createCollection("products");
db.createCollection("categories");
db.createCollection("reviews");
db.createCollection("users");

print("Base de dados ecommerce_catalog inicializada com sucesso.");
print("Utilizador app_user criado.");
