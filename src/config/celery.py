import os

from celery import Celery
from celery.signals import import_modules

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")
app = Celery("src")

# Load Celery configuration from Django settings with `CELERY_` prefix for related keys.
app.config_from_object("django.conf:settings")
# Auto-discover tasks from all registered Django apps.
app.autodiscover_tasks()

PERIODIC_TASKS = []


# Using `import_modules` signal to setup periodic tasks.
# When this signal fires, `PERIODIC_TASKS` is adequately populated
# after Celery processes all the INSTALLED_APPS.
@import_modules.connect
def setup_periodic_task(sender, **kwargs):
    for entry in PERIODIC_TASKS:
        # TODO: Handle periodic tasks that require arguments.

        task = entry["task"]
        sender.add_periodic_task(
            entry["schedule"],
            task.s(),
            name=entry["name"],
            # `add_periodic_task` accepts additional arguments like `apply_async`.
            **entry["options"],
        )
