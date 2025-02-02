from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.NoteListCreate.as_view(), name="note-list"),
    path("notes/engineer/", views.NoteListEngineer.as_view(), name="note-engineer"),
    path("notes/engineer/<int:pk>", views.NoteListEngineer.as_view(), name="note-engineer"),
    path("notes/utility/", views.NoteListUtility.as_view(), name="note-engineer"),
    path("notes/executive/", views.NoteListExecutive.as_view(), name="note-view"),
    path("notes/executive/<int:pk>", views.NoteDetailExecutive.as_view(), name="note-view"),
    path("notes/nurse/", views.NoteListNurse.as_view(), name="note-view"),
    path("notes/librarian/", views.NoteListLibrarian.as_view(), name="note-view"),
    path("notes/labtech/", views.NoteListLabtech.as_view(), name="note-view"),
    path('notes/adviser/', views.AdviserNotesView.as_view(), name='adviser-notes'),
    path('notes/<int:id>/', views.NoteDetail.as_view(), name='note-detail'),
    path('notes/delete/<int:pk>/', views.NoteDelete.as_view(), name='delete-note'),
]

