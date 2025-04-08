
from django.urls import path
from .views import (
    RoleBasedNoteListView,
    RoleBasedNoteDetailView,
    NoteDelete,
    CreateUserView,
)

urlpatterns = [
    path("user/register/", CreateUserView.as_view(), name="register"),
    path("notes/", RoleBasedNoteListView.as_view(), name="note-list"),
    path("notes/<int:pk>/", RoleBasedNoteDetailView.as_view(), name="note-detail"),
    path("notes/delete/<int:pk>/", NoteDelete.as_view(), name="delete-note"),
]
