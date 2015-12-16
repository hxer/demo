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
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=50,
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
        for k, vs in self.data.lists():
            new_vs = [v.strip() for v in vs]
            data.setlist(k, new_vs)
        self.data = data
        super(ProfileForm, self).full_clean()
