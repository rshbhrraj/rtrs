from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from .forms import  *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404,render
from django.forms import ModelForm
from django.contrib import messages
from django.http import QueryDict
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
# Create your views here.


#HOME VIEW

def home(request):
	if 'username' in request.session:
		if request.session['username']=="invalid":
			del request.session['username']
	
	return render(request,'index.html',{})

#LOGIN VIEW

def login(request):
	if(request.method=="POST"):
		form 	=	login_credentials_form(request.POST)
		if(form.is_valid()):
			obj=form.cleaned_data	
			flag=0
			for p in user_database.objects.all():
				if((p.email_id==obj['username'] or p.username==obj['username'] )and p.password==obj['password']):
					flag=1
					request.session['username']=p.email_id
					request.session['firstname']=str(p.first_name).capitalize()
					return HttpResponseRedirect("/")
			if(flag==0):
				request.session['username']="invalid"
				messages.error(request,"Invalid Login Credentials")
				return render(request,'login.html',{'form':form})	
	else:
		form 	=	login_credentials_form()
	return render(request,'login.html',{'form':form})


#LOGOUT VIEW

def logout(request):
	del request.session['username']
	del request.session['firstname']
	return render(request,'index.html',{})


#SIGNUP VIEW

def signup(request):
	if(request.method=="POST"):
		form=User_details_form(request.POST)
		if(form.is_valid()):
			obj=form.cleaned_data
			obj3=user_database.objects.filter(email_id=obj['email_id'])
			if(obj3 is None):
				obj2=user_database.objects.create(
					first_name		=	obj['first_name'],
					last_name		=	obj['last_name'],
					email_id		=	obj['email_id'],
					password		=	obj['password'],
					gender			=	obj['gender'],
					martial_status	=	obj['martial_status'],
					dob				=	obj['dob'],
					mobile_no		=	obj['mobile_no'],
					sec_question	=	obj['sec_question'],
					sec_ans			=	obj['sec_ans'],
					)
				request.session['username']=obj['first_name']
				request.session['firstname']=p.first_name	
				return HttpResponseRedirect("/")
			else:
				messages.error("User Already Exists")
				return render(request,'signup.html',{})
	else:
		form=User_details_form()

	return render(request,"signup.html",{'form':form})


#TRAIN VIEW

def train(request):
	station_req 	=	station.objects.all()
	train_req		=	train_database.objects.all()
	if(request.method=="POST"):
		form 	=	find_train_schedule_form(request.POST)
		if(form.is_valid()):
			obj 	= 	form.cleaned_data
			data 	=	list()
			if(obj['type_of_search'] =="by_name"):
				obj1	=	train_details.objects.filter(station_id=obj['source'])
				flag=0
				if(obj1):
					for obj2 in obj1:
						train_no	=	str(obj2.train_number).split(' ')
						train_no 	=	train_no[0]
						obj3		=	train_details.objects.filter(train_number=train_no).filter(station_id=obj['destination'])
						if (obj3):
							flag=1
							for i in obj3:
								train_nono	=	str(i.train_number).split(' ')
								train_nom	=	train_nono[0]
								obj4 		=	train_database.objects.filter(train_number=train_nom)
								obj5		=	train_week_schedule.objects.filter(train_number=train_nom)
								q_dict		=	{

									'train_number':obj4[0].train_number,
									'train_name':obj4[0].train_name,
									'origination':obj4[0].origination,
									'destination':obj4[0].destination,
									'monday':'Y' if obj5[0].monday else 'N',
									'tuesday':'Y' if obj5[0].tuesday else 'N',
									'wednesday':'Y' if obj5[0].wednesday else 'N',
									'thursday':'Y' if obj5[0].thursday else 'N',
									'friday':'Y' if obj5[0].friday else 'N',
									'saturday':'Y' if obj5[0].saturday else 'N',
									'sunday':'Y' if obj5[0].sunday else 'N',
									}		
								dict_q			=	QueryDict('',mutable=True)
								dict_q.update(q_dict)							
								data.append(q_dict)
						elif(flag==1):
							continue
						else:
							st2="No Direct Train from "+str(obj['source']).upper()+" to "+str(obj['destination']).upper()+"."
							messages.error(request,st2)
							return render(request,'train.html',{'form':form,'station_req':station_req,'train_req':train_req})
				else:
					st2="No Direct Train from "+str(obj['source']).upper()+" to "+str(obj['destination']).upper()+"."
					messages.error(request,st2)
			else:
				if(obj['source2'] !=""):
					obj4	=	train_database.objects.filter(train_number=obj['source2'])
					obj5	=	train_week_schedule.objects.filter(train_number=obj['source2'])
					q_dict	={
						'train_number':obj4[0].train_number,
						'train_name':obj4[0].train_name,
						'origination':obj4[0].origination,
						'destination':obj4[0].destination,
						'monday':'Y' if obj5[0].monday else 'N',
						'tuesday':'Y' if obj5[0].tuesday else 'N',
						'wednesday':'Y' if obj5[0].wednesday else 'N',
						'thursday':'Y' if obj5[0].thursday else 'N',
						'friday':'Y' if obj5[0].friday else 'N',
						'saturday':'Y' if obj5[0].saturday else 'N',
						'sunday':'Y' if obj5[0].sunday else 'N',
						}		
					dict_q			=	QueryDict('',mutable=True)
					dict_q.update(q_dict)							
					data.append(q_dict)
					if(data):
						pass
					else:
						st2="No Direct Train from "+str(obj['source']).upper()+" to "+str(obj['destination']).upper()+"."
						messages.error(request,st2)
				else:
					st2="Train Number can't be blank."
					messages.error(request,st2)
			return render(request,'train.html',{'data':data,'retained_data':obj,'station_req':station_req,'train_req':train_req})
	else:
		form 	=	find_train_schedule_form()
	return render(request,'train.html',{'form':form,'station_req':station_req,'train_req':train_req})


