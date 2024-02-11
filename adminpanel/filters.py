import django_filters
from django.contrib.auth.models import User
from django_filters.widgets import BooleanWidget
from django import forms
from booking.models import Bookings
from django.forms import TextInput
from datetime import datetime


class CustomBooleanWidget(BooleanWidget):
    """
    Override option values
    """
    def __init__(self, attrs=None, choices=()):
        choices = (('', 'All users'), ('true', 'Approved'), ('false', 'Pending'))
        forms.Select.__init__(self, attrs, choices)


class UsersFilter(django_filters.FilterSet):
    """
    Class for users filter
    """
    active = django_filters.BooleanFilter(field_name='is_active', 
                                            label=False, 
                                            widget=CustomBooleanWidget(attrs={'onchange': 'this.form.submit()', 
                                                                                'class': 'border border-dark-subtle fw-bold admin-filters'}))

    class Meta:
        model = User
        fields = ['active']


STATUS_CHOICES = (
    ('', 'All statuses'),
    ('Confirmed', 'Confirmed'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
)


ONLINE_OFFLINE_CHOICES = (
    ('', 'All types'),
    ('Online', 'Online'),
    ('Offline', 'Offline'),
)


FINALIZED_CHOICES = (
    ('', 'All statuses'),
    ('Finalized', 'Finalized'),
    ('Discarded', 'Discarded'),
)


class BookingsFilter(django_filters.FilterSet):
    """
    Class for bookings status filter
    """
    confirmed = django_filters.ChoiceFilter(choices=STATUS_CHOICES,
                                                empty_label=None,
                                                label=False, 
                                                widget=forms.Select(attrs={'onchange': 'this.form.submit()', 
                                                                        'class': 'border border-dark-subtle fw-bold admin-filters'}))
    
    lesson_type = django_filters.ChoiceFilter(choices=ONLINE_OFFLINE_CHOICES,
                                                empty_label=None,
                                                label=False, 
                                                widget=forms.Select(attrs={'onchange': 'this.form.submit()', 
                                                                            'class': 'border border-dark-subtle fw-bold admin-filters'}))
    
    date = django_filters.DateFilter(widget=forms.DateInput(attrs={'onchange': 'this.form.submit()',
                                                                   'autocomplete': 'off',
                                                                   'type': 'text',
                                                                   'placeholder': 'Select date',
                                                                   'class': 'border border-dark-subtle text-center fw-bold admin-filters'}))

    class Meta:
        model = Bookings
        fields = ['confirmed', 'lesson_type', 'date']


class AdminArchiveFilter(django_filters.FilterSet):
    """
    Class for admin archive filter
    """ 
    student = django_filters.CharFilter(field_name='student__username',
                                        lookup_expr='iexact',
                                        label=False,
                                        max_length=25,
                                        widget=TextInput(attrs={'class': 'border border-dark-subtle fw-bold admin-filters text-center',
                                                                'autocomplete': 'off',
                                                                'type': 'text',
                                                                'placeholder': 'Enter username',
                                                                }))
    
    date = django_filters.DateFilter(widget=forms.DateInput(attrs={'class': 'border border-dark-subtle text-center fw-bold admin-filters',
                                                                    'autocomplete': 'off',
                                                                    'type': 'text',
                                                                    'id': 'datepicker_archive',
                                                                    'placeholder': 'Select date'}))
    
    finalized = django_filters.ChoiceFilter(choices=FINALIZED_CHOICES,
                                            empty_label=None,
                                            label=False,
                                            widget=forms.Select(attrs={'class': 'border border-dark-subtle fw-bold admin-filters',
                                                                       'id': 'confirmed_archive',
                                                                       }))

    class Meta:
        model = Bookings
        fields = ['student', 'date', 'finalized']

    def __init__(self, *args, **kwargs):
        super(AdminArchiveFilter, self).__init__(*args, **kwargs)
        if self.data == {} or self.data == {'student': [''], 'date': [''], 'finalized': ['']}:
            self.queryset = self.queryset.none()
        if 'page' not in self.data:
            conf = list(self.data.values())
            filter = [tup[0] for tup in FINALIZED_CHOICES]
            for param in self.data:
                if param not in self.filters:
                    self.queryset = self.queryset.none()
                else:
                    if conf[0]:
                        if not User.objects.filter(username__iexact=conf[0]).exists():
                            self.queryset = self.queryset.none()            
                    if conf[1]:
                        try:
                            str(conf[1]) != datetime.strptime(str(conf[1]), "%m/%d/%Y").strftime("%m/%d/%Y")
                        except ValueError:
                            self.queryset = self.queryset.none()
                    if conf[2] not in filter:
                        self.queryset = self.queryset.none()
        else:
            if not any(x in self.data for x in ['student', 'date', 'finalized']):
                self.queryset = self.queryset.none()


class FinalizeFilter(django_filters.FilterSet):
    """
    Class for bookings status filter
    """
    confirmed = django_filters.ChoiceFilter(choices=STATUS_CHOICES,
                                                empty_label=None,
                                                label=False, 
                                                widget=forms.Select(attrs={'onchange': 'this.form.submit()', 
                                                                        'class': 'border border-dark-subtle fw-bold admin-filters'}))
    
    lesson_type = django_filters.ChoiceFilter(choices=ONLINE_OFFLINE_CHOICES,
                                                empty_label=None,
                                                label=False, 
                                                widget=forms.Select(attrs={'onchange': 'this.form.submit()', 
                                                                            'class': 'border border-dark-subtle fw-bold admin-filters'}))
    
    date = django_filters.DateFilter(widget=forms.DateInput(attrs={'onchange': 'this.form.submit()',
                                                                    'autocomplete': 'off',
                                                                    'type': 'text',
                                                                    'placeholder': 'Select date',
                                                                    'id': 'datepicker_finalize',
                                                                    'class': 'border border-dark-subtle text-center fw-bold admin-filters'}))

    class Meta:
        model = Bookings
        fields = ['confirmed', 'lesson_type', 'date']
