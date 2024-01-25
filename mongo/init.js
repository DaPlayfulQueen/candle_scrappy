var username = process.env.MONGO_USERNAME || "root";
var password = process.env.MONGO_PASSWORD || "password";
var database = process.env.MONGO_DATABASE || "candles";
var collection = process.env.MONGO_COLLECTION || "candles";

db.createUser({
    user: username,
    pwd: password,
    roles: [{ role: "readWrite", db: database }]
});

db.createCollection(collection);