#RESERVATION VIEW

def reservation(request):
	val 	=	check_session(request)
	if(val):
		station_req 	=	station.objects.all()
		case=0
		if(request.method=="POST"):	
			form 	=	train_search_form(request.POST)
			data 	=	list()
			if(form.is_valid()):
				obj 	= 	form.cleaned_data
				obob 	=	train_details.objects.all()
				obj1	=	train_details.objects.filter(station_id=obj['boarding_station'])
				flag=0	
				if(obj1 is not None):
					for obj2 in obj1:
						train_no	=	str(obj2.train_number).split(' ')
						train_no 	=	train_no[0]
						obj3		=	train_details.objects.filter(train_number=train_no).filter(station_id=str(obj['destination_station']).upper())
						if (obj3 is not None):
							for i in obj3:
								train_nono	=	str(i.train_number).split(' ')
								train_nom	=	train_nono[0]
								obj4 		=	train_database.objects.filter(train_number=train_nom)
								data.append(obj4)
						else:
							flag=1
					return render(request,'reservation.html',{'data':data,'retained_data':obj,'username':request.session['firstname']})	
				else:
					flag=1
				if(flag==1):
					messages.error("No such Station as quered.")		
			else:
				case=1
		else:
			case=1
		if(case==1):
			dt = datetime.datetime.now() + datetime.timedelta(hours=2160)
			dt = dt.strftime("%Y-%m-%d")
			form 	=	train_search_form()
		return render(request,'reservation.html',{'form':form,'station_req':station_req,'dt':dt})

	else:
		messages.error(request,'Please Login First.')
		return HttpResponseRedirect('/login/')



# RESERVATION FORM MAIN WHERE DETAILS ARE TO BE SUBMITTED

def reservation_details(request):
	if(request.method=="POST"):
		form 	=	passenger_details_form(request.POST)
		if(form.is_valid()):
			obj					=	form.cleaned_data
			user_database_obj	=	user_database.objects.get(email_id=request.session['username'])
			train_details_obj	=	train_details.objects.filter(train_number=obj['train_number']).filter(station_id=str(obj['from_station']))
			obj1				=	ticket.objects.create(
				ticket_id			=	user_database_obj,		# must be a database instance
				boarding_station	=	obj['from_station'],
				destination			=	obj['to_station'],
				fare				=	str(train_details_obj[0].general_fare),
				coach				=	obj['coach'],
				doj 				=	obj['doj']
				)
			pnr_no_object	=	ticket.objects.get(pnr_no=obj1.pnr_no)
			arr1=[i for i in range(0,10)]
			arr2=[i for i in range(1,65)]
			seat_number 		=	"S"+str(random.choice(arr1))+" "+str(random.choice(arr2))
			obj2			=		seat_status.objects.create(
				train_number		=	train_details_obj[0],
				passenger_name		=	obj['passenger_1_name'],
				passenger_age		=	obj['passenger_1_age'],
				passenger_sex		=	obj['passenger_1_sex'],
				ticket_number		=	pnr_no_object,
				booked_seat_number	=	seat_number,
				)
			return HttpResponseRedirect('/display')
		else:
			return render(request,'reser.html',{'form':form})	
	else:
		form 	=	passenger_details_form()
	return render(request,'reser.html',{'form':form})


