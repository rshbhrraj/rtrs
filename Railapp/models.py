from django.db import models
import random
import string
# Create your models here.

class user_database(models.Model):
	username		=	models.CharField(max_length=120,null=False)
	first_name		=	models.CharField(max_length=120,null=False)
	last_name		=	models.CharField(max_length=120,null=False)
	email_id		=	models.EmailField(primary_key=True,max_length=120,null=False)
	password		=	models.CharField(max_length=120,null=False)
	gender			=	models.CharField(max_length=120,null=False)
	martial_status	=	models.CharField(max_length=120,null=False)
	dob				=	models.CharField(max_length=120,null=False)
	mobile_no		=	models.CharField(max_length=120,null=False)
	sec_question	=	models.CharField(max_length=120,null=False)
	sec_ans			=	models.CharField(max_length=120,null=False)
	created			=	models.DateTimeField(auto_now_add=True)
	updated			=	models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.email_id)



class train_database(models.Model):
	train_number	=	models.CharField(max_length=120,null=False,primary_key=True)
	train_name		=	models.CharField(max_length=120,null=False)
	origination		=	models.CharField(max_length=120,null=True)
	destination		=	models.CharField(max_length=120,null=True)
	updated			=	models.DateTimeField(auto_now=True)
	

	def __str__(self):
		return str(self.train_number+" "+self.train_name)

class station(models.Model):
	station_id		= 	models.CharField(max_length=120,primary_key=True,null=False)
	station_name	=	models.CharField(max_length=120,null=False)
	station_city	=	models.CharField(max_length=120,null=False)
	
	def __str__(self):
		return str(self.station_name)

class train_details(models.Model):
	train_sno			=	models.AutoField(max_length=120,primary_key=True,null=False)
	train_number		=	models.ForeignKey(train_database,on_delete=models.CASCADE)
	general_seats		=	models.CharField(max_length=120,null=True)
	ac_seats			=	models.CharField(max_length=120,null=True)
	general_fare		=	models.CharField(max_length=120,null=True)
	ac_fare				=	models.CharField(max_length=120,null=True)
	qouta_ladies		=	models.CharField(max_length=120,null=False)
	qouta_general		=	models.CharField(max_length=120,null=False)
	availability_days	=	models.CharField(max_length=120,null=True)
	arrival_time		=	models.TimeField(default='20:00',blank=False)
	departure_time		=	models.TimeField(default='23:00',blank=False)
	station_id			=	models.ForeignKey(station,on_delete=models.CASCADE)

	def __str__(self):
		return str(str(self.train_number)+" "+str(self.station_id))

class ticket(models.Model):
	
	def gen_pnr_no():
		return str(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))).upper()

	pnr_no				=	models.CharField(unique=True,default=gen_pnr_no,max_length=10,editable=False,primary_key=True)
	ticket_id			=	models.ForeignKey(user_database,on_delete=models.CASCADE,null=True)
	boarding_station	=	models.CharField(max_length=120,null=True)
	destination			=	models.CharField(max_length=120,null=True)
	fare				=	models.CharField(max_length=120,null=True)
	coach				=	models.CharField(max_length=120,null=True)
	doj 				=	models.CharField(max_length=120,null=True)
	# doj 				=	

	def __str__(self):
		return str(self.pnr_no)

class seat_status(models.Model):
	booked_seat_number	=	models.CharField(max_length=120,primary_key=True,null=False)
	train_number		=	models.ForeignKey(train_details,on_delete=models.CASCADE)
	passenger_name		=	models.CharField(max_length=120,null=True)
	passenger_age		=	models.CharField(max_length=120,null=True)
	passenger_sex		=	models.CharField(max_length=120,null=True)
	ticket_number		=	models.ForeignKey(ticket,on_delete=models.CASCADE)

	def __str__(self):
		return str(str(self.ticket_number))

class train_week_schedule(models.Model):
	train_number		=	models.OneToOneField(train_database,max_length=120,null=False,on_delete=models.CASCADE,primary_key=True)
	monday				=	models.BooleanField(default=True)
	tuesday				=	models.BooleanField(default=True)
	wednesday			=	models.BooleanField(default=True)
	thursday			=	models.BooleanField(default=True)
	friday				=	models.BooleanField(default=True)
	saturday			=	models.BooleanField(default=True)
	sunday				=	models.BooleanField(default=True)
	def __str__(self):
		return str(self.train_number)