from extensions import celery


@celery.task
def reverse(string):
    return string[::-1]
