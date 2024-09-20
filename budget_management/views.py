from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BudgetCategory
from .serializers import BudgetCategorySerializer, CategorySerializer
from django.db.models import Avg, Sum
from collections import defaultdict

# 예산 추천
class BudgetRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request):
        total_amount = request.data.get("total_amount")

        if not total_amount:
            return Response({"error": "Total amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total_amount = int(total_amount)
        except ValueError:
            return Response({"error": "Total amount must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # 카테고리별 평균 금액 비율 계산
        category_averages = BudgetCategory.objects.values('category').annotate(avg_amount=Avg('amount'))

        if not category_averages:
            return Response({"error": "No data available for recommendation."}, status=status.HTTP_400_BAD_REQUEST)

        # 전체 평균 금액의 합
        total_avg = sum([cat['avg_amount'] for cat in category_averages])

        recommended_budget = []
        small_categories = []
        other_percentage = 0

        # 카테고리별 추천 예산 계산
        for category in category_averages:
            percentage = category['avg_amount'] / total_avg

            if percentage <= 0.10:
                # 10% 이하의 카테고리들은 '기타'로 묶기 위해 저장
                small_categories.append(category)
                other_percentage += percentage
            else:
                # 10% 이상의 카테고리들은 개별적으로 추천 예산 생성
                recommended_budget.append({
                    "category": category['category'],
                    "amount": int(total_amount * percentage)
                })

        # 10% 이하의 카테고리들을 '기타'로 묶기
        if small_categories:
            recommended_budget.append({
                "category": "other",
                "amount": int(total_amount * other_percentage)
            })

        return Response(recommended_budget, status=status.HTTP_200_OK)


# 카테고리 목록 뷰
class CategoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        # BudgetCategory 모델의 CATEGORY_CHOICES를 리스트로 변환
        categories = [{'category': key, 'label': value} for key, value in BudgetCategory.CATEGORY_CHOICES]
        # 카테고리 리스트를 시리얼라이저로 변환
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


# 카테고리 별 예산 설정과 설정된 목록 반환
class BudgetCategoryBulkCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data  # 여러 개의 카테고리 데이터를 받음 (리스트)
        
        if isinstance(data, list):  # 데이터가 리스트 형태인지 확인
            serializer = BudgetCategorySerializer(data=data, many=True, context={'request': request})
        else:
            return Response({"error": "Data should be a list of categories."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # 현재 유저의 예산 설정 목록 반환
        queryset = BudgetCategory.objects.filter(user=request.user)
        serializer = BudgetCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)