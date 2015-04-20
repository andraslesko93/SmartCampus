from django.shortcuts import render
from problems.forms import UserForm, UserProfileForm, ProblemForm, SolutionForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django import forms
from datetime import datetime
from problems.models import Problem, Solution, UserProfile, Ignore
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def index(request):
    ignored_users = Ignore.objects.all()
    ignored_users = ignored_users.filter (user_id__exact=request.user)
    problem_list = Problem.objects.all()
    problem_list = Problem.objects.order_by('-deadline')
    problem_list = problem_list.filter (status__exact="pending")
    problem_list = problem_list.filter(~Q(user=ignored_users.values('ref_user_id')))
    
    context_dict = {'problems': problem_list}

    # Render the response and send it back!
    return render(request, 'problems/index.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

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
    
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':      
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/problems/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'problems/login.html', {})
    
    

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/problems/')

@login_required
def add_problems(request):
    if request.method == 'POST':
        
        
        new_data = request.POST.copy()
        new_data['status'] = 'pending'
        new_data['pub_date'] = datetime.now()
        new_data['user'] = request.user.id
        form = ProblemForm(data=new_data)
        
        if form.is_valid():
            # Save the new category to the database.
            
            #print form.status
            #form.pub_date = 
            temp = form.save(commit=False)
            temp.key_field = request.user
            temp.save()
            #form = temp
            #print temp.
            # Now call the index() view.
            # The user will be shown the homepage.
            return HttpResponseRedirect('/problems/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = ProblemForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'problems/add_problem.html', {'form': form})

@login_required
def add_solution(request, problem_title_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        problem = Problem.objects.get(slug=problem_title_slug)
       # context_dict['problem_title'] = problem.title
        context_dict['problem'] = problem
        
        
        ignored_users = Ignore.objects.all()
        ignored_users = ignored_users.filter (user_id__exact=request.user)
        solutions = Solution.objects.all()
        solutions = solutions.filter (problem_id__exact = problem)
        solutions= solutions.filter(~Q(user_id=ignored_users.values('ref_user_id')))
        
        
        context_dict['solutions'] = solutions
       # context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
    except Problem.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    
    if request.method == 'POST':    
        new_data = request.POST.copy()
        new_data['status'] = 'pending'
        new_data['user'] = request.user.id
        sol_form = SolutionForm(data=new_data)
        # Have we been provided with a valid form?
        #form.fields["status"].initial = "pending"
        if sol_form.is_valid():
            # Save the new category to the database.
            
            #print form.status
            #form.pub_date = 
            temp = sol_form.save(commit=False)
            temp.user_id = request.user
            temp.problem_id = problem
            temp.save()
            
            retlink = '/problems/add_solution/'+ problem.slug+'/'
            return HttpResponseRedirect(retlink)
        else:
            # The supplied form contained errors - just print them to the terminal.
            
            print sol_form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        sol_form = SolutionForm()
        

    # Go render the response and return it to the client.
    return render(request, 'problems/add_solution.html',{'problem':problem, 'sol_form':sol_form, 'solutions':solutions} )


@login_required
def own_problems(request):
    problem_list = Problem.objects.order_by('-deadline')
    problem_list = problem_list.filter (user__exact=request.user)
    context_dict = {'problems': problem_list}

    # Render the response and send it back!
    return render(request, 'problems/own_problems.html', context_dict)


@login_required
def accept_solution(request, solution_id_slug):
    context_dict = {}
    try:
        solution = Solution.objects.get(slug=solution_id_slug)
        context_dict['solution'] = solution
        
    except Solution.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    if request.method == 'POST' and request.user == solution.problem_id.user:   
        solution.status = 'accepted'
        solution.save()
        solution.problem_id.rq_ppl = solution.problem_id.rq_ppl - solution.served_ppl
        solution.problem_id.save()
        if (solution.problem_id.rq_ppl <= 0):
            solution.problem_id.status = 'accepted'
            solution.problem_id.save()
        
        retlink = '/problems/add_solution/'+ solution.problem_id.slug+'/'
        return HttpResponseRedirect(retlink)
    return render(request, 'problems/accept_solution.html', context_dict)


@login_required
def users(request, user_id_slug):
    context_dict = {}
    try:
        ref_user = UserProfile.objects.get(slug=user_id_slug)
        context_dict['ref_user'] = ref_user
    except UserProfile.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    
    if request.method == 'POST':
        
        check = Ignore.objects.all()
        check = check.filter (user_id__exact=request.user)
        check = check.filter (ref_user_id__exact=ref_user.user)
        
        if check.exists() :
            return HttpResponse('You already ignored that user')
        else:
            new_data = Ignore(user_id = request.user, ref_user_id = ref_user.user)
            new_data.save()
        return HttpResponseRedirect('/problems/')

    return render(request, 'problems/users.html', context_dict)


@login_required
def ignored_users(request):
    context_dict = {}
    ignored_users = Ignore.objects.all()
    ignored_users = ignored_users.filter (user_id__exact=request.user)
    context_dict = {'ignored_users': ignored_users}
    return render(request, 'problems/ignored_users.html', context_dict)