from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Ott_titles,Ott_screens,pooled_members
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import EmailVerification

# Create your views here.
# @login_required
def ViewAllOtts(request):
	Allott_objects = Ott_titles.objects.all()
	context = {
		'Allott_objects' : Allott_objects,
	}
	return render(request,'Main/ViewAllotts.html',context=context)

# @login_required
def Ottscreendetails(request,ottid):
	try:
		poolbutton = pooled_members.objects.filter(
			userdetails=request.user,
			platform_details=ottid)
	except ObjectDoesNotExist:
		poolbutton = 0

	#Pool Count
	try:		
		pooledmembers_obj = pooled_members.objects.filter(platform_details=ottid)
	except ObjectDoesNotExist:
		pooledmembers_obj = 0

	try:
		screenobj = Ott_screens.objects.filter(ott_title=ottid)
	except ObjectDoesNotExist:
		screenobj = 0

	try:
		Otttitle = Ott_titles.objects.get(id=ottid)
	except ObjectDoesNotExist:
		Otttitle = 0

	context={
		'screenobj' : screenobj,
		'pooledmembers_obj' : pooledmembers_obj,
		'poolbutton' : poolbutton,
		'Otttitle' : Otttitle,
	}
	return render(request,'Main/Ottscreendetails.html',context=context)

@login_required
def PoolInterest(request,userid,ottid,screenid):
	try:
		emailcheck = EmailVerification.objects.get(user=userid,verified_status=True)
	except ObjectDoesNotExist:
		emailcheck = None

	if emailcheck != None:
		mainplatform = Ott_titles.objects.get(id=ottid)
		screen_obj = Ott_screens.objects.get(id=screenid)
		pooling = pooled_members(userdetails=request.user,platform_details=mainplatform,screen_Details=screen_obj,entry_on=timezone.now())
		pooling.save()

		context = {
				'Posted_user' : request.user,
				'mainplatform' : mainplatform,
				'screen_obj' : screen_obj,
			}
		html_content = render_to_string('Main/Email.html',context=context)
		email = EmailMessage("Greetings From OTT Pool", html_content, "naveens431@gmail.com", [request.user.email])
		email.content_subtype = "html"
		res = email.send()
		return redirect('Main:Ottscreendetails',ottid=ottid)
	else:
		messages.warning(request,f'Your Email is not verified.Kindly verify to proceed further !')
		return redirect('users:ProfileView',userid=userid)