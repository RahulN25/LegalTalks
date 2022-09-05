from django.shortcuts import render, redirect
from .models import ValidEnrollNo, Account
from django import forms
from .forms import (
    EnrollTestForm,
    AdvocateCreationForm,
    UserRegistrationForm,
    ProfileCreationForm,
    CommonUserProfileCreationForm,
    AdvProfileUpdateForm,
    ProfileUpdateForm,
    AccountDetailsUpdateForm,
)
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from PIL import Image
import os
from django.conf import settings
from django.core.files.storage import default_storage
from pathlib import Path

def mail_code(recipient_list=[]):
    import random
    v_code = random.randint(124000, 999999)
    subject = 'Email Verification for your LegalTalks account'
    message = f'The Code to verify your account is {v_code}\n\nIf this wasn\'t you, you can simply ignore this email'
    email_from = settings.EMAIL_HOST_USER
    recipient = recipient_list
    send_mail(
        subject,
        message,
        email_from,
        recipient,
        fail_silently=False,
    )
    return v_code

def advocate_signup(request):
    form = EnrollTestForm()
    if request.method == 'POST':
        form = EnrollTestForm(request.POST)
        if form.is_valid():
            sanitized_form = form.cleaned_data

            # Enrollment Number obtained from the new user
            input_enrollmtno = sanitized_form.get('enrollmtno')
            try:
                # ValidEnrollNo object obtained using the enrollment no. obtained from user
                test_enrollmtno = ValidEnrollNo.objects.get(enrollment_no = input_enrollmtno)

                # If the enrollment number is not used
                if not test_enrollmtno.used :
                    # Sending the email . This function returns the newly generated code
                    v_code = mail_code([test_enrollmtno.advocate_email,])

                    # Setting the session variables
                    request.session['v_code'] = v_code
                    request.session['enrollment_no'] = test_enrollmtno.enrollment_no
                    request.session['validity'] = True
                    request.session['mail'] = [test_enrollmtno.advocate_email,]
                    
                    return redirect('account:code-verification')

                # If an account with the specified enrollment number already exists
                messages.error(request, 'An account with the specified Enrollment number already exists .')
                return render(request, 'account/enterEnrollmentNumber.html', {'form': form})

            # If the enrollment number itself is not valid
            except ValidEnrollNo.DoesNotExist:
                messages.error(request, 'The Enrollment Number you provided is not valid')
                return render(request, 'account/enterEnrollmentNumber.html', {'form': form})

        return render(request, 'account/enterEnrollmentNumber.html', {'form': form})
    return render(request, 'account/enterEnrollmentNumber.html', {'form': form})

def code_verification(request):
    # The Enrollment number was valid
    try:
        # 'validity' indicates whether the attempt to verify code can be made
        if request.session['validity']:
            # When the blank form is submitted, the following code will decide where to go
            if request.method == 'POST':
                if int(request.session['v_code']) == int(request.POST.get('verification_code')):
                    request.session.pop('validity',None)
                    request.session.pop('v_code',None)
                    request.session.pop('mail',None)
                    request.session.modified = True
                    request.session['form_validity'] = True
                    return redirect('account:verification-success')
                messages.error(request, 'The entered Code didn\'t match\nPlease Try Again')
                return render(request, 'account/emailVerification.html', {})
            # Necessary for the blank form to show up after redirection
            return render(request, 'account/emailVerification.html', {})
    except KeyError:
        return redirect('account:advocate-signup')

def verification_success(request):
    try:
        if request.session['form_validity']:
            form = AdvocateCreationForm(initial={'email': ValidEnrollNo.objects.get(enrollment_no=request.session['enrollment_no']).advocate_email})
            form.custom_focus()
            if request.method == 'POST':
                form = AdvocateCreationForm(request.POST)
                form.custom_focus()
                if form.is_valid():
                    user_id = form.save(request.session['enrollment_no'])
                    request.session['can_create_profile'] = True
                    request.session['user_variable'] = user_id.username
                    request.session.pop('enrollment_no', None)
                    request.session.modified = True
                    return redirect('account:profile-creation')

                return render(request, 'account/lawyerSignUp.html', {'form': form})
            return render(request, 'account/lawyerSignUp.html', {'form': form})
    except KeyError:
        return redirect('account:advocate-signup')

def resend_code(request):
    try:
        if request.session['validity']:
            request.session['v_code'] = mail_code(request.session['mail'])
            messages.info(request, "A new code has been resent!")
            return redirect('account:code-verification')
    except KeyError:
        return redirect('account:advocate-signup')

def user_signup(request):
    user_reg_form = UserRegistrationForm()
    user_reg_form.custom_focus()
    if request.method == 'POST':
        user_reg_form = UserRegistrationForm(request.POST)
        user_reg_form.custom_focus()
        if user_reg_form.is_valid():
            user_id = user_reg_form.save()
            request.session['can_create_profile'] = True
            request.session['user_variable'] = user_id.username
            return redirect('account:profile-creation')
        return render(request, 'account/userSignUp.html', {'form': user_reg_form})
    return render(request, 'account/userSignUp.html', {'form': user_reg_form})

def profile_signup(request):
    try:
        if request.session['can_create_profile']:
            new_user = Account.objects.get(username=request.session['user_variable'])
            if new_user.is_advocate:
                profile_form = ProfileCreationForm()
            else:
                profile_form = CommonUserProfileCreationForm()
            if request.method == 'POST':
                # , instance=Account.objects.get(username=request.session['user_variable'])
                if new_user.is_advocate:
                    profile_form = ProfileCreationForm(request.POST, request.FILES)
                else:
                    profile_form = CommonUserProfileCreationForm(request.POST, request.FILES)
                if profile_form.is_valid():
                    if not isinstance(request.FILES.get('profile_image'), type(None)):
                        print('test')
                        print(type(request.FILES.get('profile_image')))
                        print(type(request.POST.get('profile_image')))
                        print('test-end')
                        profile_form.save(str(request.session['user_variable']))
                    else:
                        profile_form.save(str(request.session['user_variable']), use_custom=False)
                    request.session.pop('can_create_profile', None)
                    # new_user = Account.objects.get(username=request.session['user_variable'])
                    request.session.pop('user_variable', None)
                    request.session.modified = True
                    login(request, new_user)
                    return redirect('home')
                return render(request, 'account/profileCreation.html', {'form': profile_form, 'new_user': new_user})
            return render(request, 'account/profileCreation.html', {'form': profile_form, 'new_user': new_user})
    except KeyError:
        return redirect('account:user-signup')

@login_required
def my_profile(request):
    return render(request, 'account/myProfile.html', {})

@login_required
def edit_profile(request):
    if request.user.is_advocate:
        is_default = request.user.userprofile.profile_image.name == 'default_user.jpg'
    else:
        is_default = request.user.commonuserprofile.profile_image.name == 'default_user.jpg'
    details_form = AccountDetailsUpdateForm(instance=request.user)
    if request.user.is_advocate:
        profile_form = AdvProfileUpdateForm(instance=request.user.userprofile)
    else:
        profile_form = ProfileUpdateForm(instance=request.user.commonuserprofile)
    context = {
        'details_form': details_form,
        'profile_form': profile_form,
        'is_default': is_default,
    }
    if request.method == 'POST':
        details_form = AccountDetailsUpdateForm(request.POST, instance=request.user)
        if details_form.is_valid():
            details_form.save()
            """
            Referencing the user details(Profile details included) using following variable
            gives expected result, as opposed to using request.user.foo.bar . 
            """
            user = Account.objects.get(username=request.user.username)
            if request.user.is_advocate:
                profile = user.userprofile
                profile_form = AdvProfileUpdateForm(request.POST, request.FILES ,instance=request.user.userprofile)
            else:
                profile = user.commonuserprofile
                profile_form = ProfileUpdateForm(request.POST, request.FILES ,instance=request.user.commonuserprofile)
            if profile_form.is_valid():
                # Is the user using the default profile picture?
                if profile.profile_image.name == 'default_user.jpg':
                    # The User has not provided any picture
                    custom_image = request.FILES.get('custom_image')
                    if isinstance(custom_image, type(None)):
                        profile_form.save()
                    # The User has provided a picture (through HTML5 filefield)
                    else:
                        custom_image_name = custom_image.name
                        if os.path.isfile(Path(settings.MEDIA_ROOT, '/profile_pictures/', custom_image_name)):
                            os.remove(Path(settings.MEDIA_ROOT, '/profile_pictures/', custom_image_name))
                        with default_storage.open(settings.MEDIA_ROOT + '/profile_pictures/' + custom_image_name, 'wb+') as destination:
                            for chunk in custom_image.chunks():
                                destination.write(chunk)
                        # profile_form.fields['profile_image'] = request.FILES.get('custom_image')
                        profile_form.save(use_custom=True, image_name=custom_image_name)
                # The User uses a custom profile picture
                else:
                    # The user chose to keep the default profile picture
                    if request.POST.get('keep_default', False): # Delete the existing image and set default
                        # If this doesn't work, set profile_image.name in form.save() to 'default_user.jpg'
                        profile_form.fields['profile_image'] = None 
                        profile_form.save(use_custom=False, delete_older=True, image_name='default_user.jpg')
                    # The user didn't provide a picture and the 'keep_default' was not checked
                    else:
                        profile_image = request.FILES.get('profile_image')
                        if ((profile_image is None) or (profile_image.name == '')) or (profile_image.name == profile.profile_image.name.replace('profile_pictures/', '')) : 
                            profile_form.save()
                        # The user provided a picture and the 'keep_default' was not checked
                        else:
                            # Store the new image
                            profile_form.save(use_custom=True, delete_older=True)
                    
                messages.success(request, 'Your Profile Details Have Been Updated!')
                return redirect('account:my-profile')
            context = {
                'details_form': details_form,
                'profile_form': profile_form,
                'is_default': is_default,
            }
            messages.error(request, 'Please Correct The Following Errors')
            return render(request, 'account/editProfile.html', context)
        context = {
            'details_form': details_form,
            'profile_form': profile_form,
            'is_default': is_default,
        }
        messages.error(request, 'Please Correct The Following Errors')
        return render(request, 'account/editProfile.html', context)
    return render(request, 'account/editProfile.html', context)

def view_profile(request, user_id, username):
    visited_user = Account.objects.get(pk=user_id)
    if request.user == visited_user:
        return redirect('account:my-profile')
    return render(request, 'account/viewProfile.html', {'visited_user': visited_user})