from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from .models import Task, Note, StudySession, Course, NoteCategory
from resources.models import Resource

@login_required
def dashboard_view(request):
    tasks_count = Task.objects.filter(user=request.user, status='pending').count()
    notes_count = Note.objects.filter(user=request.user).count()
    resources_count = Resource.objects.filter(user=request.user).count()
   
    # 🌟 Recent Activity (Unified Stream)
    tasks = Task.objects.filter(user=request.user)
    notes = Note.objects.filter(user=request.user)
    resources = Resource.objects.filter(user=request.user)
    sessions = StudySession.objects.filter(user=request.user)
   
    for t in tasks:
        t.activity_type = 'Task'
        t.timestamp = t.created_at
    for n in notes:
        n.activity_type = 'Note'
        n.timestamp = n.updated_at
    for r in resources:
        r.activity_type = 'Resource'
        r.timestamp = r.created_at
    for s in sessions:
        s.activity_type = 'Session'
        s.timestamp = s.start_time

    recent_activities = sorted(
        chain(tasks, notes, resources, sessions),
        key=attrgetter('timestamp'),
        reverse=True
    )[:6]

    context = {
        'tasks_count': tasks_count,
        'notes_count': notes_count,
        'resources_count': resources_count,
        'recent_activities': recent_activities,
    }
    return render(request, 'study/dashboard.html', context)


# --- TASKS VIEWS ---
@login_required
def tasks_view(request):
    search_query = request.GET.get('q', '')
    tasks = Task.objects.filter(user=request.user)
   
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
       
    tasks = tasks.order_by('status', 'due_date')
    courses = Course.objects.filter(user=request.user)
   
    context = {
        'tasks': tasks,
        'courses': courses,
        'search_query': search_query
    }
    return render(request, 'study/tasks.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority', 'medium')
        course_id = request.POST.get('course')
       
        course = get_object_or_404(Course, id=course_id, user=request.user)
       
        if title and due_date:
            Task.objects.create(
                user=request.user,
                course=course,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority
            )
    return redirect('study:tasks')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.due_date = request.POST.get('due_date')
        task.priority = request.POST.get('priority')
        course_id = request.POST.get('course')
        task.course = get_object_or_404(Course, id=course_id, user=request.user)
        task.save()
    return redirect('study:tasks')

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if task.status == 'pending':
        task.status = 'completed'
        task.completed_at = timezone.now()
    else:
        task.status = 'pending'
        task.completed_at = None
    task.save()
    return redirect('study:tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('study:tasks')


# --- NOTES VIEWS ---
@login_required
def notes_view(request):
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
   
    notes = Note.objects.filter(user=request.user)
   
    if search_query:
        notes = notes.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    if category_id:
        notes = notes.filter(category_id=category_id)
       
    notes = notes.order_by('-updated_at')
    categories = NoteCategory.objects.all()
    courses = Course.objects.filter(user=request.user)
   
    context = {
        'notes': notes,
        'categories': categories,
        'courses': courses,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'study/notes.html', context)

@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        course_ids = request.POST.getlist('courses')
       
        category = get_object_or_404(NoteCategory, id=category_id)
       
        if title and content:
            note = Note.objects.create(
                user=request.user,
                category=category,
                title=title,
                content=content
            )
            if course_ids:
                note.courses.set(course_ids)
               
    return redirect('study:notes')

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        category_id = request.POST.get('category')
        course_ids = request.POST.getlist('courses')
       
        note.category = get_object_or_404(NoteCategory, id=category_id)
        note.save()
        note.courses.set(course_ids)
    return redirect('study:notes')

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('study:notes')


# --- STUDY SESSIONS ---
@login_required
def study_sessions_view(request):
    sessions = StudySession.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'study/sessions.html', {'sessions': sessions})

@login_required
def add_study_session(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        duration = request.POST.get('duration')
        notes = request.POST.get('notes', '')
       
        if title and start_time and end_time and duration:
            StudySession.objects.create(
                user=request.user,
                title=title,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                notes=notes
            )
    return redirect('study:study_sessions')