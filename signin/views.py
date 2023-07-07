from django.shortcuts import render,redirect
from django.http import HttpResponse
from signin.models import User
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
import random


from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

otp=0


def signin(request):
    if request.method=='GET':
        return render(request,'signin.html')
    else:
        email=request.POST.get('email')
        password=request.POST.get('password')
        print('email===',email,password)
        object=User.user_object(email)
        print(object)
        if object:
            if check_password(password,object.password):
                request.session['user']=email
                request.session.save()
                # request.session.pop('last_activity',None)
                # del request.session['last_activity']
                # request.session.save()
                print('jjjjjjjjjjjjjjjjjjj')
                print(request.session.get('user'))
                return redirect('home')
            error=error='Wrong email or password entered..'
            return render(request,'signin.html',{'error':error})
        else:
            error='Wrong email or password entered...............'
            print('kkkkkkkkkk')
            return render(request,'signin.html',{'error':error})


import smtplib

from django.core.exceptions import ValidationError
# from dns import resolver

# def check_email_exists(email):
#     # Split the email address to extract the domain
#     # domain = email.split('@')[1]

#     try:
#         resolver.resolve(email, 'MX')
#         print('here im//////////////////////////////////////')
#         return True
#     # except resolver.NXDOMAIN:
#     #     raise ValidationError('The domain of the email address does not exist.')
       
#     # except resolver.NoAnswer:
#     #     raise ValidationError('The domain of the email address does not have MX records.')
#     except:  
#         print('uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
#         return False



# from  validate_email import validate_Email
# from validate_email_address import validate_email

# import re










def signup(request):
    otp= random.randint(1000, 9999)
    request.session['otp']=otp
    if request.method=='GET':
        # global otp
        return render(request,'signup.html')
    if request.method=='POST':
        email=request.POST.get('email')


        subject='Email verification'
        from_email='rajashekarganiger2002@gmail.com'
        to = email
        html_content = render_to_string('mail_template.html',{'otp':otp})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        
        
        try:
            # x=resolver.resolve(email, 'MX')
            # validate_Email()
            msg.send()
            success="OTP sent successfully"
            request.session['email']=email
            return render(request,'verification.html',{'success':success})

        except:
            error = "Invalid email"
            return render(request,'signup.html',{'error':error})

    
        # password=make_password(request.POST.get('password'))
        # check=User.check_user_exist(email)

        # if check:
        #     error='User already registered...please Login'
        #     return render(request,'signup.html',{'error':error})
            
        # else:
        #     user=User(email=email,password=password)
        #     user.save()
        #     return redirect('signin')



def logout(request):
    if request.method=='GET':
        request.session.pop('user',None)
        
        # request.session.save()
        return redirect('signup')
    



def verifyotp(request):
    if request.method=='POST':
        verifyotp=request.POST.get('otpi')
        otp=request.session.get('otp')
        print(type(verifyotp),type(otp))
        if int(verifyotp)==otp:
            return redirect('altsignup')
        else:
            print(verifyotp,otp)
            print(otp)
            error="Wrong OTP entered"
            return render(request,'verification.html',{'error':error})
    else:
        return render(request,'verification.html')

def altsignup(request):
    if request.method=='POST':
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password==cpassword:
            email=request.session.get('email')
            # user=User(email=email,password=password)
            # user.save()
            check=User.check_user_exist(email)

            if check:
                error='User already registered...please Login'
                return render(request,'signin.html',{'error':error})
            
            else:
                password=make_password(request.POST.get('password'))
                user=User(email=email,password=password)
                user.save()
                return redirect('signin')
        else:
            error="Password do not match"
            return render(request,'altsignup.html',{'error':error})
    else:
        return render(request,'altsignup.html')
            
