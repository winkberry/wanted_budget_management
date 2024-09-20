from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BudgetCategory
from .serializers import BudgetCategorySerializer

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