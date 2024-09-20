import requests
from django.utils import timezone
from django.db.models import Sum
from .models import Expense
from budget_management.models import BudgetCategory
from django.contrib.auth import get_user_model

User = get_user_model()

def send_daily_spending_report():
    today = timezone.now().date()
    users = User.objects.all()

    for user in users:
        expenses_today = Expense.objects.filter(user=user, date=today)
        total_expense = expenses_today.aggregate(Sum('amount'))['amount__sum'] or 0
        category_totals = expenses_today.values('category__category').annotate(total=Sum('amount'))

        message = f"User: {user.username}\nToday Total Spending: {total_expense}\n"
        for category_total in category_totals:
            category_name = category_total['category__category']
            spent_amount = category_total['total']
            budget_category = BudgetCategory.objects.filter(user=user, category=category_name, month=today.month).first()
            
            if budget_category:
                daily_budget = budget_category.amount / 31
                risk_percentage = (spent_amount / daily_budget) * 100 if daily_budget > 0 else 0
                message += f"\nCategory: {category_name}, Spent: {spent_amount}, Risk: {risk_percentage}%"

        # Discord Webhook 발송
        webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'
        requests.post(webhook_url, json={"content": message})