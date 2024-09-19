from rest_framework import generics, permissions
from .models import BudgetCategory
from .serializers import BudgetCategorySerializer

class BudgetCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = BudgetCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 유저의 예산 설정만 가져옴
        return BudgetCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)