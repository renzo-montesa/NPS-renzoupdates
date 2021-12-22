from extensions import celery, create_app
from celery.utils.log import get_task_logger


app = create_app('config')
app.app_context().push()

logger = get_task_logger(__name__)
