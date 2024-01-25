var username = process.env.MONGO_INITDB_ROOT_USERNAME || "root";
var password = process.env.MONGO_INITDB_ROOT_PASSWORD || "password";
var database = process.env.MONGO_INITDB_DATABASE || "candles";
var collection = process.env.MONGO_INITDB_COLLECTION || "candles";

db.auth(username, password);

db.createUser({
    user: username,
    pwd: password,
    roles: [{ role: "readWrite", db: database }]
});

db.createCollection(collection);