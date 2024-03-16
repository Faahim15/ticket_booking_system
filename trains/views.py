from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Train,TicketBooking
from passengers.models import AccountModel
from .forms import TrainForm,TicketBookingForm,ClientReview
from django.views.generic import ListView
from django.views.generic.edit import UpdateView 
from django.views.generic import DeleteView  
from . models import TicketBooking 
from django.contrib import messages 
from . models import Train, Station,Review  
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test  
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
class SuperuserRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('home')  # Redirect non-superusers to the home page
        return super().dispatch(request, *args, **kwargs)
# Create your views here.

@staff_member_required
def train_create_view(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Train information added successfully!")
            return redirect('admin_dashboard')
        
    else:
        form = TrainForm()
    
    context = {
        'form': form,
        'type': 'ADD A NEW TRAIN INFORMATION'
    }
    
    return render(request, 'trains/train_list.html', context)
   

class TrainListView(SuperuserRequiredMixin,ListView):
    model = Train
    template_name = 'trains/admin_dashboard.html' 
    context_object_name = 'trains'

class TrainUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Train
    template_name = 'trains/train_edit.html'  
    fields = '__all__'
    success_url = reverse_lazy('home')   
    def get_initial(self):
        initial = super().get_initial()
        instance = self.object
        if instance:
            initial['train_pic'] = instance.train_pic
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'EDIT TRAIN INFORMATION'  
        return context 
    def form_valid(self, form):
        messages.success(self.request, "Train information updated successfully!")
        return super().form_valid(form)

class TrainDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Train
    template_name = 'trains/train_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')
    context_object_name = 'train' 
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Train information deleted successfully!")
        return super().delete(request, *args, **kwargs)


def ticket_booking(request):
    reviews = Review.objects.all()
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['From'] 
            to = form.cleaned_data['to']
            date = form.cleaned_data['date']
            tickets = form.cleaned_data['tickets'] 
            choose_class = form.cleaned_data['choose_class']
            acc = None
            try:
                train_obj = Train.objects.get(origin=from_location, destination=to) 
                total_price = tickets * train_obj.ticket_price 
                try:
                    acc = AccountModel.objects.get(user_acc = request.user) 
                

                      
                    if acc.total_buyed_tickets > 3: 
                        messages.error(request, "Oops! You've already purchased 3 tickets. To ensure fair access, we limit purchases to a maximum of 3 tickets per transaction. Thank you.")
                    
                    elif total_price <= acc.balance:
                        acc.balance -= total_price
                        if train_obj.available_seats >= tickets:
                            train_obj.available_seats -= tickets 
                            acc.total_buyed_tickets += tickets
                            train_obj.save() 
                            acc.save() 
                            TicketBooking.objects.create( 
                                user = request.user,
                                train = train_obj,
                                From=from_location,
                                to=to,
                                date=date,
                                tickets=tickets,
                                choose_class = choose_class
                            )
                            messages.success(request, f"Success! You have successfully purchased {tickets} tickets from {from_location} to {to} in {choose_class} class for {date}.Your booking is confirmed. We appreciate your trust in our ticket booking service. Wishing you a safe and pleasant journey!")

                            return redirect('home')  
                        else:
                            messages.error(request, f"There are not enough available seats on the train for {choose_class} class.")
                            return redirect('home')
                    else: 
                        messages.error(request, f"You don't have sufficient balance to buy tickets.") 
                except AccountModel.DoesNotExist:
                    messages.error(request, 'An account is required to proceed. Please make a deposit to create your account.')

            except Train.DoesNotExist:
                messages.error(request, f'Enter valid location')

    else:
        form = TicketBookingForm()

    return render(request, 'base.html', {'form': form, 'reviews':reviews}) 

class Home(ListView):
    model = Train
    template_name = 'trains/station_filter.html' 
    context_object_name = 'trains' 
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
         category = Station.objects.get(slug=category_slug)
         return Train.objects.filter(station_name=category) 
        else:
         return Train.objects.all() 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['station'] = Station.objects.all()
        return context
@login_required
def leave_review(request,id):
    train = get_object_or_404(Train, id=id)
    existing_review = Review.objects.filter(train=train, user_review=request.user).first() 
    buy_or_not = TicketBooking.objects.filter(train=train, user=request.user).exists() 
    if existing_review:
        messages.info(request, 'You have already reviewed this Train.')
        return redirect('profile')
    elif buy_or_not is False: 
        messages.warning(request, 'You need to buy a ticket to leave a review.')
        return redirect('home') 
    else:
        if request.method == 'POST':
            form = ClientReview(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                rating = form.cleaned_data['rating']
            
                Review.objects.create(train=train, user_review=request.user, content=content, rating=rating)
            
                messages.success(request, 'Thank you for your review!')
                return redirect('home')
        else:
            form = ClientReview() 
        return render(request, 'trains/leave_review.html', {'form': form})

        
    
        
    

    




