# fastack-migrate

fastack-migrate is a database migration tool for FastAPI.
This is a fork of [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate)!

# Usage

Install plugin:

```
pip install fastack-migrate
```

Add the plugin to your project configuration:

```python
PLUGINS = [
    "fastack.plugins.sqlmodel",
    "fastack_migrate",
    ...
]
```

And initialize your project with alembic template:

```
fastack db init
```

Then check if there are any changes in ``app.models``:

```
fastack db migrate
```

Update all changes in ``app.models``:

```
fastack db upgrade
```

For more, please visit https://flask-migrate.readthedocs.io/en/latest/
