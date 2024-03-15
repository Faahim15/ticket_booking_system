from django.http import HttpResponse
from django.contrib.auth.views import LoginView 
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail   
from decimal import Decimal 
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm,RegistrationEditForm,DepositForm
from django.views.generic.edit import CreateView 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes 
# for sending email 
from django.http import Http404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect ,render
from django.contrib.auth import logout 
from django.views.generic.detail import DetailView
from .models import PassengersAccount,AccountModel 
from django.contrib.auth.decorators import login_required

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'passengers/signup.html'
    success_url = reverse_lazy('login') 

    def form_valid(self, form): 
        response = super().form_valid(form) 
        user = form.save(commit=False) 
        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk)) 

        # Build the confirmation link
        confirm_link = f"http://127.0.0.1:8000/passengers/active/{uid}/{token}" 

        # Compose email
        email_subject = "Confirm Your Email"
        email_body = render_to_string('passengers/confirmation_email.html', {'confirm_link': confirm_link})
        # Send email
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.info(self.request, "Check your email for confirmation.") 
        return response 
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been confirmed. You can now login.')
        return redirect('login')
    else:
        messages.success(request, 'Your email has been confirmed. You can now login.')
        return redirect('login')
        


class UserLoginView(LoginView):
    template_name = 'passengers/login.html'
    
    def get_success_url(self):
        return reverse_lazy('profile') 
    

@login_required
def UserDetails(request):
    user = request.user
    return render(request, 'passengers/passengers_account_detail.html',{'user':user}) 
@login_required
def edit_profile(request):
    profile = PassengersAccount.objects.get(user = request.user)

    if request.method == 'POST':
        form = RegistrationEditForm(request.POST,request.FILES, instance = profile) 
        if form.is_valid():
            form.save() 
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile') 
    else:
        form = RegistrationEditForm(instance=profile)  
    return render(request,'passengers/signup.html',{'form':form}) 
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to reflect the new password
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Change 'profile' to the URL you want to redirect to after password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'passengers/change_password.html', {'form': form})        

@login_required
def Deposit_money(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = DepositForm(request.POST) 
            if form.is_valid(): 
                deposit = form.cleaned_data['amount'] 
                amount = Decimal(deposit) 
                if amount < 100 and amount < 50000:
                    messages.success(request, 'Transaction Alert: Insufficient funds. Please ensure your deposit exceeds 100Tk for successful processing and does not exceed 50,000Tk.') 
                else:
                    user_model_instance, created = AccountModel.objects.get_or_create(user_acc=request.user) 
                    if user_model_instance.balance is not None:
                        user_model_instance.balance += amount 
                    else: 
                        user_model_instance.balance = amount 
                    user_model_instance.save()
                    messages.success(request, f'You have successfully deposited {amount}Tk.') 
                    return redirect('home')
    else:
        form = DepositForm() 
    return render(request, 'passengers/deposit_money.html',{'form':form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('home')