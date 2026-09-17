from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DonorProfileForm, DonorSearchForm
from .models import DonorProfile


def donor_list_view(request):
    donors = DonorProfile.objects.select_related('user').all()
    form = DonorSearchForm(request.GET or None)

    if form.is_valid():
        blood_group = form.cleaned_data.get('blood_group')
        location = form.cleaned_data.get('location')
        availability = form.cleaned_data.get('availability')

        if blood_group:
            donors = donors.filter(blood_group=blood_group)
        if location:
            donors = donors.filter(location__icontains=location)
        if availability:
            donors = donors.filter(availability=availability)

    paginator = Paginator(donors, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'donors/donor_list.html', {
        'page_obj': page_obj,
        'form': form,
    })


def donor_detail_view(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk)
    return render(request, 'donors/donor_detail.html', {'donor': donor})


@login_required
def donor_create_view(request):
    if hasattr(request.user, 'donor_profile'):
        messages.info(request, 'You already have a donor profile. You can edit it below.')
        return redirect('donors:edit', pk=request.user.donor_profile.pk)

    if request.method == 'POST':
        form = DonorProfileForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, 'You are now registered as a donor. Thank you!')
            return redirect('donors:detail', pk=donor.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        initial = {
            'name': request.user.profile.full_name,
            'phone_number': request.user.profile.phone_number,
            'blood_group': request.user.profile.blood_group,
            'location': request.user.profile.location,
        }
        form = DonorProfileForm(initial=initial)

    return render(request, 'donors/donor_form.html', {'form': form, 'action': 'Become a Donor'})


@login_required
def donor_edit_view(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk)
    if donor.user != request.user:
        messages.error(request, 'You are not allowed to edit this donor profile.')
        return redirect('donors:detail', pk=pk)

    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donor profile updated successfully.')
            return redirect('donors:detail', pk=donor.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = DonorProfileForm(instance=donor)

    return render(request, 'donors/donor_form.html', {'form': form, 'action': 'Update Donor Profile'})


@login_required
def donor_delete_view(request, pk):
    donor = get_object_or_404(DonorProfile, pk=pk)
    if donor.user != request.user:
        messages.error(request, 'You are not allowed to delete this donor profile.')
        return redirect('donors:detail', pk=pk)

    if request.method == 'POST':
        donor.delete()
        messages.success(request, 'Your donor profile has been deleted.')
        return redirect('donors:list')

    return render(request, 'donors/donor_confirm_delete.html', {'donor': donor})
