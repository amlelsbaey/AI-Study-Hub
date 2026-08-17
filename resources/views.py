from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from .models import Resource, ResourceType


@login_required
def resources_view(request):
    search_query = request.GET.get('q', '')
    type_id = request.GET.get('type', '')

    resources = Resource.objects.filter(
        user=request.user
    )

    if search_query:
        resources = resources.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if type_id:
        resources = resources.filter(
            resource_type_id=type_id
        )

    resources = resources.order_by('-created_at')

    resource_types = ResourceType.objects.all()

    context = {
        'resources': resources,
        'resource_types': resource_types,
        'search_query': search_query,
        'selected_type': type_id,
    }

    return render(
        request,
        'resources/resources.html',
        context
    )


@login_required
def add_resource_type(request):
    if request.method != 'POST':
        return JsonResponse(
            {
                'success': False,
                'error': 'Invalid request method.'
            },
            status=405
        )

    name = request.POST.get('name', '').strip()

    if not name:
        return JsonResponse(
            {
                'success': False,
                'error': 'Resource type name is required.'
            },
            status=400
        )

    resource_type = ResourceType.objects.filter(
        name__iexact=name
    ).first()

    if resource_type:
        return JsonResponse({
            'success': True,
            'id': resource_type.id,
            'name': resource_type.name,
            'existing': True
        })

    resource_type = ResourceType.objects.create(
        name=name
    )

    return JsonResponse({
        'success': True,
        'id': resource_type.id,
        'name': resource_type.name,
        'existing': False
    })


@login_required
def add_resource(request):
    if request.method == 'POST':

        title = request.POST.get(
            'title',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        type_id = request.POST.get(
            'resource_type'
        )

        link = request.POST.get(
            'link',
            ''
        ).strip()

        uploaded_file = request.FILES.get(
            'file'
        )

        resource_type = get_object_or_404(
            ResourceType,
            id=type_id
        )

        if title and (link or uploaded_file):

            Resource.objects.create(
                user=request.user,
                resource_type=resource_type,
                title=title,
                description=description,
                link=link,
                file=uploaded_file
            )

    return redirect(
        'resources:resources_list'
    )


@login_required
def delete_resource(request, resource_id):

    resource = get_object_or_404(
        Resource,
        id=resource_id,
        user=request.user
    )

    resource.delete()

    return redirect(
        'resources:resources_list'
    )