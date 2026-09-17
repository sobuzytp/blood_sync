from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BloodRequestForm, BloodRequestSearchForm, BloodRequestStatusForm
from .models import BloodRequest


def request_list_view(request):
    blood_requests = BloodRequest.objects.select_related('requester').all()
    form = BloodRequestSearchForm(request.GET or None)

    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        status = form.cleaned_data.get('status')

        if blood_group:
            blood_requests = blood_requests.filter(blood_group=blood_group)
        if location:
            blood_requests = blood_requests.filter(location__icontains=location)
        if status:
            blood_requests = blood_requests.filter(status=status)
        elif not any(form.cleaned_data.values()):
            # By default show only active (pending) requests on the public listing
            pass

    paginator = Paginator(blood_requests, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'requests_app/request_list.html', {
        'page_obj': page_obj,
        'form': form,
    })


def request_detail_view(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'requests_app/request_detail.html', {'blood_request': blood_request})


@login_required
def request_create_view(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()
            messages.success(request, 'Your blood request has been posted.')
            return redirect('requests_app:detail', pk=blood_request.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = BloodRequestForm()

    return render(request, 'requests_app/request_form.html', {'form': form, 'action': 'Create Blood Request'})


@login_required
def request_edit_view(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if blood_request.requester != request.user:
        messages.error(request, 'You are not allowed to edit this request.')
        return redirect('requests_app:detail', pk=pk)

    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood request updated successfully.')
            return redirect('requests_app:detail', pk=blood_request.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = BloodRequestForm(instance=blood_request)

    return render(request, 'requests_app/request_form.html', {'form': form, 'action': 'Edit Blood Request'})


@login_required
def request_delete_view(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if blood_request.requester != request.user:
        messages.error(request, 'You are not allowed to delete this request.')
        return redirect('requests_app:detail', pk=pk)

    if request.method == 'POST':
        blood_request.delete()
        messages.success(request, 'Blood request deleted.')
        return redirect('requests_app:my_requests')

    return render(request, 'requests_app/request_confirm_delete.html', {'blood_request': blood_request})


@login_required
def request_status_update_view(request, pk):
    blood_request = get_object_or_404(BloodRequest, pk=pk)
    if blood_request.requester != request.user:
        messages.error(request, 'You are not allowed to update this request.')
        return redirect('requests_app:detail', pk=pk)

    if request.method == 'POST':
        form = BloodRequestStatusForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request status updated.')
        return redirect('requests_app:detail', pk=pk)

    return redirect('requests_app:detail', pk=pk)


@login_required
def my_requests_view(request):
    blood_requests = BloodRequest.objects.filter(requester=request.user)
    return render(request, 'requests_app/my_requests.html', {'blood_requests': blood_requests})
