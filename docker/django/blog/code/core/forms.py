from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    """
    """
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=30,
        required=False,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        max_length=254,
        required=False,
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=50,
        required=False,
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=50,
        required=False,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'url', 'location']

    def full_clean(self):
        'strip whitespace automatically in all form fields'
        data = self.data.copy()
        for k, vs in self.data.items():
            data[k] = vs.strip()
        self.data = data
        super(ProfileForm, self).full_clean()

class ChangePasswordForm(forms.ModelForm):
    """
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        label="Old password",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        label="New password",
    )
    confirm_newpassword = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        label="Confirm new password"
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_newpassword']

    def clean(self):
        super(ChangePassword, self).clean()
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_newpassword = self.cleaned_data.get('confirm_ewpassword')
        uid = self.cleaned_data.get('id')
        user = User.objects.get(pk=uid)
        if not user.check_password(old_password):
            self._errors['password'] = self.error_class(['Old passwords don\'t match'])
        if new_password and new_password != confirm_newpassword:
            self._errors['password'] = self.error_class(['New passwords don\'t match'])
        return self.cleaned_data

