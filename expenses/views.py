from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer, DailyExpenseSerializer
from django.utils import timezone  # 기간 필터를 처리할 때 사용할 수 있음

class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 사용자 및 추가 로직을 적용하여 지출 항목을 저장
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ExpenseListView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Expense.objects.filter(user=user)

        # 기간 필터링
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])

        # 카테고리 필터링
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__category=category)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"error": "No expenses found for the given criteria."}, status=status.HTTP_404_NOT_FOUND)

        response = super().list(request, *args, **kwargs)

        # 전체 지출 합계
        total_expense = queryset.filter(excluded_from_total=False).aggregate(Sum('amount'))['amount__sum'] or 0

        # 카테고리별 합계
        category_totals = queryset.values('category__category').annotate(total=Sum('amount')).order_by()

        response.data = {
            'total_expense': total_expense,
            'category_totals': category_totals,
            'expenses': response.data
        }

        return Response(response.data, status=status.HTTP_200_OK)
    

class ExpenseUpdateView(generics.UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
class DailyExpenseSummaryView(generics.ListAPIView):
    serializer_class = DailyExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()  # 오늘 날짜
        user = request.user

        # 오늘 지출 항목 조회
        expenses_today = Expense.objects.filter(user=user, date=today)

        # 오늘 총 지출
        total_expense = expenses_today.aggregate(total=Sum('amount'))['total'] or 0

        # 카테고리별 지출 합계
        category_totals = expenses_today.values('category__category').annotate(total=Sum('amount'))

        # 위험도 계산 (카테고리별 예산과 비교)
        risk_data = []
        for category_total in category_totals:
            category_name = category_total['category__category']
            spent_amount = category_total['total']
            
            # 예산 정보 가져오기
            current_month = timezone.now().month
            budget_category = BudgetCategory.objects.filter(user=user, category=category_name, month=current_month).first()
            
            if budget_category:
                # 오늘 사용하면 적당한 금액 (예산 나누기 31일)
                daily_budget = budget_category.amount / 31
                risk_percentage = (spent_amount / daily_budget) * 100 if daily_budget > 0 else 0
                
                risk_data.append({
                    'category': category_name,
                    'daily_budget': round(daily_budget, 2),
                    'spent_amount': round(spent_amount, 2),
                    'risk_percentage': round(risk_percentage, 2),
                })

        return Response({
            'total_expense': total_expense,
            'risk_data': risk_data
        })