from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from booking.models import Bookings
from django import forms
from .forms import UsersCheckboxForm, FinalizeDiscardForm, NotesForm
from django.contrib import messages
from django.views import generic
from .filters import UsersFilter, BookingsFilter, AdminArchiveFilter, FinalizeFilter
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils import timezone


def admin_panel(request):
    """
    Render admin panel
    """
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, "admin_panel.html")


class AdminUsersView(generic.ListView):
    """
    Class for admin users page
    """
    template_name = "admin_users.html"
    model = User
    form_class = forms.modelformset_factory(User, UsersCheckboxForm, extra=0)
    context_object_name = 'students'

    def get_context_data(self, *args, **kwargs):
        context = super(AdminUsersView, self).get_context_data(*args,**kwargs)
        user_filter = User.objects.all()
        context['formset'] = self.form_class
        context['users_filter'] = UsersFilter(self.request.GET, queryset=user_filter)
        return context
    
    def get(self, request):
        """
        Limit access to superuser
        """
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request)


def activate_users(request):
    """
    Activate inactive users
    """
    if request.method == 'POST':
        ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in request.POST.get('hidden-ids')) # Convert JS value into list of numbers
        ids_list = [i for i in ids.split()] # Convert JS value into list of numbers
        [User.objects.filter(id=id).update(is_active=True) for id in ids_list]
        messages.success(request, 'User(s) activated.')
        return redirect('admin_users:admin_users')
        
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, 'activate_users.html')


def inactivate_users(request):
    """
    Inactivate inactive users
    """
    if request.method == 'POST':
        ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in request.POST.get('hidden-ids-inact')) # Convert JS value into list of numbers
        ids_list = [i for i in ids.split()] # Convert JS value into list of numbers
        [User.objects.filter(id=id).update(is_active=False) for id in ids_list]
        messages.success(request, 'User(s) inactivated.')
        return redirect('admin_users:admin_users')
    
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, 'inactivate_users.html')


def delete_users(request):
    """
    Delete users
    """
    if request.method == 'POST':
        ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in request.POST.get('hidden-ids-del')) # Convert JS value into list of numbers
        ids_list = [i for i in ids.split()] # Convert JS value into list of numbers
        [User.objects.filter(id=id).delete() for id in ids_list]
        messages.success(request, 'User(s) deleted.')
        return redirect('admin_users:admin_users')
        
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, 'delete_users.html')


class AdminReviewView(generic.ListView):
    """
    Class for admin review page
    """
    template_name = "admin_review.html"
    model = Bookings

    def get_context_data(self, *args, **kwargs):
        context = super(AdminReviewView, self).get_context_data(*args,**kwargs)
        bookings_confirmed = Bookings.objects.filter(status=True)
        context['bookings_filter'] = BookingsFilter(self.request.GET, queryset=bookings_confirmed)
        return context
    
    def post(self, request):
        """
        Change lesson status
        """
        if request.method == 'POST':
            id = request.POST.get('admin-status-id')
            status = request.POST.get('admin-status-submit')
            bulk_confirm = request.POST.get('bulk-confirm-user-id')
            bulk_to_pending = request.POST.get('bulk-to-pending-user-id')
            bulk_cancel = request.POST.get('bulk-cancel-user-id')
            if id:
                Bookings.objects.filter(id=id).update(confirmed=status, 
                        notes=Bookings.objects.get(id=id).notes + \
                        timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                        ", " + status + ",")
                messages.success(request, 'Saved.')
                return HttpResponseRedirect(reverse('admin_review:admin_review'))
            elif bulk_confirm:
                review_ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in bulk_confirm) # Convert JS value into list of numbers
                review_ids_list = [i for i in review_ids.split()] # Convert JS value into list of numbers
                [Bookings.objects.filter(id=id).update(confirmed='Confirmed', 
                            notes=Bookings.objects.get(id=id).notes + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            "," + \
                            " Confirmed,") for id in review_ids_list]
                messages.success(request, 'Lesson(s) confirmed.')
                return HttpResponseRedirect(reverse('admin_review:admin_review'))
            elif bulk_to_pending:
                review_ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in bulk_to_pending) # Convert JS value into list of numbers
                review_ids_list = [i for i in review_ids.split()] # Convert JS value into list of numbers
                [Bookings.objects.filter(id=id).update(confirmed='Pending', 
                            notes=Bookings.objects.get(id=id).notes + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            "," + \
                            " Pending,") for id in review_ids_list]
                messages.success(request, 'Lesson(s) set to pending.')
                return HttpResponseRedirect(reverse('admin_review:admin_review'))
            elif bulk_cancel:
                review_ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in bulk_cancel) # Convert JS value into list of numbers
                review_ids_list = [i for i in review_ids.split()] # Convert JS value into list of numbers
                [Bookings.objects.filter(id=id).update(confirmed='Cancelled', 
                            notes=Bookings.objects.get(id=id).notes + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            "," + \
                            " Cancelled,") for id in review_ids_list]
                messages.success(request, 'Lesson(s) cancelled.')
                return HttpResponseRedirect(reverse('admin_review:admin_review'))
    
    def get(self, request):
        """
        Limit access to superuser
        """
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request)


