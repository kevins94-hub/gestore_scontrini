from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from .models import Expense, ReceiptImage
from .forms import ExpenseForm, ReceiptUploadForm


def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'spese_app/expense_list.html', {'expenses': expenses})


def expense_create(request):
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        upload_form = ReceiptUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if expense_form.is_valid() and upload_form.is_valid():
            expense = expense_form.save()

            for f in files:
                ReceiptImage.objects.create(expense=expense, original_image=f)

            return redirect('spese_app:expense_list')
    else:
        expense_form = ExpenseForm()
        upload_form = ReceiptUploadForm()

    return render(request, 'spese_app/expense_create.html', {
        'expense_form': expense_form,
        'upload_form': upload_form,
    })


def monthly_report(request):
    today = timezone.now().date()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    expenses = Expense.objects.filter(date__year=year, date__month=month)
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'expenses': expenses,
        'total': total,
        'month': month,
        'year': year,
    }
    return render(request, 'spese_app/monthly_report.html', context)
