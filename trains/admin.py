from django.contrib import admin
from . models import Train,Station,TicketBooking,Review
# Register your models here. 
admin.site.register(Train) 

class StationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('station_name',)}
    list_display = ['station_name', 'slug']
    
admin.site.register(Station, StationAdmin) 

admin.site.register(TicketBooking)
admin.site.register(Review)
