from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta
from .models import Chapter
from .serializers import ChapterSerializer
from .tasks import release_chapter
from rest_framework.decorators import api_view


# Lista todos los capítulos y permite crear uno nuevo
class ChapterListCreateView(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


# Recupera, actualiza o elimina un capítulo específico
class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer


@api_view(["POST"])
def reserve_chapter(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if chapter.status != "disponible":
        return Response(
            {"error": "Capítulo no disponible"}, status=status.HTTP_400_BAD_REQUEST
        )

    chapter.status = "reservado"
    chapter.reserved_at = now()
    chapter.save()

    # Lanza la tarea de liberación en 4 minutos
    release_chapter.apply_async((str(chapter.id),), countdown=240)

    return Response({"message": "Capítulo reservado por 4 minutos"})


@api_view(["POST"])
def confirm_payment(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if chapter.status != "reservado":
        return Response(
            {"error": "Capítulo no reservado"}, status=status.HTTP_400_BAD_REQUEST
        )

    chapter.status = "alquilado"
    chapter.rented_until = now() + timedelta(hours=24)
    chapter.save()

    return Response({"message": "Capítulo alquilado por 24 horas"})
