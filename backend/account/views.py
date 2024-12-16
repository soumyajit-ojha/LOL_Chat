from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from account.forms import RegistrationForm, LoginForm
from . models import Account
from django.conf import settings
from django.db.models import Q


def registration_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You are already authenticate as {user.email} ")

    context={}
    if request.POST :
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            
            return redirect("home")
        else:
            context['registration_form'] = form
    
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}

    # If user is already logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid email or password.")
        context['login_form'] = form
    else:
        context['login_form'] = LoginForm()

    return render(request, 'account/login.html', context)


# User account and its modification
def account_view(request, *args, **kwargs):

    context = {}
    user_id = kwargs.get("user_id")
    print(f"User ID {user_id}")
    try:
        account = Account.objects.get(pk = user_id)
    except:
        HttpResponse("<h3 class = text-center> Something went wrong.</h3>")
    if account:
        context['user_id'] = account.id
        context["username"] = account.username
        context["email"] = account.email
        context["profile_image"] = account.profile_image.url
        context["hide_email"] = account.hide_email

        # define template variable for is_self and is_friend
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
    
        return render(request, 'account/account.html', context=context)
    else:
        return redirect("login")

# Search friends

def account_search_view(request, *args, **kwargs):
    context = {}
    print("view called")
    if request.method == "GET":
        search_query = request.GET.get("q")
        print(search_query)
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
            user = request.user
            accounts = []  # [(account1, True), (account2, False), ...]
            if user.is_authenticated:
                # get the authenticated users friend list
                # auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    accounts.append((account, False))  # auth_user_friend_list.is_mutual_friend(account)
                context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False))
                context['accounts'] = accounts
    # return HttpResponse("Data found")            
    return render(request, "account/search_results.html", context)
