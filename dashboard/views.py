from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, HttpResponse, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from expenseapp.models import Expense
from django.db.models.functions import TruncMonth
from django.db.models import Sum
import json
from datetime import datetime, timedelta

# Create your views here.
def auth_dashboard(request):
    if request.user.is_authenticated: # if user is logged in
        return redirect('dashboard')
    else: # if user is not logged in
        return redirect('user_login')
    
@login_required
def dashboard(request):
    # Define the user variable
    user = request.user
    # Get today's date
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)
    # Fetch the expense data for the logged-in user
    expenses = Expense.objects.filter(user=request.user, date__gte=one_year_ago).order_by('date')
    # Aggregate expenses by category for the logged-in user
    expenses_by_category = (
        Expense.objects.filter(user=user)
        .values('category')
        .annotate(total_amount=Sum('amount'))
    )
    # Aggregate expenses by month for the logged-in user
    expenses_by_month = (
        Expense.objects.filter(user=user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total_amount=Sum('amount'))
        .order_by('month')
    )
    # Extract the data for the chart
    dates = [expense.date.strftime('%Y-%m-%d') for expense in expenses]
    amounts = [float(expense.amount) for expense in expenses]  # Convert Decimal to float
    # Convert data to JSON format for use in the template
    context = {
        'dates': json.dumps(dates),
        'amounts': json.dumps(amounts),
        'expenses_by_category': expenses_by_category,
        'expenses_by_month': expenses_by_month,
    }
    return render(request, 'dashboard/dashboard.html', context)


def user_login(request):
    return render(request, 'authenticate/login.html')

def user_signup(request):
    return render(request, 'authenticate/signup.html')

def signup(request):
    # handeling POST requesting
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # Validation Checking
        if len(username) > 10 :
            # flashing error message
            messages.error(request, 'Username must be  More than 1 and less than 10 characters')  
            return redirect('user_signin')
        if len(username) < 1 :
            # flashing error message
            messages.error(request, 'Username must be  More than 1 and less than 10 characters')  
            return redirect('user_signin')
        if password != password2 :
            # flashing error message
            messages.error(request, 'Passwords must be matched')  
            return redirect('user_signin')
        # Creating User
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        # flashing success message
        messages.success(request, 'User Created Sucessfully')
        return redirect('dashboard')
    else:
        return HttpResponse('404 - Not Found')
    
def signin(request):
    # handeling POST requesting
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        # authenticating user
        user = authenticate(username = loginusername, password= loginpassword)
        # if user is matched then giving accesss
        if user is not None:
            login(request,user)
            messages.success(request, 'Loggedin Sucessfully')
            return redirect('dashboard')
        # if user is not matched then acced denied 
        else:
            messages.error(request, 'Invalid Information')
            return redirect('user_login')
    return HttpResponse('404 - Not Found')

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Loggedout Sucessfully')
    return redirect('auth_dashboard')
