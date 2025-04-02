
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now, timedelta
from .models import Chapter
from .serializers import ChapterSerializer
from .tasks import release_chapter


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    @action(detail=True, methods=["post"])
    def reserve(self, request, pk=None):
        chapter = self.get_object()
        if chapter.status != "disponible":
            return Response(
                {"error": "Capítulo no disponible"}, status=status.HTTP_400_BAD_REQUEST
            )

        chapter.status = "reservado"
        chapter.reserved_at = now()
        chapter.save()
        release_chapter.apply_async((chapter.id,), countdown=240)  # 4 minutos
        return Response({"message": "Capítulo reservado por 4 minutos"})

    @action(detail=True, methods=["post"])
    def confirm_payment(self, request, pk=None):
        chapter = self.get_object()
        if chapter.status != "reservado":
            return Response(
                {"error": "Capítulo no reservado"}, status=status.HTTP_400_BAD_REQUEST
            )

        chapter.status = "alquilado"
        chapter.rented_until = now() + timedelta(hours=24)
        chapter.save()
        return Response({"message": "Capítulo alquilado por 24 horas"})
