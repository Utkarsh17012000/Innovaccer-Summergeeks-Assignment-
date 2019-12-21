from django.shortcuts import render,redirect,get_object_or_404
from django import forms
from django.forms.models import model_to_dict
from django.contrib import auth
from django.core import mail
from .models import Account,User,Meeting
from .forms import AccountForm,MeetingForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from twilio.rest import Client
from .tasks import send_meeting_email
from datetime import datetime
import smtplib
from django.contrib.auth import hashers

def signup(request):
    account_form = AccountForm()

    if request.method=="POST":
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            if account_form.cleaned_data.get('account_type')!='visitor' and account_form.cleaned_data.get('account_type')!='host':
                return forms.ValidationError("Invalid Account Type!")
            else:
                if account_form.cleaned_data.get('password')!=account_form.cleaned_data.get('confirm_password'):
                    return forms.ValidationError("Password Mismatch!")
                else:
                    try:
                        user = User.objects.get(email=account_form.cleaned_data.get('email'))
                        return render(request,'accounts/signuppage.html',{'error':'Email already registered!'})
                    except User.DoesNotExist:
                        user = User.objects.create_user(email=account_form.cleaned_data.get('email'),password=account_form.cleaned_data.get('password'))

                        account_data = account_form.save(commit=False)
                        account_data.password = hashers.make_password(account_form.cleaned_data.get('password'))
                        account_data.save()

                        auth.login(request,user)

                        subject = "SignUp Successful!"
                        body = "Your credentials\nEmail: {}\nPassword: {}\nPhone: {}".format(account_form.cleaned_data.get('email'),
                                                                                            account_form.cleaned_data.get('password'),
                                                                                            account_form.cleaned_data.get('phone'))
                        frm = "utkarshtanwar0@gmail.com" 
                        to = ["utkarshtanwar0@hotmail.com"]

                        send_email(subject,body,frm,to)

                        login_email = Account.objects.get(email=account_form.cleaned_data.get('email'))
                        details = model_to_dict(login_email)
                        return HttpResponseRedirect(reverse('accounts:relogin',args=(details['id'],)))
                      
    context = {
        'form':account_form
    }
    
    return render(request,"accounts/signuppage.html",context)

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            login_email = Account.objects.get(email=request.POST['email'])
            details = model_to_dict(login_email)
            return HttpResponseRedirect(reverse('accounts:relogin',args=(details['id'],)))
        else:
            return render(request,"accounts/loginpage.html",{'error':'Username or password incorrect!'})

    return render(request,"accounts/loginpage.html")

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')

def delete_account(request,account_id):
    if request.method == "POST":
        deleting_details = get_object_or_404(Account,pk=account_id)
        User.objects.filter(email=deleting_details.email).delete()
        Account.objects.filter(id=account_id).delete()
    
    return redirect('home')

def meeting(request,visitor_id):
    visitor_data = Account.objects.get(id=visitor_id)
    visitor_details = model_to_dict(visitor_data)
    host_details = Account.objects.filter(account_type='host').values()

    initial_data={
        'visitor_name':visitor_details['name'],
        'visitor_phone':visitor_details['phone'],
        'timestamp':timezone.now()
    }

    meeting_form = MeetingForm(request.POST or None,initial=initial_data)

    if request.method=="POST":
        if meeting_form.is_valid():
            meeting_data = meeting_form.save(commit=False)
            meeting_data.visitor_name = visitor_details['name']
            meeting_data.visitor_phone = visitor_details['phone']
            meeting_data.timestamp = timezone.now()
            meeting_data.save()

        email_visitor_name = visitor_details['name']
        email_visitor_email = visitor_details['email']
        email_address = request.POST['address']
        email_check_in_time = request.POST['check_in_time']
        email_check_out_time = request.POST['check_out_time']
        
        subject = "Meeting Scheduled"
        body = "Visitor Name: {}\nVisitor Email: {}\nMeeting address: {}\nCheck-in-time: {}\nCheck-out-time: {}".format(
            email_visitor_name,email_visitor_email,email_address,email_check_in_time,email_check_out_time)

        frm_email = visitor_details['email'] 
        email_host_details = model_to_dict(Account.objects.filter(id=request.POST['host_id'])[0])
        to_email = email_host_details['email']

        frm_phn = visitor_details['phone']
        to_phn = str(email_host_details['phone'])

        #send email
        send_email(subject,body,frm_email,to_email)

        #send message
        send_sms(body,frm_phn,to_phn)

        #scheduling email and message after meeting
        time_in = request.POST['check_in_time']
        time_out = request.POST['check_out_time']
        time_in_hh,time_out_hh = (int(time_in[:2]))%12*60,(int(time_in[:2]))%12*60
        time_in_mm,time_out_mm = int(time_in[3:]),int(time_out[3:])
        send_diff = abs(time_out_hh-time_in_hh)+abs(time_out_mm-time_in_mm) 

        send_meeting_email.delay(subject,body,frm_email,to_email,send_diff)
        
        return HttpResponseRedirect(reverse('accounts:relogin',args=(visitor_details['id'],)))
    
    edited_host_data = []
    for dic in host_details:
        edited_host_data.append({'id':dic['id'],'name':dic['name']})

    context = {
        'form':meeting_form,
        'visitor_details':visitor_details,
        'host_details':edited_host_data
    }
    return render(request,'accounts/meetingpage.html',context)

def relogin(request,relogin_id):
    context = Account.objects.get(id=relogin_id)
    context = model_to_dict(context)
    user = auth.authenticate(email=context['email'],password=context['password'])
    auth.login(request,user)
    return render(request,'base2.html',context)


def send_email(subject,body,frm,to):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('***********************','********************') #(username,password)

    msg = "Subject: {}\n\n{}".format(subject,body)

    server.sendmail(
        frm,
        to,
        msg
    )
    server.close()

def send_sms(body,frm,to):
    account_sid = '**********************************'
    auth_token = '********************************'
    client = Client(account_sid,auth_token)

    message = client.messages \
        .create(
            body = body,
            from_= frm,
            to = to_phn
        )    

