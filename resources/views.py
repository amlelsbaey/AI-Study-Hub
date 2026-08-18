from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Resource, ResourceType

@login_required
def resources_view(request):
    search_query = request.GET.get('q', '')
    type_id = request.GET.get('type', '')
    
    resources_list = Resource.objects.filter(user=request.user).select_related('resource_type')
    
    if search_query:
        resources_list = resources_list.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
    if type_id:
        resources_list = resources_list.filter(resource_type_id=type_id)
        
    resources_list = resources_list.order_by('-created_at')
    
    paginator = Paginator(resources_list, 10)  # 10 عناصر في كل صفحة
    page_number = request.GET.get('page')
    resources = paginator.get_page(page_number)
    
    resource_types = ResourceType.objects.all()
    
    context = {
        'resources': resources,
        'resource_types': resource_types,
        'search_query': search_query,
        'selected_type': type_id,
    }
    return render(request, 'resources/resources.html', context)

@login_required
def add_resource(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        description = request.POST.get('description', '')
        type_id = request.POST.get('resource_type')
        
        resource_type = get_object_or_404(ResourceType, id=type_id)
        
        if title and link:
            Resource.objects.create(
                user=request.user,
                resource_type=resource_type,
                title=title,
                link=link,
                description=description
            )
    return redirect('resources:resources_list')

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, user=request.user)
    resource.delete()
    return redirect('resources:resources_list')