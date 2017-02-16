import urllib
import urllib2
import json

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms import ValidationError

from models import Comment, Item


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        staff_status = True

    # fff

    def __init__(self, *args, **kwargs):
        # make the request object available to the form object
        self.request = kwargs.pop('request', None)
        super(MyRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(MyRegistrationForm, self).clean()
        # test the google recaptcha
        url = "https://www.google.com/recaptcha/api/siteverify"
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': self.request.POST.get(u'g-recaptcha-response', None),
            'remoteip': self.request.META.get("REMOTE_ADDR", None),
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())

        # result["success"] will be True on a success
        if not result["success"]:
            raise forms.ValidationError(_(u'Only humans are allowed to submit this form.'))
        return self.cleaned_data

    # gggg
    def clean_password(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('Password too short')
        return password

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        commit = self.clean_password()
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title', 'image', 'content',)
