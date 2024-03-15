from django import forms
from .models import Train 
from .models import TicketBooking,Review
from django.core.exceptions import ValidationError

class TrainForm(forms.ModelForm):

    class Meta:
        model = Train
        fields = '__all__'
        widgets = {
            
            'train_pic': forms.ClearableFileInput(attrs={'value': '{{ form.train_pic.value }}'})
        
        } 


class TicketBookingForm(forms.ModelForm):
    
    class Meta:
        model = TicketBooking
        fields = ['From', 'to', 'date', 'tickets','choose_class'] 
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date','placeholder':'Pick a date'}),
             'choose_class':forms.Select(attrs={'class':' bg-gray-500 text-white border border-green-500 rounded-md p-2 w-full','placeholder':'Choose class'})
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
    
