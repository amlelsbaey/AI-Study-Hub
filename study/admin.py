from django.contrib import admin
from .models import Course, Task, NoteCategory, Note, StudySession
# Register your models here.

admin.site.register(Course)
admin.site.register(Task)
admin.site.register(NoteCategory)
admin.site.register(Note)
admin.site.register(StudySession)