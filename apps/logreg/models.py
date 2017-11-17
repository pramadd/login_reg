from __future__ import unicode_literals

from django.db import models

# Create your models here.
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')


class UserManager(models.Manager):

    def validatereg(self,postData):
        errors = {}
        if len(postData['first_name']) < 3 :
            errors['first_name'] = "first name must be atleast 3 characters"

        if len(postData['last_name']) < 3 :
            errors['last_name'] = "last name must be atleast 3 characters"

        if not EMAIL_REGEX.match(postData['email']):  
            errors['email'] = "Invalid email Address!"

        if len(postData['password']) < 8 :
            errors['password'] = "password must be atleast 8 characters"

        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = "passwords does not match"

        if len(postData['first_name']) < 1 or len(postData['last_name']) < 1  or len(postData['email']) < 1 or  len(postData['password']) < 1  or len(postData['confirm_password']) < 1 :
            errors['empty'] = "Fields cant be empty"

        return errors

        # x = {'first_name': first_name,'last_name': last_name, 'email': email, 'password': password, 'confirm_password': confirm_password}
        # errors = User.objects.validate(x)
        # if errors:
        #     for tag, error in errors.iteritems():
        #     messages.error(request, error, extra_tags=tag)
        #     return redirect('/')
        # else:
        #     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        #     user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = hashed_password )
        #     return redirect('/success')


    def validatelogin(self,postData):
        errors = {}
        hashed_password = postData['password'].encode()

        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 1 :
            errors['email'] = "Invalid email Address!"

        if len(postData['password']) < 8 :
            errors['password'] = "password must be atleast 8 characters"

        try:
            user = User.objects.get(email = postData['email'])    
            if (user):
                if bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                    print "succesfully logged in"
                else:
                    errors['password']= "password do not match"

        except:
            errors['email_not_exist'] = "email doesn't exist"

        return errors    




class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

