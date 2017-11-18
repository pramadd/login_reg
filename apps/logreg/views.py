from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
# from .models import *
import bcrypt



def index(request):
    return render(request,'logreg/index.html')

def register(request):

    first_name = request.POST['first_name']
    last_name =  request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    errors = User.objects.validatereg(request.POST)


    #errors
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    else:
        
         #hashing pswd
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = hashed_password )
        
        request.session['id'] = user.id
        #session
        

        return redirect('/success')


    #date of birth 
    minyear = 1900
    maxyear = datetime.date.today().year
    print datetime.date.today().year
    mydate = '12/12/2000'
    dateparts = mydate.split('/')
    try:
        if len(date) != 10:
           flash("Invalid date format")
        if int(date[2]) > maxyear or int(date[2]) < minyear:
           flash("Year out of range")
        dateobj = datetime.date(int(date[2]),int(date[1]),int(date[0]))
    except:
       return errors


def login(request):

    email = request.POST['email']
    password = request.POST['password']

    errors = User.objects.validatelogin(request.POST)
   
    #errors
    if len(errors):
        print "We have errors", errors
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    else:
        user = User.objects.get(email= request.POST['email'])

        request.session['id'] = user.id
        
        #session
       
     
        
        
        return redirect('/success')


def success(request):
    if 'id' not in request.session:
        return redirect('/')

    else:
        context={
            'user' : User.objects.get(id=request.session['id'])
        }
    

    
    # return render(request,'logreg/success.html',{"user" : User.objects.get(id=id)})
    return render(request,'logreg/success.html',context)





def logout(request):
    request.session.clear()
    return redirect('/')