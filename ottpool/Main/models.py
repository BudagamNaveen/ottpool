from django.db import models
from django.conf import settings

# Create your models here.
class Ott_titles(models.Model):
	platform_name = models.CharField(max_length=200)
	platform_image = models.ImageField(upload_to='ottimages/',default='websitepics/default.jpg')

	def __str__(self):
		return self.platform_name

class Ott_screens(models.Model):
	ott_title = models.ForeignKey('Ott_titles',on_delete=models.CASCADE,blank=True,null=True)
	screen_options = models.CharField(max_length=20)

	def __str__(self):
		return self.ott_title.platform_name

class pooled_members(models.Model):
	userdetails = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
	platform_details = models.ForeignKey('Ott_titles',on_delete=models.CASCADE,blank=True,null=True)
	screen_Details = models.ForeignKey('Ott_screens',on_delete=models.CASCADE,blank=True,null=True)
	entry_on = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return f'{self.screen_Details.screen_options} screen of {self.platform_details.platform_name} by {self.userdetails.username}'
