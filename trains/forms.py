from django import forms
from .models import Train 
from .models import TicketBooking,Review
from django.core.exceptions import ValidationError

class TrainForm(forms.ModelForm):

    class Meta:
        model = Train
        fields = '__all__'
        widgets = {
            'arrival_time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
            'train_number': forms.TextInput(attrs={'placeholder': 'Enter Train Number'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter Train Name'}),
            'origin': forms.TextInput(attrs={'placeholder': 'Enter Origin'}),
            'destination': forms.TextInput(attrs={'placeholder': 'Enter Destination'}),
            'total_seats': forms.NumberInput(attrs={'placeholder': 'Enter Total Seats'}),
            'available_seats': forms.NumberInput(attrs={'placeholder': 'Enter Available Seats'}),
        } 


class TicketBookingForm(forms.ModelForm):

    class Meta:
        model = TicketBooking
        fields = ['From', 'to', 'date', 'tickets'] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        } 
    
    def clean_tickets(self):
        tickets = self.cleaned_data.get('tickets')

        if tickets is not None:
            if tickets < 1 or tickets > 3:
                raise ValidationError("You can only buy between 1 and 3 tickets.")

        return tickets 

class ClientReview(forms.ModelForm):
    class Meta:
        model = Review 
        fields = ['content','rating']
    
