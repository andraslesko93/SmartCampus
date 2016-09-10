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
    #has_notification = forms.BooleanField
    class Meta:
        model = UserProfile
        fields = ('local_picture',)

class ProblemForm(forms.ModelForm):   
    title = forms.CharField (max_length = 30, help_text ="Title:", widget=forms.TextInput(attrs={'size': 30}))
    place = forms.CharField (max_length = 30, help_text = "Place:", widget=forms.TextInput(attrs={'size': 30}))
    desc = forms.CharField (max_length = 300, help_text = "Description", widget=forms.Textarea(attrs={'cols': 31, 'rows': 5}))
    tags = forms.CharField (max_length = 50, help_text = "Tags", widget=forms.TextInput(attrs={'size': 30}))
    status = forms.CharField (max_length = 10, help_text ="Status", widget=forms.TextInput(attrs={'size': 30}))
    rq_ppl = forms.IntegerField (help_text="Required people:",
                                 min_value = 1, 
                                 widget=forms.TextInput(attrs={'size': 30}))
    added_at = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], help_text="added_at")
    deadline = forms.DateTimeField(help_text="Deadline", widget=forms.DateTimeInput(attrs={'size': 30}))
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Problem
        exclude = ("key_field",)
        fields = ('title','place', 'desc', 'tags', 'status', 'rq_ppl', 'added_at', 'deadline', 'user')
        
        
class SolutionForm (forms.ModelForm):
    desc = forms.CharField (max_length = 300, help_text = "Description", widget=forms.Textarea(attrs={'cols': 31, 'rows': 5}))
    served_ppl = forms.IntegerField (help_text="Served people:",
                                 min_value = 1, 
                                 widget=forms.TextInput(attrs={'size': 30}))
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Solution
        exclude = ("user_id","problem_id")
        fields = ('desc', 'status', 'served_ppl')

