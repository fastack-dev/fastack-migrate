DEBUG = True
PLUGINS = ["fastack_sqlmodel", "fastack_migrate"]
COMMANDS = []
DB_USER = "fastack_user"
DB_PASSWORD = "fastack_pass"
DB_HOST = "db"
DB_PORT = 5432
DB_NAME = "fastack_db"
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_OPTIONS = {}
