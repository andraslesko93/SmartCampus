from django.shortcuts import render
from problems.forms import UserForm, UserProfileForm
from eventlog.models import Log
from problems.views.user_authentication import user_login
from problems.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

def register(request):

    registered = False
    welcome_reputation = 100
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if (request.POST.get('accept_terms', None)==None):
            error_message="You have to accept the terms of use before register to the application"
            return render(request, 'problems/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_message':error_message} )
        
        if (request.POST.get('username')==""):
            error_message="Username field is required"
            return render(request, 'problems/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_message':error_message} )
        
        if (request.POST.get('email')==""):
            error_message="Email field is required"
            return render(request, 'problems/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_message':error_message} )
        
        if (request.POST.get('password')==""):
            error_message="Password field is required"
            return render(request, 'problems/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_message':error_message} )
        
        if (request.POST.get('confirm_password')==""):
            error_message="Password confirmation field is required"
            return render(request, 'problems/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_message':error_message} )

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            if (request.POST.get('password')==request.POST.get('confirm_password')): 
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                
                profile = profile_form.save(commit=False)
                profile.user = user
            
                if 'local_picture' in request.FILES:
                    profile.local_picture = request.FILES['local_picture']
                # Now we save the UserProfile model instance.
                profile.save()
                profile.picture_url=profile.local_picture.url
                profile.reputation = welcome_reputation
                profile.save()
                # Update our variable to tell the template registration was successful.
                registered = True
                
                new_log_entry = Log(user = user, 
                                    action = "Registration",                            
                                    )
                new_log_entry.save()
                
                welcome_notification = Notification(user = user,
                                                    content_type = ContentType.objects.get_for_model(user)
                                                    )
                welcome_notification.save()
                
                user_login(request)
                retlink = '/'
                return HttpResponseRedirect(retlink)
            else:
                error_message="Password mismatch"
                return render(request, 'problems/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_message':error_message} )
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
            

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'problems/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )