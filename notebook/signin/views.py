from django.shortcuts import render,redirect
from django.http import HttpResponse
from signin.models import User
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.






def signin(request):
    if request.method=='GET':
        return render(request,'signin.html')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        print('email===',email,password)
        object=User.user_object(email)
        if object:
            if check_password(password,object.password):
                request.session['user']=email
                # request.session.pop('last_activity',None)
                # request.session.save()
                return redirect('home')
            error=error='Wrong email or password entered..'
            return render(request,'signin.html',{'error':error})
        else:
            error='Wrong email or password entered...............'
            return render(request,'signin.html',{'error':error})



def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')
    if request.method=='POST':
        email=request.POST.get('email')
        password=make_password(request.POST.get('password'))
        check=User.check_user_exist(email)

        if check:
            error='User already registered...please Login'
            return render(request,'signup.html',{'error':error})
            
        else:
            user=User(email=email,password=password)
            user.save()
            return redirect('signin')



def logout(request):
    if request.method=='GET':
        request.session.pop('user',None)
        
        # request.session.save()
        return redirect('signup')