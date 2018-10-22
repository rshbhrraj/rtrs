from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from .models import *
from django.core.validators import validate_email
from captcha.fields import CaptchaField



class User_details_form(forms.Form):
	first_name		=	forms.CharField(required=True)
	last_name		=	forms.CharField(required=True)
	email_id		=	forms.EmailField(required=True)
	password		=	forms.CharField(required=True)
	cpsd			=	forms.CharField(required=True)
	gender			=	forms.CharField(required=True)
	martial_status	=	forms.CharField(required=True)
	dob				=	forms.CharField(required=True)
	mobile_no		=	forms.CharField(required=True)
	sec_question	=	forms.CharField(required=True)
	sec_ans			=	forms.CharField(required=True)

	def clean(self):
		validate_email(self.cleaned_data.get('email_id'))
		if (self.cleaned_data.get('password')!=self.cleaned_data.get('cpsd')):
			raise ValidationError("passwords do not match.")
		obj=user_database.objects.filter(email_id=self.cleaned_data.get('email_id'))
		if (obj is not None):
			raise ValidationError("Email already exists.")
		return self.cleaned_data

class login_credentials_form(forms.Form):
	username		= 	forms.CharField(required=True)
	password 		=	forms.CharField(required=True)
	captcha 		= 	CaptchaField(required=True)

	

class train_search_form(forms.Form):
	boarding_station		=	forms.CharField(required=True)
	destination_station		=	forms.CharField(required=True)
	quota					=	forms.CharField(required=True)
	doj						=	forms.DateField(required=True)

	def clean(self):
		if(self.cleaned_data.get('boarding_station')==self.cleaned_data.get('destination_station')):
			print("SOURCE == Destination")
			raise ValidationError("Source and Destination can't be same.")
		if(self.cleaned_data.get('doj') is None):
			print("date not coming")
			raise ValidationError("date error.")
		return self.cleaned_data



class find_train_schedule_form(forms.Form):
	type_of_search	=	forms.CharField(required=True)
	source			=	forms.CharField(required=False)
	source2			=	forms.CharField(required=False)
	destination 	=	forms.CharField(required=False)

	def clean(self):
		if((self.cleaned_data.get('source') is None and self.cleaned_data.get('source2') is None)):
			raise ValidationError("Source or Train Number should be provided.")	
			
		if(self.cleaned_data.get('destination') is not None):
			if((self.cleaned_data.get('source')==self.cleaned_data.get('destination')) and(self.cleaned_data.get('source')!="")):
				raise ValidationError("Source and Destination can't be same.")

		return self.cleaned_data
	
class passenger_details_form(forms.Form):
	train_number		=	forms.CharField(required=True)
	from_station		=	forms.CharField(required=True)
	to_station			=	forms.CharField(required=True)
	doj 				=	forms.CharField(required=True)
	coach 				=	forms.CharField(required=True)
	passenger_1_name	=	forms.CharField(required=True)
	passenger_1_age		=	forms.CharField(required=True)
	passenger_1_sex		=	forms.CharField(required=True)

	passenger_2_name	=	forms.CharField(required=False)
	passenger_2_age		=	forms.CharField(required=False)
	passenger_2_sex		=	forms.CharField(required=False)
	passenger_3_name	=	forms.CharField(required=False)
	passenger_3_age		=	forms.CharField(required=False)
	passenger_3_sex		=	forms.CharField(required=False)
	passenger_4_name	=	forms.CharField(required=False)
	passenger_4_age		=	forms.CharField(required=False)
	passenger_4_sex		=	forms.CharField(required=False)
	passenger_5_name	=	forms.CharField(required=False)
	passenger_5_age		=	forms.CharField(required=False)
	passenger_5_sex		=	forms.CharField(required=False)

	def clean(self):
		if(self.cleaned_data.get('doj') is None):
			raise ValidationError("doj anhi aaya")
		if(self.cleaned_data.get('coach') is None):
			raise ValidationError("coach anhi aaya")

class password_validation_form(forms.Form):
	password 			=	forms.CharField(required=True)
	entered_password	=	forms.CharField(required=True)

	def clean(self):
		if(self.cleaned_data.get('password')!=self.cleaned_data.get('entered_password')):
			print("Wrong password entered")
			raise ValidationError("Wrong Password entered. Password Not Updated!!")
		return self.cleaned_data

class password_change_form(forms.Form):
	
	original_password		=	forms.CharField(required=True)
	new_password 			=	forms.CharField(required=True)
	confirm_new_password	=	forms.CharField(required=True)

	def clean(self):
		if(self.cleaned_data.get('new_password')!=self.cleaned_data.get('confirm_new_password')):
			print("password could not be changed as new_passwords are not same.")
			raise ValidationError("Invalid passwords. Password Not Updated!!")
		return self.cleaned_data

class profile_change_form(forms.Form):

	last_name		=	forms.CharField(required=True)
	gender			=	forms.CharField(required=True)
	martial_status	=	forms.CharField(required=True)
	dob				=	forms.CharField(required=True)
	mobile_no		=	forms.CharField(required=True)
	sec_ans			=	forms.CharField(required=True)

