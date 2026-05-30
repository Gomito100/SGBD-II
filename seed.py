import random
from datetime import datetime
from pymongo import MongoClient, GEOSPHERE, TEXT, ASCENDING, DESCENDING
from faker import Faker

MONGO_URI = "mongodb://127.0.0.1:27017/"
DB_NAME   = "ecommerce_catalog"
BATCH     = 1000

fake = Faker("pt_PT")
random.seed(42)

client = MongoClient(MONGO_URI)
db     = client[DB_NAME]

print("A limpar colecoes existentes...")
db.products.drop()
db.categories.drop()
db.users.drop()
db.reviews.drop()

print("[1/5] A inserir categorias...")
category_tree = [
    {"name":"Electronica","slug":"electronica","subcategories":["Smartphones","Laptops","Tablets","Auscultadores","Smartwatches"]},
    {"name":"Moda","slug":"moda","subcategories":["Camisas","Calcas","Vestidos","Sapatos","Acessorios"]},
    {"name":"Casa e Jardim","slug":"casa-jardim","subcategories":["Mobiliario","Decoracao","Jardim","Cozinha","Iluminacao"]},
    {"name":"Desporto","slug":"desporto","subcategories":["Futebol","Fitness","Ciclismo","Natacao","Campismo"]},
    {"name":"Livros","slug":"livros","subcategories":["Ficcao","Tecnicos","Infantis","Historico","Autoajuda"]},
]
categories = []
cat_ids = []
for cat in category_tree:
    parent_id = fake.uuid4()
    cat_ids.append({"id":parent_id,"name":cat["name"],"slug":cat["slug"]})
    categories.append({"_id":parent_id,"name":cat["name"],"slug":cat["slug"],"parent_id":None,"level":1,"created_at":datetime.utcnow()})
    for sub in cat["subcategories"]:
        sub_id = fake.uuid4()
        cat_ids.append({"id":sub_id,"name":sub,"slug":sub.lower().replace(" ","-")})
        categories.append({"_id":sub_id,"name":sub,"slug":sub.lower().replace(" ","-"),"parent_id":parent_id,"parent_name":cat["name"],"level":2,"created_at":datetime.utcnow()})
db.categories.insert_many(categories)
print(f"  {len(categories)} categorias inseridas.")

print("[2/5] A inserir utilizadores...")
users = []
user_ids = []
for _ in range(1000):
    uid = fake.uuid4()
    user_ids.append(uid)
    users.append({"_id":uid,"name":fake.name(),"email":fake.unique.email(),"country":random.choice(["PT","AO","BR","MZ","CV"]),"created_at":fake.date_time_between(start_date="-3y",end_date="now"),"total_orders":random.randint(0,150),"is_verified":random.choice([True,False])})
db.users.insert_many(users)
print(f"  {len(users)} utilizadores inseridos.")

print("[3/5] A inserir 100000 produtos...")
brands = ["Samsung","Apple","Sony","LG","Nike","Adidas","Zara","IKEA","Bosch","Philips","Dell","HP","Lenovo","Asus","Canon"]
conditions = ["novo","recondicionado","usado - bom estado"]
warehouses = [{"city":"Lisboa","lat":38.7169,"lng":-9.1399},{"city":"Porto","lat":41.1496,"lng":-8.6109},{"city":"Luanda","lat":-8.8368,"lng":13.2343},{"city":"Sao Paulo","lat":-23.5505,"lng":-46.6333}]
product_ids = []
total_inserted = 0
batch = []
for i in range(100000):
    cat = random.choice(cat_ids)
    wh = random.choice(warehouses)
    pid = fake.uuid4()
    product_ids.append(pid)
    price = round(random.uniform(1.99,2999.99),2)
    discount = random.choice([0,5,10,15,20,25,30])
    batch.append({"_id":pid,"sku":f"SKU-{fake.bothify('??####').upper()}","name":f"{random.choice(brands)} {fake.word().capitalize()} {random.randint(1,9000)}","description":fake.paragraph(nb_sentences=3),"brand":random.choice(brands),"category":{"id":cat["id"],"name":cat["name"],"slug":cat["slug"]},"price":{"original":price,"final":round(price*(1-discount/100),2),"discount_pct":discount,"currency":"EUR"},"stock":{"quantity":random.randint(0,5000),"warehouse":wh["city"],"location":{"type":"Point","coordinates":[wh["lng"],wh["lat"]]}},"condition":random.choice(conditions),"tags":random.sample(["promocao","novo","bestseller","premium","economico","exclusivo","limitado"],k=random.randint(1,3)),"rating":{"average":round(random.uniform(1.0,5.0),1),"count":random.randint(0,2000)},"is_active":random.choices([True,False],weights=[90,10])[0],"created_at":fake.date_time_between(start_date="-2y",end_date="now"),"updated_at":datetime.utcnow()})
    if len(batch)==BATCH:
        db.products.insert_many(batch)
        total_inserted+=len(batch)
        batch=[]
        print(f"  {total_inserted}/100000...",end="\r")
if batch:
    db.products.insert_many(batch)
    total_inserted+=len(batch)
print(f"\n  {total_inserted} produtos inseridos.")

print("[4/5] A inserir 50000 reviews...")
review_batch=[]
total_reviews=0
for i in range(50000):
    review_batch.append({"_id":fake.uuid4(),"product_id":random.choice(product_ids),"user_id":random.choice(user_ids),"rating":random.randint(1,5),"title":fake.sentence(nb_words=6),"body":fake.paragraph(nb_sentences=2),"helpful_votes":random.randint(0,500),"verified_purchase":random.choice([True,False]),"created_at":fake.date_time_between(start_date="-2y",end_date="now")})
    if len(review_batch)==BATCH:
        db.reviews.insert_many(review_batch)
        total_reviews+=len(review_batch)
        review_batch=[]
        print(f"  {total_reviews}/50000...",end="\r")
if review_batch:
    db.reviews.insert_many(review_batch)
    total_reviews+=len(review_batch)
print(f"\n  {total_reviews} reviews inseridas.")

print("[5/5] A criar indices...")
db.products.create_index([("name",TEXT),("description",TEXT),("tags",TEXT)],name="idx_text_search")
db.products.create_index([("category.slug",ASCENDING),("price.final",ASCENDING)],name="idx_category_price")
db.products.create_index([("stock.location",GEOSPHERE)],name="idx_geo_location")
db.products.create_index([("rating.average",DESCENDING)],name="idx_rating")
db.products.create_index([("is_active",ASCENDING),("created_at",DESCENDING)],name="idx_active_recent")
db.reviews.create_index([("product_id",ASCENDING),("rating",DESCENDING)],name="idx_review_product")
print("  Indices criados.")

print("\n=============================================")
print("  SEED CONCLUIDO COM SUCESSO!")
print("=============================================")
print(f"  Categorias : {db.categories.count_documents({})}")
print(f"  Utilizadores: {db.users.count_documents({})}")
print(f"  Produtos   : {db.products.count_documents({})}")
print(f"  Reviews    : {db.reviews.count_documents({})}")
print("=============================================")
client.close()
