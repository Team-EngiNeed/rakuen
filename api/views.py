from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NoteSerializer
from .models import Note

# 📌 Special case for Advisers to see notes from Executives in the same section
class AdviserNotesView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.username.endswith("-Adviser"):
            return Note.objects.none()
        section_prefix = user.username.split("-")[0]
        executives = User.objects.filter(username__startswith=f"{section_prefix}-Executive")
        return Note.objects.filter(author__in=executives)

# ✅ Universal list/create view with role-based logic
class RoleBasedNoteListView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        role = self.request.user.username.split("-")[-1]
        if role in ["Executive", "Nurse", "Librarian", "Labtech", "Engineer", "Utility"]:
            return Note.objects.filter(author=self.request.user)
        return Note.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ✅ Universal detail view for retrieve/update
class RoleBasedNoteDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

# ✅ Note Deletion (only delete notes created by self)
class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

# ✅ User registration
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# 🔎 Optional: if you still need a non-role-specific detail view
class NoteDetail(generics.RetrieveUpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
