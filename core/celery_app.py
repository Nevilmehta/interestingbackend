from celery import Celery

celery_app = Celery(
    "BACKEND_CONCEPTS",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer = "json",
    accept_content = ["json"],
    result_serializer = "json",
    timezone = "UTC",
    enable_utc = True
)

celery_app.autodiscover_tasks(["core.tasks"])
# connect celery to redis and can never run directly
# Without autodiscover_tasks, Celery never loads email.py