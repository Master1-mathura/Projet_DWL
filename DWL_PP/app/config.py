import os

DB_CONFIG = {
    # On récupère la variable d'environnement définie dans docker-compose
    # S'il ne la trouve pas, il utilisera "localhost" par défaut
    "host" : os.environ.get("DB_HOST", "localhost"),
    "user" : os.environ.get("DB_USER", "root"),
    "password" : os.environ.get("DB_PASSWORD", "123456"),
    "database" : os.environ.get("DB_NAME", "watchlist_api"),
    "port" : os.environ.get("DB_PORT", "4000")
}