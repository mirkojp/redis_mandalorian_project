from celery import shared_task
from django.utils.timezone import now
from .models import Chapter


def release_chapter(chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    if (
        chapter.status == "reservado"
        and chapter.reserved_at
        and (now() - chapter.reserved_at).total_seconds() >= 240
    ):
        chapter.status = "disponible"
        chapter.reserved_at = None
        chapter.save()
