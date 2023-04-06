from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat Password'),
                                widget=forms.PasswordInput)
    
    error_messages = {
        'password_mismatch': _('Password don\'t match!'),
    }
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email')
        
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     if self._meta.model.USERNAME_FIELD in self.fields:
    #         self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
    #             'autofocus'
    #         ] = True
        
    
    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd['password1']
        password2 = cd['password2']
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch']
            )
        return password2
    
    
    def clean_email(self):
        data = self.cleaned_data['email']
        user = get_user_model().objects.filter(email=data)\
                                        .exists()
        if user:
            raise forms.ValidationError(_('Email already in use!'))
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = get_user_model().objects\
                .filter(email=data)\
                .exclude(id=self.instance.id)
        if qs.exists():
            raise forms.ValidationError(_('Email already in use'))
        return data
        


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
  

# class UserPasswordChangeForm(PasswordChangeForm):
    
#     def __init__(self, *args, **kwargs):
#         super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        
#         for field in self.fields:
#             self.fields[field].widget \
#             .attrs.update({'class': 'form-control'})
    