from django.contrib import admin

# Register your models here.
from .models import *

class page_admin_user_database(admin.ModelAdmin):
	list_display	=	('first_name','last_name','email_id','password','mobile_no','created','updated')
	list_per_page	=25

admin.site.register(user_database,page_admin_user_database)
class page_admin_train_database(admin.ModelAdmin):
	list_display	=	('train_number','train_name','origination','destination','updated')
	list_per_page	=	25

admin.site.register(train_database,page_admin_train_database)

admin.site.register(station)
admin.site.register(train_details)
admin.site.register(ticket)
admin.site.register(seat_status)
admin.site.register(train_week_schedule)
