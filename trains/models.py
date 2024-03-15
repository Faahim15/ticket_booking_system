from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
# Create your models here.
SEAT_CHOICES = [
    ('AC_B','AC_B'),
    ('AC_S','AC_S'),
    ('SNIGDHA','SNIGDHA'),
    ('S_CHAIR','S_CHAIR'),
    ('SHULOV','SHULOV'),
    ('F_SEAT','F_SEAT'),
]
class Station(models.Model):
    station_name = models.CharField(max_length = 100,default = '') 
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True) 

    def __str__(self):
        return self.station_name  
    
class Train(models.Model): 
    station_name = models.ForeignKey(Station, related_name='origin_station', on_delete=models.CASCADE )
    train_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100 ,default = '')
    origin = models.CharField(max_length=100,default = '')
    destination = models.CharField(max_length=100,default = '')
    departure_time = models.TimeField()
    arrival_time = models.TimeField() 
    ticket_price = models.PositiveIntegerField()
    train_pic = models.ImageField(upload_to='passengers/media/uploads/',null = True, blank=True) 
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField() 
    

    def __str__(self):
        return f"{self.train_number} - {self.name}"

    class Meta:
        ordering = ['departure_time'] 



class TicketBooking(models.Model): 
    user = models.ForeignKey(User, on_delete = models.CASCADE,blank=True, null = True)
    train = models.ForeignKey(Train, on_delete = models.CASCADE,blank=True, null = True)
    From = models.CharField(max_length = 100) 
    to = models.CharField(max_length = 100) 
    date = models.DateField() 
    tickets = models.PositiveIntegerField() 
    choose_class = models.CharField(choices= SEAT_CHOICES,default = '')

    def __str__(self) -> str:
        return f'From {self.From} to {self.to}' 

class Review(models.Model):
    train = models.ForeignKey(Train,related_name ='review', on_delete = models.CASCADE) 
    user_review = models.ForeignKey(User,on_delete=models.CASCADE,related_name ='user_review')
    content = models.TextField()
    rating = models.PositiveIntegerField() 
    created_on =models.DateTimeField(default =timezone.now)
    
    def __str__(self):
        return f"Comments by {self.user_review.username}"

    


