from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import pgettext_lazy

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from .filters import GroupFilter
from .forms import GroupPermissionsForm


@staff_member_required
@permission_required('userprofile.view_group')
def group_list(request):
    groups = (Group.objects.all().prefetch_related('permissions')
              .order_by('name'))
    group_filter = GroupFilter(request.GET, queryset=groups)
    groups = [{'name': group, 'permissions': group.permissions.all()}
              for group in group_filter.qs]
    groups = get_paginator_items(
        groups, settings.DASHBOARD_PAGINATE_BY, request.GET.get('page'))
    ctx = {'groups': groups, 'filter': group_filter}
    return TemplateResponse(request, 'dashboard/group/list.html', ctx)


@staff_member_required
@permission_required('userprofile.edit_group')
def group_create(request):
    group = Group()
    form = GroupPermissionsForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            pgettext_lazy('Dashboard message',
                          'Created group'))
        return redirect('dashboard:group-list')
    ctx = {'group': group, 'form': form}
    return TemplateResponse(request, 'dashboard/group/detail.html', ctx)


@staff_member_required
@permission_required('userprofile.edit_group')
def group_details(request, pk):
    group = Group.objects.get(pk=pk)
    form = GroupPermissionsForm(request.POST or None, instance=group)
    if form.is_valid():
        form.save()
        messages.success(
            request,
            pgettext_lazy('Dashboard message', 'Updated group %s') % group.name
        )
        return redirect('dashboard:group-list')
    ctx = {'group': group, 'form': form}
    return TemplateResponse(request, 'dashboard/group/detail.html', ctx)


@staff_member_required
@permission_required('userprofile.edit_group')
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        group.delete()
        messages.success(
            request,
            pgettext_lazy('Dashboard message', 'Removed group %s') % group
        )
        return redirect('dashboard:group-list')
    return TemplateResponse(
        request, 'dashboard/group/modal/confirm_delete.html', {'group': group})
