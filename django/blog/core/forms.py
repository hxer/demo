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
