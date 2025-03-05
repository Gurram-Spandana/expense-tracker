from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Sum
from datetime import datetime

def home(request):
    return render(request, 'expenses/home.html')

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('expense_list')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# List all expenses
@login_required
def expense_list(request):
    if request.user.is_authenticated:
        selected_month = request.GET.get('month', datetime.today().strftime('%Y-%m'))
        year, month = map(int, selected_month.split('-'))
        current_month = datetime.today().strftime('%Y-%m')           # Get the current month and year
        selected_month = request.GET.get('month', current_month)  # Get selected month from request defualting to current month
        year, month = map(int, selected_month.split('-'))    # Convert selected month to year and month format
        is_current_month = (selected_month == current_month)
        expenses = Expense.objects.filter(user=request.user,date__year=year, date__month=month).order_by('-date')  # Filter by logged-in user
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0  # Calculate total
    else:
        expenses = []
        total_expenses = 0
        selected_month = datetime.today().strftime('%Y-%m')
        is_current_month = True

    return render(request, 'expenses/expense_list.html', {'expenses': expenses,'total_expenses': total_expenses,'selected_month': selected_month,'is_current_month': is_current_month})

# Add new expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # Update this with the correct redirect URL
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')  # Update this with the correct redirect URL

    return render(request, 'expenses/delete_expense.html', {'expense': expense})

