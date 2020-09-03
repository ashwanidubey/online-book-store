from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import datetime




def userlogin(request):
    return render(request,'bookstore/login.html')


def login(request):
    if request.method=='POST':
        print(1)
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username , password=password)
        if user :
            print(2)
            auth.login(request,user)
            request.session['username']=username
            books=models.Book.objects.all()
            return render(request,'bookstore/home.html',{'info':"you are now logged in",'books':books})
        print(3)
        return  render(request,'bookstore/login.html',{"info":"either password of username is incorrect"})
    print(4)
    return render(request,'bookstore/login.html')
def Logout(request):
    logout(request)
    return  render(request,'bookstore/login.html',{'logoutwarn':"you are now logged out"})
#@login_required(login_url="/bookstore/login/")
def home(request):
    books=models.Book.objects.all()
    return render(request,'bookstore/home.html',{'books':books})
def signup(request):
    return render(request,'bookstore/signup.html')
def signuped(request):
    print("hello")
    if request.method=='GET':
        return render(request,'bookstore/signup.html')
    else :
        print("sabash")
        first_name=request.POST['FN']
        last_name=request.POST['LN']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request,'bookstore/signup.html',{'usernameexist':"this username already exist"})
        elif  User.objects.filter(email=email).exists():
                 return render(request,'bookstore/signup.html',{'emailexist':"this emai id already exist"})
        else :
           user=User.objects.create_user(username=username,password=password ,email=email ,first_name=first_name,last_name=last_name)
           user.save()
           user1=auth.authenticate(username=username , password=password)
           auth.login(request,user1)
           request.session['username']=username
           books=models.Book.objects.all()
           return render(request,'bookstore/home.html',{'created':"congratulatios! your account is now created",'books':books})
#@login_required(login_url="/bookstore/login/")
def search(request):
    if request.method=='POST':
         books1=models.Book.objects.filter(book_name=request.POST['search'])
         books2=models.Book.objects.filter(book_author=request.POST['search'])
         data={'books1':books1,'books2':books2}
         if books1 :
             for x in books1 :
                  if x.book_status=="AVAILABLE":
                      data['order']='done'
         if books2 :
                  for x in books2 :
                       if x.book_status=="AVAILABLE":
                            data['order']='done'
         if not(books1 or books2 ):
             data={'empty':"no data found ,plese try with other name or see the name from the home page"}
    return render(request,'bookstore/search.html',data)
@login_required(login_url="/bookstore/login/")
def booknow(request):
    if request.method=='GET':
        return render(request,'bookstore/home.html')

    b=models.Book.objects.filter(book_name=request.POST['book_name'])
    b1=b[0]

    b1.book_copy-=1
    if b1.book_copy<1:
        b1.book_status="NOT AVAILABLE"
    b1.save()

    tra=models.Transaction()
    u=User.objects.filter(username=request.user.username)
    tra.user=u[0]
    tra.book=b1
    tra.T_date=datetime.datetime.now()
    tra.save()
    return render(request,'bookstore/booknow.html',{'t1':tra})
@login_required(login_url="/bookstore/login/")
def history(request):
    data={}
    u=User.objects.filter(username=request.user.username)
    t=models.Transaction.objects.filter(user=u[0])
    if t :

        for x in t :
            x.T_idd="TRAN"+'0'*(10-len(str(x.T_id)))+str(x.T_id)
            x.save()
        data['t']=t
        return render(request,'bookstore/history.html',data)
    else :
        data['info']="you have no transaction history"
        return render(request,'bookstore/history.html',{'HISTORYLESS':'done'})
@login_required(login_url="/bookstore/login/")
def payment(request):
    data={'book_name':request.GET['name']}
    return render(request,'bookstore/payment.html',data)
@login_required(login_url="/bookstore/login/")
def Return(request):
    if request.method=='GET' :
        #print(request.GET['T_id'],"hiiiiiiiiii")
        t1=models.Transaction.objects.filter(T_id=request.GET['T_id'])
        t1=t1[0]
        t1.R_status="Returned"
        t1.R_date=datetime.datetime.now()
        t1.save()

        b=models.Book.objects.filter(book_name=t1.book)
        b1=b[0]
        b1.book_copy+=1
        b1.book_status="AVAILABLE"
        b1.save()
        u=User.objects.filter(username=request.user.username)
        t=models.Transaction.objects.filter(user=u[0])
        #print("hiiiiii")
        #data={'t':t}
        return render(request,'bookstore/history.html',{'RETURN':"done"})
    else :
        return render(request,'bookstore/home.html')
def forgot(request):
    print(0)
    if request.method=='GET':
        print(1)
        return render(request,'bookstore/forgot.html')
    else :
        print(2)
        UN=request.POST['UN']
        FN=request.POST['FN']
        LN=request.POST['LN']
        user=User.objects.get(username=UN)

        if user and user.first_name==FN and user.last_name==LN   and request.POST['NP1']==request.POST['NP2']:
            #user.password=request.POST['NP1']
            #user.last_name="Las"
            user.set_password(request.POST['NP1'])
            user.save()
            print("hii",user.username,user.password,user.email,user.first_name,user.last_name,"hii")
            user=auth.authenticate(username=user.username , password=user.password)

            return render(request,'bookstore/login.html',{'UPDATE':'your password is updated'})

        else :
            print(4)
            return render(request,'bookstore/forgot.html',{'NOTUPDATE':'something is wrong'})

def help(request):
    if request.method=='GET':

            return render(request,'bookstore/help.html')
    else :
        return render(request,'bookstore/help.html',{'Post':"done"})
