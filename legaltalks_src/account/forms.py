from django import forms
from django.core import exceptions
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Account,
    ValidEnrollNo,
    UserProfile,
    CommonUserProfile,
)
from PIL import Image
import os
from django.conf import settings
from pathlib import Path

class EnrollTestForm(forms.Form):
    enrollmtno = forms.CharField(max_length=9, required=True, label='')

    """ def clean_enrollmt(self, *args, **kwargs):
        enrollmtno = self.cleaned_data.get('enrollmtno')
        if not len(enrollmtno) == 9:
            raise exceptions.ValidationError('An Enrollment Number is 9 characters long')
        return enrollmtno """

class AdvocateCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = [
            "Your password must contain at least 8 characters.<br>",
            "Your password can't be a commonly used password.<br>",
            "Your password can't be entirely numeric.<br>",
        ]
    class Meta:
        model = Account
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )
    
    def custom_focus(self):
        self.fields['first_name'].widget.attrs.update(autofocus='autofocus')
        self.fields['email'].widget.attrs.update(autofocus='')
    
    def save(self, enrollment_no, commit=True):
        advocate = super().save(commit=False)
        advocate.is_advocate = True
        advocate.enrollment_no = enrollment_no

        # Setting the enrollment number as used
        used_enrollment_no = ValidEnrollNo.objects.get(enrollment_no = enrollment_no)
        used_enrollment_no.used = True
        used_enrollment_no.save()
        if commit:
            advocate.save()
        return advocate

class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = [
            "Your password must contain at least 8 characters.<br>",
            "Your password can't be a commonly used password.<br>",
            "Your password can't be entirely numeric.<br>",
        ]
    class Meta:
        model = Account
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )

    def custom_focus(self):
        self.fields['first_name'].widget.attrs.update(autofocus='autofocus')
        self.fields['email'].widget.attrs.update(autofocus='')

class ProfileCreationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = (
            'gender',
            'birth_date',
            'phone_number',
            'profile_image',
        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

    def save(self, user_name, use_custom=True, commit=True):
        usr_profile = super().save(commit=False)
        usr_profile.user = Account.objects.get(username=user_name)
        # Save the image as it is with the name provided.
        usr_profile.save()
        # If an image is not provided, default value will be used and following code will not be executed.
        if use_custom:
            # Get the path of the stored image
            initial_path = usr_profile.profile_image.path
            # Open and bring the image into context
            img = Image.open(initial_path)
            # Image Manipulation Code
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                # Save the image with the user provided random name and path, but with modified attributes
                img.save(initial_path)
            print(initial_path)
            """
            The following assignment is done in the table and NOT on the file system.
            That is, in the table, the value for the profile_image field is modified as below.
            But on the filesystem, we still have the image named with the name provided by the user.
            """
            # The following value will be used to construct a new path
            usr_profile.profile_image.name = f'profile_pictures/{user_name}.jpg'
            usr_profile.save() # Save this as the new name for the specific user's profile image.
            # Now we construct a new path using the above 'name' value
            new_path = Path(settings.MEDIA_ROOT, usr_profile.profile_image.name)
            img.close()
            # And then we rename the user's image pointed to by 'initial_path' to 'new_path'
            # for the changes to be reflected at the level of File System.
            os.rename(initial_path, new_path)
            # Now the string value in table for 'profile_image' field matches the specified
            # value on the File System.
            usr_profile.save()
        if commit:
            usr_profile.save()
        return usr_profile

class CommonUserProfileCreationForm(forms.ModelForm):
    class Meta:
        model = CommonUserProfile
        fields = (
            'gender',
            'birth_date',
            'profile_image'
        )
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

    def save(self, user_name, use_custom=True, commit=True):
        usr_profile = super().save(commit=False)
        usr_profile.user = Account.objects.get(username=user_name)
        usr_profile.save()
        if use_custom:
            initial_path = usr_profile.profile_image.path
            img = Image.open(initial_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(initial_path)
            print(initial_path)
            usr_profile.profile_image.name = f'profile_pictures/{user_name}.jpg'
            usr_profile.save() # Call everytime when the image attributes are modified
            new_path = Path(settings.MEDIA_ROOT, usr_profile.profile_image.name)
            img.close()
            os.rename(initial_path, new_path)
            usr_profile.save()
        if commit:
            usr_profile.save()
        return usr_profile

class AccountDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'username',
            'email',
        )
    """ Not useful method
    def save(self, use_default=False, commit=True):
        user = super().save()
        if use_default:
            if user.is_advocate:
                # user.userprofile.profile_image.delete()
                profile = user.userprofile
                setattr(profile, 'profile_image', None)
                user.userprofile.save()
            else:
                # user.commonuserprofile.profile_image.delete()
                profile = user.commonuserprofile
                setattr(profile, 'profile_image', None)
                user.commonuserprofile.save()
        return user
    """

class AdvProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'profile_image',
            'phone_number'
        )
    def save(self, use_custom=False, delete_older=False, image_name=None, commit=True):
        profile = super().save(commit=False)
        if image_name:
            if image_name == 'default_user.jpg':
                profile.profile_image.name = image_name
            else:
                profile.profile_image.name = f'profile_pictures/{image_name}'
        profile.save()
        if os.path.isfile(Path(settings.MEDIA_ROOT + f'/profile_pictures/{profile.user.username}.jpg')) and delete_older:
            os.remove(Path(settings.MEDIA_ROOT + f'/profile_pictures/{profile.user.username}.jpg'))
        if use_custom:
            initial_path = profile.profile_image.path
            img = Image.open(initial_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(initial_path)
            profile.profile_image.name = f'profile_pictures/{profile.user.username}.jpg'
            profile.save()
            new_path = Path(settings.MEDIA_ROOT, profile.profile_image.name)
            img.close()
            os.rename(initial_path, new_path)
            profile.save()
        if commit:
            profile.save()
        return profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CommonUserProfile
        fields = (
            'profile_image',
        )
    def save(self, use_custom=False, delete_older=False, image_name=None, commit=True):
        profile = super().save(commit=False)
        if image_name:
            if image_name == 'default_user.jpg':
                profile.profile_image.name = image_name
            else:
                profile.profile_image.name = f'profile_pictures/{image_name}'
        profile.save()
        if os.path.isfile(Path(settings.MEDIA_ROOT + f'/profile_pictures/{profile.user.username}.jpg')) and delete_older:
            os.remove(Path(settings.MEDIA_ROOT + f'/profile_pictures/{profile.user.username}.jpg'))
        if use_custom:
            initial_path = profile.profile_image.path
            img = Image.open(initial_path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(initial_path)
            profile.profile_image.name = f'profile_pictures/{profile.user.username}.jpg'
            profile.save()
            new_path = Path(settings.MEDIA_ROOT, profile.profile_image.name)
            img.close()
            os.rename(initial_path, new_path)
            profile.save()
        if commit:
            profile.save()
        return profile