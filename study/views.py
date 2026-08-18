from itertools import chain
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    Task,
    Note,
    StudySession,
    Course,
    NoteCategory,
)

from resources.models import Resource


@login_required
def dashboard_view(request):
   
    tasks_count = Task.objects.filter(
        user=request.user,
        status='pending'
    ).count()

    completed_tasks_count = Task.objects.filter(
        user=request.user,
        status='completed'
    ).count()

    notes_count = Note.objects.filter(
        user=request.user
    ).count()

    resources_count = Resource.objects.filter(
        user=request.user
    ).count()

    
    task_stats = {
        'pending': tasks_count,
        'completed': completed_tasks_count,
    }

   
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        status='pending',
        due_date__isnull=False
    ).order_by('due_date')

   
    upcoming_sessions = StudySession.objects.filter(
        user=request.user,
        start_time__isnull=False
    ).order_by('start_time')

    deadlines_list = []

    for task in upcoming_tasks:
        deadlines_list.append({
            'title': f"[Task] {task.title}",
            'date_str': task.due_date.strftime('%Y-%m-%d %H:%M'),
            'timestamp': task.due_date.timestamp(),
        })

    for session in upcoming_sessions:
        deadlines_list.append({
            'title': f"[Session] {session.title}",
            'date_str': session.start_time.strftime('%Y-%m-%d %H:%M'),
            'timestamp': session.start_time.timestamp(),
        })


    deadlines_list = sorted(
        deadlines_list,
        key=lambda x: x['timestamp']
    )[:7]

    deadline_labels = [
        item['title']
        for item in deadlines_list
    ]

    deadline_dates = [
        item['date_str']
        for item in deadlines_list
    ]

   
    tasks = Task.objects.filter(
        user=request.user
    )

    notes = Note.objects.filter(
        user=request.user
    )

    resources = Resource.objects.filter(
        user=request.user
    )

    sessions = StudySession.objects.filter(
        user=request.user
    )

    for task in tasks:
        task.activity_type = 'Task'
        task.timestamp = task.created_at

    for note in notes:
        note.activity_type = 'Note'
        note.timestamp = note.updated_at

    for resource in resources:
        resource.activity_type = 'Resource'
        resource.timestamp = resource.created_at

    for session in sessions:
        session.activity_type = 'Session'
        session.timestamp = session.start_time

    recent_activities = sorted(
        chain(
            tasks,
            notes,
            resources,
            sessions
        ),
        key=attrgetter('timestamp'),
        reverse=True
    )[:6]

    context = {
        'tasks_count': tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'notes_count': notes_count,
        'resources_count': resources_count,
        'recent_activities': recent_activities,
        'task_stats': task_stats,
        'deadline_labels': deadline_labels,
        'deadline_dates': deadline_dates,
    }

    return render(
        request,
        'study/dashboard.html',
        context
    )


