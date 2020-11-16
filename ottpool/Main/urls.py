from django.urls import path,re_path
# from django.core.signing import Signer
from .views import ViewAllOtts,Ottscreendetails,PoolInterest

app_name = 'Main'

urlpatterns=[
	path('ViewAllOtts/',ViewAllOtts,name='ViewAllOtts'),
	path('Ottscreendetails/<ottid>',Ottscreendetails,name='Ottscreendetails'),
	path('PoolInterest/<userid>/<ottid>/<screenid>',PoolInterest,name='PoolInterest'),
	]