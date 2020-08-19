from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth import login , logout , get_user_model
from ways.forms import SignupForm , LoginForm , BfaForm , OtpForm
from django.db import IntegrityError 
from django.core.exceptions import ObjectDoesNotExist
from ways.models import user_login_failed_callback
import bfa , pyotp , qrcode


# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    errors = []
    if request.user.is_authenticated:
        return redirect('home')
    form = SignupForm()
    if request.method =='POST':
        form = SignupForm(request.POST)
        seckey = pyotp.random_base32()
        totp = pyotp.TOTP(seckey)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            email = cd['email']
            img = qrcode.make(totp.provisioning_uri(username))
            a= 'ways/static/images/otp' + username
            print(a)
            b = '.'.join([a,'png'])
            img.save(b,'PNG')
            img.save('ways/static/images/otp.png','PNG')
        try:
            fp = bfa.fingerprint.get(request)
            User = get_user_model()
            User.objects.create(username = username , password = password , passwordbfa = fp , passwordotp = seckey , email = email)
            user = User.objects.get(username = username)
            login(request,user)
            return render(request,'new.html',{'username':username})
        except IntegrityError:
            errors.append('username already taken')
        except ConnectionError:
            errors.append('Cant Download or execute JS')
        except ValueError:
            errors.append('Fingerprint bad value')
    return render(request,'signup.html',{'errors':errors, 'form':form})




def log_in(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd['login_type'])
            L_type = cd['login_type']
            if L_type == 'bfa':
                #loginBFA(request)
                #return render(request,'loginbfa.html',{'form':BfaForm})
                return redirect('bfa')
            else :
                #loginOTP(request)
                return redirect('otp')
        else:
            errors.append('This Form is not valid')
            #return HttpResponse('Is not Valid')
    else :
        form = LoginForm()
    return render(request,'login.html',{'form':form,'errors':errors})        



def loginOTP(request):
    errors = []
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =='POST':
        form = OtpForm(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            username = cd['username']
            pass1 = cd['OneTimePass']
            try:
                user  = get_user_model()
                sec_key = user.objects.filter(username = username).values_list('passwordotp').get()
                otp = pyotp.TOTP(sec_key[0])
                print('pass1:   ',pass1,type(pass1))
                print('******** ', otp.now())
                b = int(otp.now())
                print(type(b))
                if b == int(pass1) :
                    User = user.objects.get(username = username , passwordotp = sec_key[0])
                    login(request,User)
                    print('you login')
                    return redirect('home')
                else :
                    errors.append('Password is not correct')
                    user_login_failed_callback(request,username)
            except IntegrityError:
                errors.append('One Time Password is wrong ')
            except ObjectDoesNotExist:
                errors.append('This User does not exist')
        #else:
        #    return HttpResponse('Form is not valid')
    else:
        form = OtpForm()
    return render(request,'loginotp.html',{'form':form , 'errors':errors})

def loginBFA(request):
    errors = []
    if request.user.is_authenticated:
        return redirect('home')
    form = BfaForm
    if request.method == 'POST':
        form = BfaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user1 = cd['username']
            pass1 = cd['password']
            user = get_user_model()
            try:
                fp = bfa.fingerprint.get(request)
                try:
                    user = get_user_model()
                    p = user.objects.filter(username = user1 , password = pass1).values_list('passwordbfa').get()
                    print('passsssssss',p)
                    print('******',fp)
                    User = user.objects.get(username = user1 , passwordbfa = fp)
                    login(request,User)
                    print('You Login')
                    return redirect('home')
                except ObjectDoesNotExist:
                    errors.append('This User Does not Exist ')
            except ConnectionError:
                errors.append('Cant Dowmload or exceute JS')
                user_login_failed_callback(request,user1)
            except ValueError:
                errors.append('Bad Fingerprint')
        #else:
            #return HttpResponse('The Form is not valid')
    else:
        form = BfaForm
    return render(request,'loginbfa.html',{'form':form , 'errors':errors })    


def back(request):
    return redirect('home')

def log_out(request):
    logout(request)
    return redirect('home')
