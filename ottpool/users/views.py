from django.shortcuts import render,redirect
from .forms import (NewRegistrationForm,
	ProfileUpdateForm,
	UserUpdateForm,)
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import Profile,EmailVerification
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import random,math

# Create your views here.
def Registration(request):
	form=NewRegistrationForm()
	if request.method == 'POST':
		form = NewRegistrationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			email_context = User.objects.filter(email__icontains=email)
			if email_context.exists():
				messages.warning(request,f'Email Already taken')
				return redirect('users:Registration')
			else:
				form.save()
				send_mail('Greetings from Ott Pool',f'Hai {username} ! Thanks For enrolling to Ott pool app','naveens431@gmail.com',[email])
				return redirect('users:Login')
	return render(request,'users/Registration.html',{'form':form})

def ProfileView(request,userid):
	try:
		emailverify = EmailVerification.objects.get(user=userid,verified_status=True)
	except ObjectDoesNotExist:
		emailverify = 0
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,
                                   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('users:ProfileView',userid=userid)
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		context={
		'u_form' : u_form,
		'p_form' : p_form,
		'emailverify' : emailverify,
		}
	return render(request,'users/ProfileView.html',context=context)

def UserEmailVerification(request):
	if request.method=='POST':
		emailcode  = request.POST.get('emailcode')
		verifyemailcode = EmailVerification.objects.get(user=request.user)
		if str(emailcode) == str(verifyemailcode.Email_code):
			verifyemailcode.verified_status=True
			verifyemailcode.verified_on=timezone.now()
			verifyemailcode.save()
			send_mail('Greetings from OTT Pool',f'Hai {request.user.username} ! your email has been verified sucessfully !','naveens431@gmail.com',[request.user.email])
			messages.success(request,f'email has been verified !')
			return redirect('users:ProfileView',userid=request.user.id)
		else:
			messages.success(request,f'Enter correct code !')
			return redirect('users:UserEmailVerification')
	else:
		try:
			pointone = EmailVerification.objects.get(user=request.user)
		except ObjectDoesNotExist:
			pointone = None

		if pointone != None:
			code = pointone.Email_code
			send_mail('Greetings from OTT Pool',f'Hai {request.user.username} ! your email verification code {code}','naveens431@gmail.com',[request.user.email])
		else:
			code = generateOTP()
			emailmodel,created = EmailVerification.objects.get_or_create(
			user=request.user,
			Email_code=code,
			verified_status=False,
			verified_on=timezone.now()
			)
			send_mail('Greetings from OTT Pool',f'Hai {request.user.username} ! your email verification code {code}','naveens431@gmail.com',[request.user.email])
		return render(request,'users/UserEmailVerification.html')

def generateOTP(): 
    digits = "0123456789"
    OTP = "" 
  
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
    return OTP 