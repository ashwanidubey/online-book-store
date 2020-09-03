from . import views
from django.conf.urls import url,include

urlpatterns=[
url('home/',views.home),
url('userlogin/',views.userlogin),
url('login/',views.login),
url('logout/',views.Logout),
url('signup/',views.signup),
url('search',views.search),
url('signuped',views.signuped),
url('booknow',views.booknow),
url('history',views.history),
url('payment',views.payment),
url('Return',views.Return),
url('forgot',views.forgot),
url('help',views.help),
]
