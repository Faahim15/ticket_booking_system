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

# Create your views here.
class TrainCreateView(CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/train_list.html'
    success_url = reverse_lazy('home')   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'ADD A NEW TRAIN INFORMATION'  # Make sure to add a comma at the end
        return context
   

class TrainListView(ListView):
    model = Train
    template_name = 'trains/admin_dashboard.html' 
    context_object_name = 'trains'

class TrainUpdateView(UpdateView):
    model = Train
    template_name = 'trains/train_list.html'  
    fields = '__all__'
    success_url = reverse_lazy('home')   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'EDIT TRAIN INFORMATION'  # Make sure to add a comma at the end
        return context 

class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'trains/train_confirm_delete.html'
    success_url = reverse_lazy('home')
    context_object_name = 'train' 


def ticket_booking(request):
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            from_location = form.cleaned_data['From'] 
            to = form.cleaned_data['to']
            date = form.cleaned_data['date']
            tickets = form.cleaned_data['tickets'] 

            try:
                train_obj = Train.objects.get(origin=from_location, destination=to) 
                acc = AccountModel.objects.get(user_acc = request.user) 
                total_price = tickets * train_obj.ticket_price
                if total_price <= acc.balance:
                    acc.balance -= total_price
                    if train_obj.available_seats >= tickets:
                        train_obj.available_seats -= tickets 
                        train_obj.save() 
                        acc.save() # Save the updated Train object
                        TicketBooking.objects.create( 
                            user = request.user,
                            From=from_location,
                            to=to,
                            date=date,
                            tickets=tickets
                        )
                        messages.success(request, f"Success! You have successfully purchased {tickets} tickets from {from_location} to {to}. Your booking is confirmed for {date}. Thank you for choosing our ticket booking service. Have a safe and pleasant journey!")

                        return redirect('home')  # Redirect to a success page
                    else:
                        messages.error(request, f'Not enough available seats on the train.') 
                else: 
                     messages.error(request, f"You don't have sufficient balance to buy tickets.") 

            except Train.DoesNotExist:
                messages.error(request, f'Enter valid location')

    else:
        form = TicketBookingForm()

    return render(request, 'base.html', {'form': form}) 

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


        
    
        
    

    




