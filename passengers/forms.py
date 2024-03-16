from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  
from . models import PassengersAccount
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class UserRegistrationForm(UserCreationForm): 
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200) 
    profile_pic = forms.ImageField()  
    nid_no = forms.IntegerField(
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),
            RegexValidator(r'^[0-9]{10}$', message='Must be a 10-digit number.')
        ]
    ) 
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    address = forms.CharField(max_length = 400)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1','password2','profile_pic','nid_no','gender','address'] 

    def save(self, commit=True):
    # Get the user instance from the form
        our_user = super().save(commit=False)

        if commit:
            try:
                # Save the user instance
                our_user.save()

                # Get additional data from form.cleaned_data
                first_name = self.cleaned_data.get('first_name')
                last_name = self.cleaned_data.get('last_name')
                profile_pic = self.cleaned_data.get('profile_pic')
                nid_no = self.cleaned_data.get('nid_no')
                gender = self.cleaned_data.get('gender')
                address = self.cleaned_data.get('address')

                # Create PassengersAccount instance
                PassengersAccount.objects.create(
                    user=our_user,
                    first_name=first_name,
                    last_name=last_name,
                    profile_pic=profile_pic,
                    nid_no=nid_no,
                    gender=gender,
                    address=address
                )

                # Deactivate the user
                our_user.is_active = False
                our_user.save()

            except Exception as e:
                
                our_user.delete()
                raise e

        return our_user

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

class RegistrationEditForm(forms.ModelForm):
    class Meta:
        model = PassengersAccount 
        fields = ['first_name','last_name','profile_pic','nid_no','gender','address'] 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            }) 
class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)