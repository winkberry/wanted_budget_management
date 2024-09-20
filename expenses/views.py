from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer, DailyExpenseSerializer
from django.utils import timezone  # 기간 필터를 처리할 때 사용할 수 있음
from budget_management.models import BudgetCategory
from decimal import Decimal
from rest_framework.views import APIView
from datetime import date  # 이 부분을 추가


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
    


class DailyExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        current_month = date.today().month

        # 오늘 날짜의 지출 데이터 조회
        today_expenses = Expense.objects.filter(user=user, date=date.today())

        if not today_expenses.exists():
            return Response({"error": "오늘 지출 데이터가 없습니다."}, status=404)

        # 카테고리별 지출 총액 계산
        category_summary = today_expenses.values('category__category').annotate(total=Sum('amount'))

        summary = []
        for category_data in category_summary:
            category_name = category_data['category__category']
            spent_amount = category_data['total']

            # 해당 카테고리의 월 예산 정보 가져오기
            budget_category = BudgetCategory.objects.filter(user=user, category=category_name, month=current_month).first()
            if not budget_category:
                daily_budget = Decimal(0)  # 예산 정보가 없으면 0으로 처리
            else:
                daily_budget = budget_category.amount / Decimal(31)  # 적정 지출 금액 (예산 / 31일)

            # float로 변환해서 퍼센트 계산
            risk_percentage = (float(spent_amount) / float(daily_budget)) * 100 if daily_budget > 0 else 0
            daily_budget_rounded = round(float(daily_budget), 2)  # 소수점 2자리로 제한

            summary.append({
                'category': category_name,
                'total_expense': spent_amount,
                'appropriate_expense': daily_budget_rounded,  # 소수점 2자리까지 표현
                'risk_percentage': round(risk_percentage, 2),  # 위험도도 소수점 2자리까지
            })

        # 오늘 총 지출 금액 계산
        total_expense = today_expenses.aggregate(total=Sum('amount'))['total'] or 0

        return Response({
            'total_expense': total_expense,
            'category_summary': summary,
        }, status=200)
    

class DailyBudgetRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        today = date.today()
        current_month = today.month
        days_in_month = 31  # 한 달을 31일로 고정

        # 이번 달의 예산을 가져옴
        budget_categories = BudgetCategory.objects.filter(user=user, month=current_month)
        if not budget_categories.exists():
            return Response({"error": "예산이 설정되지 않았습니다."}, status=404)

        # 현재까지의 지출 총액 및 카테고리별 지출
        spent_up_to_today = Expense.objects.filter(user=user, date__lte=today).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
        days_passed = today.day
        days_left = days_in_month - days_passed

        # 카테고리별 지출 금액 계산
        total_budget = budget_categories.aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
        recommended_total_today = Decimal(total_budget) / Decimal(days_in_month)

        # 이미 사용한 금액 계산
        spent_today = Expense.objects.filter(user=user, date=today).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
        overspent = max(Decimal(0), spent_today - recommended_total_today)

        # 남은 일수 동안 부담을 분배
        daily_adjusted_budget = recommended_total_today
        if days_left > 0:
            daily_adjusted_budget -= overspent / Decimal(days_left)

        # 최소 금액 보장
        daily_adjusted_budget = max(daily_adjusted_budget, Decimal(5000))

        # 카테고리별 추천 금액 계산
        category_recommendations = []
        for category in budget_categories:
            category_budget_per_day = Decimal(category.amount) / Decimal(days_in_month)
            category_spent_today = Expense.objects.filter(user=user, category=category, date=today).aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
            category_overspent = max(Decimal(0), category_spent_today - category_budget_per_day)

            # 남은 기간 동안 초과분을 분배
            category_adjusted_budget = category_budget_per_day
            if days_left > 0:
                category_adjusted_budget -= category_overspent / Decimal(days_left)

            # 최소 금액 보장
            category_adjusted_budget = max(category_adjusted_budget, Decimal(5000))

            category_recommendations.append({
                "category": category.category,
                "recommended_amount": int(round(category_adjusted_budget))  # 소수점 제거
            })

        # 상황에 맞는 멘트
        if spent_today < recommended_total_today:
            message = "절약을 잘 실천하고 계시네요! 오늘도 절약 도전!"
        elif spent_today == recommended_total_today:
            message = "적정하게 지출하고 계십니다. 꾸준히 유지하세요!"
        else:
            message = "오늘 예산을 초과했습니다. 남은 기간 동안 분배하여 조절하세요."

        # 최종 응답
        return Response({
            "total_recommended_amount": int(round(daily_adjusted_budget)),  # 소수점 제거
            "category_recommendations": category_recommendations,
            "message": message
        }, status=200)
    
