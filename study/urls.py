from django.urls import path
from . import views


app_name = 'study'


urlpatterns = [
    
    path(
        'dashboard/',
        views.dashboard_view,
        name='dashboard'
    ),

    path(
        'tasks/',
        views.tasks_view,
        name='tasks'
    ),
    path(
        'tasks/add/',
        views.add_task,
        name='add_task'
    ),
    path(
        'tasks/<int:task_id>/edit/',
        views.edit_task,
        name='edit_task'
    ),
    path(
        'tasks/<int:task_id>/toggle/',
        views.toggle_task,
        name='toggle_task'
    ),
    path(
        'tasks/<int:task_id>/delete/',
        views.delete_task,
        name='delete_task'
    ),

    path(
        'notes/',
        views.notes_view,
        name='notes'
    ),
    path(
        'notes/add/',
        views.add_note,
        name='add_note'
    ),
    path(
        'notes/<int:note_id>/edit/',
        views.edit_note,
        name='edit_note'
    ),
    path(
        'notes/<int:note_id>/delete/',
        views.delete_note,
        name='delete_note'
    ),

    path(
        'note-categories/add/',
        views.add_category,
        name='add_category'
    ),

   
    path(
        'courses/add/',
        views.add_course,
        name='add_course'
    ),

    path(
        'sessions/',
        views.study_sessions_view,
        name='study_sessions'
    ),
    path(
        'sessions/add/',
        views.add_study_session,
        name='add_study_session'
    ),
]