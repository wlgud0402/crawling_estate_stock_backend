from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celery.decorators import task
from celery.utils.log import get_task_logger
from .email import send_estate_email, send_stock_detail_email, send_stock_email

logger = get_task_logger(__name__)


@task(name="send_estate_task")
def send_estate_task(location, email):
    logger.info("Sent email")
    return send_estate_email(location, email)


@task(name="send_stock_detail_task")
def send_stock_detail_task(name, email):
    logger.info("Sent email")
    return send_stock_detail_email(name, email)


@task(name="send_stock_task")
def send_stock_task(kind, page, email):
    logger.info("Sent email")
    return send_stock_email(kind, page, email)