@login_required
def tasks_view(request):
    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    tasks = Task.objects.filter(
        user=request.user
    ).select_related(
        'course'
    )

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    tasks = tasks.order_by(
        'status',
        'due_date'
    )

    
    paginator = Paginator(tasks, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    courses = Course.objects.filter(
        user=request.user
    ).order_by('name')

    context = {
        'tasks': page_obj,
        'page_obj': page_obj,
        'courses': courses,
        'search_query': search_query,
    }

    return render(
        request,
        'study/tasks.html',
        context
    )


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get(
            'title',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        due_date = request.POST.get(
            'due_date'
        )

        priority = request.POST.get(
            'priority',
            'medium'
        )

        course_id = request.POST.get(
            'course'
        )

        if not title or not due_date or not course_id:
            return redirect('study:tasks')

        course = get_object_or_404(
            Course,
            id=course_id,
            user=request.user
        )

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
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    if request.method == 'POST':
        title = request.POST.get(
            'title',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        due_date = request.POST.get(
            'due_date'
        )

        priority = request.POST.get(
            'priority',
            'medium'
        )

        course_id = request.POST.get(
            'course'
        )

        if title:
            task.title = title

        task.description = description
        task.due_date = due_date
        task.priority = priority

        if course_id:
            task.course = get_object_or_404(
                Course,
                id=course_id,
                user=request.user
            )

        task.save()

    return redirect('study:tasks')


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

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
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user
    )

    task.delete()

    return redirect('study:tasks')


@login_required
def notes_view(request):
    search_query = request.GET.get(
        'q',
        ''
    ).strip()

    category_id = request.GET.get(
        'category',
        ''
    )

    notes = Note.objects.filter(
        user=request.user
    ).select_related(
        'category'
    ).prefetch_related(
        'courses'
    )

    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    if category_id:
        notes = notes.filter(
            category_id=category_id
        )

    notes = notes.order_by(
        '-updated_at'
    )

   
    paginator = Paginator(notes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = NoteCategory.objects.all()

    courses = Course.objects.filter(
        user=request.user
    ).order_by('name')

    context = {
        'notes': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'courses': courses,
        'search_query': search_query,
        'selected_category': category_id,
    }

    return render(
        request,
        'study/notes.html',
        context
    )


@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST.get(
            'title',
            ''
        ).strip()

        content = request.POST.get(
            'content',
            ''
        ).strip()

        category_id = request.POST.get(
            'category'
        )

        course_ids = request.POST.getlist(
            'courses'
        )

        if not title or not content or not category_id:
            return redirect('study:notes')

        category = get_object_or_404(
            NoteCategory,
            id=category_id
        )

        note = Note.objects.create(
            user=request.user,
            category=category,
            title=title,
            content=content
        )

        valid_courses = Course.objects.filter(
            user=request.user,
            id__in=course_ids
        )

        note.courses.set(
            valid_courses
        )

    return redirect('study:notes')


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    if request.method == 'POST':
        title = request.POST.get(
            'title',
            ''
        ).strip()

        content = request.POST.get(
            'content',
            ''
        ).strip()

        category_id = request.POST.get(
            'category'
        )

        course_ids = request.POST.getlist(
            'courses'
        )

        category = get_object_or_404(
            NoteCategory,
            id=category_id
        )

        note.title = title
        note.content = content
        note.category = category

        note.save()

        valid_courses = Course.objects.filter(
            user=request.user,
            id__in=course_ids
        )

        note.courses.set(
            valid_courses
        )

    return redirect('study:notes')


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(
        Note,
        id=note_id,
        user=request.user
    )

    note.delete()

    return redirect('study:notes')


@login_required
def add_category(request):
    if request.method != 'POST':
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid request.'
            },
            status=400
        )

    name = request.POST.get(
        'name',
        ''
    ).strip()

    if not name:
        return JsonResponse(
            {
                'success': False,
                'error': 'Category name is required.'
            },
            status=400
        )

    category = NoteCategory.objects.filter(
        name__iexact=name
    ).first()

    if category:
        return JsonResponse({
            'success': True,
            'id': category.id,
            'name': category.name
        })

    category = NoteCategory.objects.create(
        name=name
    )

    return JsonResponse({
        'success': True,
        'id': category.id,
        'name': category.name
    })


@login_required
def add_course(request):
    if request.method != 'POST':
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid request.'
            },
            status=400
        )

    name = request.POST.get(
        'name',
        ''
    ).strip()

    if not name:
        return JsonResponse(
            {
                'success': False,
                'error': 'Course name is required.'
            },
            status=400
        )

    course = Course.objects.filter(
        user=request.user,
        name__iexact=name
    ).first()

    if course:
        return JsonResponse({
            'success': True,
            'id': course.id,
            'name': course.name,
            'existing': True
        })

    course = Course.objects.create(
        user=request.user,
        name=name
    )

    return JsonResponse({
        'success': True,
        'id': course.id,
        'name': course.name,
        'existing': False
    })


@login_required
def study_sessions_view(request):
    sessions = StudySession.objects.filter(
        user=request.user
    ).order_by(
        '-start_time'
    )

    return render(
        request,
        'study/sessions.html',
        {
            'sessions': sessions
        }
    )


@login_required
def add_study_session(request):
    if request.method == 'POST':
        title = request.POST.get(
            'title',
            ''
        ).strip()

        start_time = request.POST.get(
            'start_time'
        )

        end_time = request.POST.get(
            'end_time'
        )

        duration = request.POST.get(
            'duration'
        )

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

        if (
            title
            and start_time
            and end_time
            and duration
        ):
            StudySession.objects.create(
                user=request.user,
                title=title,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                notes=notes
            )

    return redirect(
        'study:study_sessions'
    )