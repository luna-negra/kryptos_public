// Set variables
const db_name = process.env.MONGO_INITDB_KRYPTOS_DBNAME || "THIS_IS_SECRET";
const username = process.env.MONGO_INITDB_KRYPTOS_USERNAME || "THIS_IS_SECRET";
const password = process.env.MONGO_INITDB_KRYPTOS_PASSWORD || "THIS_IS_SECRET";

// Connect to Database
db = db.getSiblingDB(db_name);

// Create User for Database
db.createUser({
  user: username,
  pwd: password,
  roles: [
    {role: "readWrite", db: db_name}
  ],
});

// Drop all superuser
db = db.getSiblingDB("admin");
db.system.users.find({ "roles.role": "root" }).forEach(user => {
    db.dropUser(user.user);
});
