# Celery Learning

Commands:
- docker-compose up --build

When adding a worker that is not inside the docker, we can use
```python
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "group1.tasks",
        "group2.tasks",
    ],
)
```
