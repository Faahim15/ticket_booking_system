from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator 
# Create your models here.
class PassengersAccount(models.Model): 
    user = models.OneToOneField(User,on_delete = models.CASCADE,related_name = 'account')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200) 
    profile_pic = models.ImageField(upload_to='passengers/media/uploads/')  
    nid_no = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999),
            RegexValidator(r'^[0-9]{10}$', message='Must be a 10-digit number.')
        ]
    ) 
    gender = models.CharField(max_length = 100, default = '')
    address = models.CharField(max_length = 400, default = '')
    def __str__(self):
        return str(self.first_name)
class AccountModel (models.Model): 
    user_acc = models.OneToOneField(User,  on_delete=models.CASCADE,related_name='deposit')
    balance = models.DecimalField(max_digits=12, decimal_places=2,null=True)  

    def __str__(self):
        return f'{self.user_acc.username} deposited {self.balance} Tk.'