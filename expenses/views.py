from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .models import Expense
from .serializers import ExpenseSerializer
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