from celery import shared_task
from django.utils.timezone import now
from .models import Chapter
import logging
logger = logging.getLogger(__name__)

@shared_task
def release_chapter(chapter_id):
    logger.info(f"Intentando liberar capítulo: {chapter_id}")
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        if chapter.status == "reservado" and chapter.reserved_at:
            if (now() - chapter.reserved_at).total_seconds() >= 240:
                chapter.status = "disponible"
                chapter.reserved_at = None
                chapter.save()
                logger.info(f"Capítulo {chapter_id} liberado.")
    except Chapter.DoesNotExist:
        logger.warning(f"Capítulo {chapter_id} no existe.")
