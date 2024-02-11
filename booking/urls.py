from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.BookingsView.as_view(), name="bookings"),
    path(
        'manage_bookings/',
        views.ManageBookingsView.as_view(),
        name='manage_bookings'
        ),
    path('edit/<booking_id>', views.edit_booking_date, name="edit"),
    path('edit_type/<booking_id>', views.edit_booking_type, name="edit_type"),
    path('cancel/<booking_id>', views.cancel_booking, name="cancel"),
    path(
        'past_bookings/',
        views.PastBookingsView.as_view(),
        name="past_bookings"
        ),
]