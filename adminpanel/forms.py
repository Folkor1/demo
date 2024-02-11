from django import forms
from django.contrib.auth.models import User
from booking.models import Bookings


class UsersCheckboxForm(forms.ModelForm):
    """
    Single checkbox
    """
    selected = forms.BooleanField(required=False, label=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input check'}))

    class Meta:
        model = User
        fields = []


class FinalizeDiscardForm(forms.ModelForm):
    """
    Comms form
    """
    comms = forms.CharField(required=False, 
                            label=False, 
                            widget=forms.Textarea(attrs={'class': 'finalize-form rounded-1 border border-secondary-subtle small',
                                                         'placeholder': 'Write notes...'}))

    class Meta:
        model = Bookings
        fields = ['comms']


class NotesForm(forms.ModelForm):
    """
    Notes form
    """
    comms = forms.CharField(required=False, 
                            label=False, 
                            widget=forms.Textarea(attrs={'class': 'notes-form rounded-1 border border-secondary-subtle small text-center',
                                                         'placeholder': 'Write notes...',
                                                         'spellcheck': 'false'}))

    class Meta:
        model = Bookings
        fields = ['comms']
