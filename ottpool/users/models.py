from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
	ProfilePic = models.ImageField(upload_to='profilepics/',default='profilepics/default.jpg')
	mobile = models.CharField(max_length=10,blank=True,null=True)

	def __str__(self):
		return self.user.username

class EmailVerification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
	Email_code = models.CharField(max_length=20)
	verified_status = models.BooleanField(default=False)
	verified_on = models.DateTimeField()

	def __str__(self):
		return f'{self.user.username} email is {self.verified_status}'
		
def create_profile(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(user=instance)

post_save.connect(create_profile,sender=User)

def update_profile(sender,instance,created,**kwargs):
	if created == False:
		instance.profile.save()

post_save.connect(update_profile,sender=User)

