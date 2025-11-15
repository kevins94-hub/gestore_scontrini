from django.contrib import admin
from .models import Expense, ReceiptImage

class ReceiptImageInline(admin.TabularInline):
    model = ReceiptImage
    extra = 1

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'city', 'province', 'amount')
    list_filter = ('category', 'city', 'province', 'date')
    inlines = [ReceiptImageInline]

@admin.register(ReceiptImage)
class ReceiptImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'expense', 'uploaded_at')
