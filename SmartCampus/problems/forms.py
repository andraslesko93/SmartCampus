from django import forms
from problems.models import Solution, Ignore, Problem, UserProfile
from django.contrib.auth.models import User

my_default_errors = {
    'required': 'Tolts ki plz.',
    'invalid': 'Rendesen toltsd ki plz'
} # Igy lehet felulirni a default error-t

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('picture',)

class ProblemForm(forms.ModelForm):
    title = forms.CharField (max_length = 30, help_text ="Title:")
    place = forms.CharField (max_length = 30, help_text = "Place:")
    desc = forms.CharField (max_length = 300, help_text = "Description")
    tags = forms.CharField (max_length = 50, help_text = "Tags")
    status = forms.CharField (max_length = 10, help_text ="Status")
    rq_ppl = forms.IntegerField (help_text="Required people:")
    pub_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], help_text="pub_date")
    deadline = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], help_text="Deadlin")
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Problem
        exclude = ("key_field",)
        fields = ('title','place', 'desc', 'tags', 'status', 'rq_ppl', 'pub_date', 'deadline', 'user')
        
        
class SolutionForm (forms.ModelForm):
    desc = forms.CharField (max_length = 300, help_text = "Description")
    served_ppl = forms.IntegerField (help_text="Served people:")
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Solution
        exclude = ("user_id","problem_id")
        fields = ('desc', 'status', 'served_ppl')

