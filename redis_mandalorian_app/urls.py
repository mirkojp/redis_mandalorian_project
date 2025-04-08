from django.urls import path
from .views import (
    ChapterListCreateView,
    ChapterDetailView,
    reserve_chapter,
    confirm_payment,
)

urlpatterns = [
    path("chapters/", ChapterListCreateView.as_view(), name="chapter-list"),
    path("chapters/<uuid:pk>/", ChapterDetailView.as_view(), name="chapter-detail"),
    path("chapters/<uuid:pk>/reserve/", reserve_chapter, name="chapter-reserve"),
    path(
        "chapters/<uuid:pk>/confirm_payment/", confirm_payment, name="chapter-payment"
    ),
]
