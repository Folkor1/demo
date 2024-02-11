from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
import threading, datetime, time
from booking.models import Bookings


stop_event = threading.Event()
threads_counter = 0
timer = 0
time_remaining = 0
time_remaining_sec = 0

stop_dupes = threading.Event()
threads_counter_dupes = 0
timer_dupes = 0
time_remaining_dupes = 0
time_remaining_dupes_sec = 0


def services(request):
    """
    Render services page
    """
    if not request.user.is_superuser:
        raise PermissionDenied
    
    time_remaining_sec = 300 - (time.time() - timer)
    time_remaining = datetime.timedelta(seconds = time_remaining_sec)
    time_remaining_dupes_sec = 600 - (time.time() - timer_dupes)
    time_remaining_dupes = datetime.timedelta(seconds = time_remaining_dupes_sec)
    event_thread = threading.Thread(target=expired)
    event_thread_dupes = threading.Thread(target=duplicates)
    
    if request.method == 'POST':
        if 'run_expiry' in request.POST:
            stop_event.clear()
            event_thread.start()
            return HttpResponseRedirect(request.path_info)
        if 'stop_expiry' in request.POST:
            stop_event.set()
            return HttpResponseRedirect(request.path_info)
        if 'run_dupes' in request.POST:
            stop_dupes.clear()
            event_thread_dupes.start()
            return HttpResponseRedirect(request.path_info)
        if 'stop_dupes' in request.POST:
            stop_dupes.set()
            return HttpResponseRedirect(request.path_info)
    context = {
        'threading': stop_event.is_set(),
        'counter': threads_counter,
        'time_remaining': str(time_remaining)[3:7],
        'time_remaining_sec': time_remaining_sec,
        'stop_dupes': stop_dupes.is_set(),
        'threads_counter_dupes': threads_counter_dupes,
        'time_remaining_dupes': str(time_remaining_dupes)[2:7],
        'time_remaining_dupes_sec': time_remaining_dupes_sec
    }
    
    return render(request, "services.html", context)


def expired():
    """
    Set past dates to false
    """
    global threads_counter
    global timer
    while not stop_event.is_set():
        threads_counter+= 1
        now = datetime.datetime.now()
        book = Bookings.objects.filter(status=True).all()
        for b in book:
            mytime = datetime.datetime.strptime(str(b.time), '%H:%M:%S').time()
            mydatetime = datetime.datetime.combine(b.date, mytime)
            if now > mydatetime:
                b.status = False
                b.save()
        timer = time.time()
        time.sleep(300)


def duplicates():
    """
    Search for duplicated date/time
    """
    date = []
    duplicates = []
    global timer_dupes
    global threads_counter_dupes
    while not stop_dupes.is_set():
        threads_counter_dupes+= 1
        book = Bookings.objects.filter(status=True).all()
        for b in book:
            d = b.date
            t = b.time
            date.append((str(d), str(t)))
        for i in date:
            if date.count(i) > 1 and i not in duplicates:
                duplicates.append(i)
        for y in duplicates:
            Bookings.objects.filter(date=y[0], time=y[1], status=True).update(flagged=True)
        timer_dupes = time.time()
        duplicates = []
        date = []
        time.sleep(600)