#DISPLAY VIEW FOR TICKETS

def display(request):
	val 	=	check_session(request)
	if(val):
		data 		=	[]
		ticket_obj 	=	ticket.objects.filter(ticket_id=str(request.session['username']))
		flag=0
		if(len(ticket_obj)!=0):
			flag=1
			for i in ticket_obj:
				seat_obj			=	seat_status.objects.get(ticket_number=str(i.pnr_no))
				train_nono 			=	str(seat_obj.train_number).split(' ')
				train_nono			=	train_nono[0]
				q_dict	={
					'train_number':train_nono,
					'boarding_station':i.boarding_station,
					'destination':i.destination,
					'doj':i.doj,
					'coach':i.coach,
					'pnr_no':i.pnr_no
					}		
				dict_q			=	QueryDict('',mutable=True)
				dict_q.update(q_dict)							
				data.append(q_dict)
			return render(request,'display.html',{'data':data,'flag':flag})
		else:
			messages.error(request,'No Tickets Booked Yet.')
		return render(request,'display.html',{'data':data,'flag':flag})
	else:
		messages.error(request,'Please Login First.')
		return HttpResponseRedirect('/login/')
	return render(request,'display.html',{})


#PROFILE DETAILS VIEW

def profile(request):
	val 	=	check_session(request)
	if(val):
		if(request.method=="POST"):
			if('password_change' in request.POST):
				form	=	password_change_form(request.POST)	
				obj2	=	user_database.objects.filter(email_id=str(request.session['username']))
				password_validation	=	obj2[0].password
				if(form.is_valid()):
					obj 			=	form.cleaned_data
					q_dict			=	{'password':password_validation,'entered_password':obj['original_password'],
					'csrfmiddlewaretoken':request.POST['csrfmiddlewaretoken']}		
					dict_q			=	QueryDict('',mutable=True)
					dict_q.update(q_dict)
					form2			=	password_validation_form(dict_q)
					if(form2.is_valid()):
						obj3		=	form2.cleaned_data					
						if(obj2[0].password!=obj['original_password']):
							messages.error(request,"Wrong Password Entered")
						else:
							obj2.update(password=str(obj['new_password']))
							obj2[0].save()
							messages.success(request, 'Profile details updated.')
					return render(request,'profile.html',{'form':form2,'data':obj2[0]})	
				return render(request,'profile.html',{'form':form,'data':obj2[0]})
			elif('profile_change' in request.POST):
				form 	=	profile_change_form(request.POST)	
				if(form.is_valid()):
					obj 	=	form.cleaned_data
					obj2	=	user_database.objects.filter(email_id=request.session['username'])
					obj2.update(
						last_name=obj['last_name'],
						gender=obj['gender'],
						martial_status=obj['martial_status'],
						dob=obj['dob'],
						mobile_no=obj['mobile_no'],
						sec_ans=obj['sec_ans'])
					obj2[0].save()
					messages.success(request, 'Profile details updated.')
				return render(request,'profile.html',{'form':form,'data':obj2[0]})
		else:
			data		=	user_database.objects.get(first_name=str(request.session['firstname']).lower())
		return render(request,'profile.html',{'data':data})
	else:
		messages.error(request,'Please Login First.')
		return HttpResponseRedirect('/login/')


#VIEW FOR CHEECKING SESSIONS

def check_session(request):
	if 'username' in request.session:
		if(request.session['username']!="invalid" and request.session['username'] is not None):
			return True
	return False
	


#PAYMENT VIEW

def payment_module(request):
	paypal_dict = {
		"business": "receiver_email@example.com",
		"amount": "10000000.00",
		"item_name": "name of the item",
		"invoice": "unique-invoice-id",
		"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
		"return_url": request.build_absolute_uri(reverse('/display')),
		"cancel_return": request.build_absolute_uri(reverse('/reservation')),
		"custom": "premium_plan",  # Custom command to correlate to some function later (optional)
	}
	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form}
	return render(request, "payment.html", context)


def schedule(request):
	return render(request,'schedule.html',{})
