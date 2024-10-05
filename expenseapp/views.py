from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from expenseapp.models import Expense
from expenseapp.forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .currency_converter import get_exchange_rates, convert_currency
from django.core.paginator import Paginator
import csv, openpyxl
from openpyxl import Workbook
 
@login_required
def expense_home(request):
    allExpenses = Expense.objects.filter(user=request.user).order_by('-date')
    # Implementing pagination: Show 5 expenses per page
    paginator = Paginator(allExpenses, 5)  # Show 5 expenses per page
    page_number = request.GET.get('page')  # Get the page number from the query parameters
    page_expenses = paginator.get_page(page_number)  # Get expenses for the requested page
    context = {
        'allExpenses': allExpenses,
        'page_expenses': page_expenses,
        }
    return render(request, 'expense/expensehome.html', context)

@login_required
def view_expense(request, slug):
    expense = Expense.objects.filter(slug = slug).first()
    context = {
        'expense' : expense,
        }
    return render(request, 'expense/viewexpense.html', context)

@login_required
def addexpense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)  # Save the data temporarily
            expense.user = request.user  # Assign the logged-in user to the expense
            expense.save()  # Save to the database
            messages.success(request, 'Expense Added Sucessfully')
            return redirect('expense_home')  # Redirect to the expense home page after saving
        else:
            messages.error(request, 'Failed to Add Expense')
            print(form.errors)  # Print form errors to debug why it's not saving
    else:
        form = ExpenseForm()
    return render(request, 'expense/addexpense.html', {'form': form})

@login_required
def edit_expense(request, slug):
    # Get the expense object or return a 404 if it doesn't exist
    expense = get_object_or_404(Expense, slug=slug, user=request.user)
    if request.method == 'POST':
        # Bind the form to the POST data and the existing expense
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()  # Save the updated data
            messages.success(request, 'Expense edited Sucessfully')
            return redirect('expense_home')  # Redirect to expense home or some other page after saving
    else:
        # Display the form pre-filled with the current expense data
        form = ExpenseForm(instance=expense)
    context = {
        'form': form,
        'expense': expense
    }
    return render(request, 'expense/editexpense.html', context)

@login_required
def delete_expense(request, slug):
    # Get the expense object or return a 404 if it doesn't exist
    expense = get_object_or_404(Expense, slug=slug, user=request.user)
    if request.method == 'POST':
        expense.delete()  # Delete the expense
        messages.success(request, 'Expense deleted Sucessfully')
        return redirect('expense_home')  # Redirect to the expense home or some other page after deleting
    # Optional: Render a confirmation page before deletion
    context = {
        'expense': expense
    }
    return render(request, 'expense/confirm_delete.html', context)

@login_required
def search_expense(request):
    query = request.GET.get('query', '')  # Safely get the query parameter
    # Initialize an empty queryset for results
    allExpense = Expense.objects.none()
    # Only search if query is not too long
    if len(query) > 40:
        messages.error(request, 'Search query is too long.')
    elif query:  # If query is not empty
        # Search in different fields
        allExpense = Expense.objects.filter(user=request.user).filter(
            Q(title__icontains=query) |  # Search by title
            Q(description__icontains=query) |  # Search by description
            Q(amount__icontains=query) |  # Search by amount
            Q(date__icontains=query)  # Search by date
        ).distinct()  # Ensure no duplicate results

    # If no results found
    if allExpense.count() == 0:
        messages.error(request, 'No result found.')
    
    # Pass the results to the template
    params = {'allExpense': allExpense, 'query': query}
    return render(request, 'expense/searchresult.html', params)

def exchange_rates_view(request):
    rates = get_exchange_rates()
    if not rates:
        messages.error(request, "Error fetching exchange rates.")
        rates = {}
    return render(request, 'expense/exchange_rates.html', {'rates': rates})

def currency_converter_view(request):
    converted_amount = None
    if request.method == 'POST':
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')
        amount = request.POST.get('amount')

        try:
            amount = float(amount)
            converted_amount = convert_currency(from_currency, to_currency, amount)

            if converted_amount is None:
                messages.error(request, "Conversion failed. Please try again.")
            else:
                messages.success(request, f"Converted Amount: {converted_amount:.2f} {to_currency.upper()}")
        except ValueError:
            messages.error(request, "Invalid amount. Please enter a valid number.")
    
    return render(request, 'expense/currency_converter.html', {'converted_amount': converted_amount})

@login_required
def export_expenses_csv(request):
    # Create an HTTP response with the CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    # Create a CSV writer object
    writer = csv.writer(response)
    # Write the header row for the CSV
    writer.writerow(['Title', 'Amount', 'Description', 'Date', 'User'])
    # Fetch the expense data for the logged-in user
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    # Write data rows for each expense
    for expense in expenses:
        writer.writerow([expense.title, expense.amount, expense.description, expense.date, expense.user])
    return response

@login_required
def export_expenses_excel(request):
    # Create an HTTP response with the Excel header
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    # Create an Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"
    # Write the header row
    ws.append(['Title', 'Amount', 'Description', 'Date', 'User'])
    # Fetch the expense data for the logged-in user
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    # Write data rows for each expense
    for expense in expenses:
        # Convert the `User` object to `expense.user.username` or any other field
        ws.append([expense.title, expense.amount, expense.description, expense.date, expense.user.username])
    # Save the workbook to the response
    wb.save(response)
    return response