from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views import generic
from .models import Bookings
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


class BookingsView(generic.ListView):
    """
    Render bookings page
    """
    model = Bookings
    template_name = "bookings.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(BookingsView, self).get_context_data(*args,**kwargs)
        context['upcoming_lessons'] = Bookings.objects.filter(status=True, student=self.request.user)
        return context

    def post(self, request):
        """
        Create new booking
        """
        if request.method == 'POST':
            lesson = request.POST.get('lesson_inp')
            lesson_type = request.POST.get('lesson_type_inp')
            date = request.POST.get('date_inp')
            time = request.POST.get('time_inp')
            status = True
            student = request.user
            notes = 'book_' + lesson_type[0:3] + ", " + \
                    datetime.strptime(date, "%Y-%m-%d").strftime("%d %B %Y") + \
                    ", " + \
                    datetime.strptime(time, "%H:%M").strftime("%I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                    ","
            booking = Bookings(
                lesson=lesson,
                lesson_type=lesson_type,
                date=date,
                time=time,
                status=status,
                student=student,
                notes=notes)
            dates_list = str(list(Bookings.objects.filter(date=date).values_list('date', 'time').all()))
            convert_date = str(datetime.strptime(date, "%Y-%m-%d").strftime("%Y, %m, %#d"))
            convert_time = str(datetime.strptime(time, "%H:%M").strftime("%H, %#M"))
            if convert_date and convert_time not in dates_list:
                booking.save()
                messages.success(request, 'Booking successfully added.')
                return HttpResponseRedirect(reverse('manage_bookings'))
            else:
                messages.error(request, 'Sorry, selected date/time no longer available.')
                return HttpResponseRedirect(reverse('manage_bookings'))

    def get(self, request):
        """
        Authenticated users only
        """
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().get(request)


class ManageBookingsView(generic.ListView):
    """
    Render manage bookings page
    """

    model = Bookings
    template_name = "manage_bookings.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ManageBookingsView, self).get_context_data(*args,**kwargs)
        context['upcoming_lessons'] = Bookings.objects.filter(status=True, student=self.request.user)
        return context

    def get(self, request):
        """
        Authenticated users only
        """
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().get(request)


def edit_booking_date(request, booking_id):
    """
    Edit booking date and time
    """
    if not request.user.is_authenticated:
        raise PermissionDenied

    booking = get_object_or_404(Bookings, id=booking_id, student=request.user, status=True)
    if request.method == 'POST':
        booking.date = request.POST.get('edit_date_inp')
        booking.time = request.POST.get('edit_time_inp')
        dates_list = str(list(Bookings.objects.filter(date=booking.date).values_list('date', 'time').all()))
        convert_date = str(datetime.strptime(booking.date, "%Y-%m-%d").strftime("%Y, %m, %#d"))
        convert_time = str(datetime.strptime(booking.time, "%H:%M").strftime("%H, %#M"))
        if convert_date and convert_time not in dates_list:
            booking.confirmed = 'Pending'
            booking.flagged = False
            booking.notes = booking.notes + \
                timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                ", " + \
                datetime.strptime(booking.date, "%Y-%m-%d").strftime("%d %B %Y") + " " + \
                datetime.strptime(booking.time, "%H:%M").strftime("%I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
                ","
            booking.save()
            messages.success(request, 'Date/time successfully changed.')
            return redirect('manage_bookings')
        else:
            messages.error(request, 'Sorry, selected date/time no longer available.')
            return redirect('manage_bookings')
    context = {
        'edit_date_lesson': Bookings.get_lesson(booking),
        'edit_date_lesson_type': Bookings.get_lesson_type(booking),
        'date_and_time': Bookings.objects.filter(status=True).all()
        }
    return render(request, 'edit_booking_date.html', context)


def edit_booking_type(request, booking_id):
    """
    Edit lesson type
    """
    if not request.user.is_authenticated:
        raise PermissionDenied

    booking = get_object_or_404(Bookings, id=booking_id, student=request.user, status=True)
    if request.method == 'POST':
        booking.lesson_type = request.POST.get('edit_lesson_type')
        booking.notes = booking.notes + \
            timezone.now().strftime("%d %B %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m.") + \
            ", " + \
            booking.lesson_type + ","
        booking.save()
        messages.success(request, 'Lesson type successfully changed.')
        return redirect('manage_bookings')
    context = {
        'edit_date_lesson_type': Bookings.get_lesson_type(booking)
        }
    return render(request, 'edit_booking_type.html', context)


def cancel_booking(request, booking_id):
    """
    Cancel booking
    """
    if not request.user.is_authenticated:
        raise PermissionDenied

    booking = get_object_or_404(Bookings, id=booking_id, student=request.user, status=True)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Lesson successfully canceled.')
        return redirect('manage_bookings')
    context = {
        'cancel_lesson': Bookings.get_lesson(booking),
        'cancel_lesson_type': Bookings.get_lesson_type(booking),
        'cancel_date': Bookings.get_date(booking),
        'cancel_time': Bookings.get_time(booking)
        }
    return render(request, 'cancel_booking.html', context)


class PastBookingsView(generic.ListView):
    """
    Render past bookings page
    """

    model = Bookings
    paginate_by = 14
    template_name = "past_bookings.html"

    def get_queryset(self):
        return Bookings.objects.filter(status=False, student=self.request.user)
    
    def get(self, request):
        """
        Authenticated users only
        """
        if not request.user.is_authenticated:
            raise PermissionDenied
        return super().get(request)