class AdminChartsView(generic.ListView):
    """
    Class for admin review page
    """
    template_name = "admin_charts.html"
    model = Bookings

    def get(self, request):
        """
        Limit access to superuser
        """
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request)


class AdminArchiveView(generic.ListView):
    """
    Class for admin archive page
    """
    template_name = "admin_archive.html"
    model = Bookings
    paginate_by = 8
    
    def get_queryset(self):
        queryset = Bookings.objects.filter(Q(finalized='Finalized') | Q(finalized='Discarded'), status=False)
        self.filterset_class = AdminArchiveFilter
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, *args, **kwargs):
        context = super(AdminArchiveView, self).get_context_data(*args,**kwargs)
        context['bookings_past'] = self.filterset
        return context

    def get(self, request):
        """
        Limit access to superuser
        """
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request)
    

def admin_lesson_details(request, booking_id):
    """
    Render lesson details page
    """
    booking = get_object_or_404(Bookings, Q(finalized='Finalized') | Q(finalized='Discarded'), id=booking_id, status=False)
    instance = Bookings.objects.get(id=booking_id)
    listt = Bookings.get_notes(booking).split(",")[:-1]
    tuple_of_lists = [(listt[i].strip(), listt[i+1].strip(), listt[i+2].strip()) for i in range(0, len(listt), 3)], # Convert list into tuple of lists
    if request.method == 'POST':
        if request.POST['comms']:
            _mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['comms'] = booking.comms + \
                                    "\n" + \
                                    request.POST['comms'] + \
                                    "\n" + \
                                    "<" + \
                                    timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                                    ">\n"
            request.POST._mutable = _mutable
        form = NotesForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note added.')
            return HttpResponseRedirect(request.path_info)
    context = {
        'details_student': Bookings.get_student(booking),
        'details_lesson': Bookings.get_lesson(booking),
        'details_lesson_type': Bookings.get_lesson_type(booking),
        'details_date': Bookings.get_date(booking),
        'details_time': Bookings.get_time(booking),
        'details_confirmed': Bookings.get_confirmed(booking),
        'details_finalized': Bookings.get_finalized(booking),
        'details_notes': tuple_of_lists[0],
        'details_date_booked': Bookings.get_datetime_booked(booking),
        'details_comms': Bookings.get_comms(booking),
        'details_notes_form': NotesForm
        }
    if not request.user.is_superuser:
        raise PermissionDenied
    return render(request, 'lesson_details.html', context)


class AdminFinalizeView(generic.ListView):
    """
    Class for admin finalize page
    """
    template_name = "admin_finalize.html"
    model = Bookings
    form = FinalizeDiscardForm

    def get_context_data(self, *args, **kwargs):
        context = super(AdminFinalizeView, self).get_context_data(*args,**kwargs)
        bookings_confirmed = Bookings.objects.filter(status=False, finalized='Not finalized')
        context['bookings_filter'] = FinalizeFilter(self.request.GET, queryset=bookings_confirmed)
        context['finalize_form'] = self.form
        return context
    
    def post(self, request):
        """
        Change finalize status
        """
        if request.method == 'POST':
            id = request.POST.get('admin-fin-id')
            status = request.POST.get('admin-fin-submit')
            bulk_finalize = request.POST.get('bulk-finalize-user-id')
            bulk_discard = request.POST.get('bulk-discard-user-id')
            if id:
                Bookings.objects.filter(id=id).update(finalized=status, 
                        notes=Bookings.objects.get(id=id).notes + \
                        timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                        "," + status + ",")
                messages.success(request, 'Saved.')
                return HttpResponseRedirect(reverse('admin_finalize:admin_finalize'))
            elif bulk_finalize:
                review_ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in bulk_finalize) # Convert JS value into list of numbers
                review_ids_list = [i for i in review_ids.split()] # Convert JS value into list of numbers
                [Bookings.objects.filter(id=id).update(finalized='Finalized', 
                            notes=Bookings.objects.get(id=id).notes + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            "," + \
                            " Finalized,", comms=request.POST.get('comms') + \
                            "\n" + \
                            "<" + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            ">" + \
                            "\n") for id in review_ids_list]
                messages.success(request, 'Lesson(s) finalized.')
                return HttpResponseRedirect(reverse('admin_finalize:admin_finalize'))
            elif bulk_discard:
                review_ids = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in bulk_discard) # Convert JS value into list of numbers
                review_ids_list = [i for i in review_ids.split()] # Convert JS value into list of numbers
                [Bookings.objects.filter(id=id).update(finalized='Discarded', 
                            notes=Bookings.objects.get(id=id).notes + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            "," + \
                            " Discarded,", comms=request.POST.get('comms') + \
                            "\n" + \
                            "<" + \
                            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                            ">" + \
                            "\n") for id in review_ids_list]
                messages.success(request, 'Lesson(s) discarded.')
                return HttpResponseRedirect(reverse('admin_finalize:admin_finalize'))
    
    def get(self, request):
        """
        Limit access to superuser
        """
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().get(request)
