from fastack.globals import state
from werkzeug.local import LocalProxy

from fastack_migrate import MigrateConfig

migrate: MigrateConfig = LocalProxy(lambda: getattr(state, "migrate", None))
