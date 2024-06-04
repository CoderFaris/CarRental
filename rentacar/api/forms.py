from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import UserInfo, Renting, Cars, Rating

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'date_of_birth', 'car_model']
        widgets = {
            'date_of_birth' : forms.DateInput(attrs={'type' : 'date', 'placeholder' : 'DD-MM-YYYY'})
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'date_of_birth', 'car_model']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False

    def clean_date_of_birth(self):
        return self.instance.date_of_birth


class CarForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['id', 'car_model', 'cost']

class RentingForm(forms.ModelForm):
    class Meta:
        model = Renting
        fields = ['car_model', 'pick_up_date', 'return_date']
        widgets = {
            'pick_up_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'car_model']

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is None:
            raise forms.ValidationError("Please enter a valid rating")
        return score
        
