from rest_framework import serializers
from .models import Expense
from budget_management.models import BudgetCategory  # 카테고리 모델 가져오기

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.CharField()  # 카테고리를 이름으로 받음

    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date', 'memo', 'excluded_from_total']

    def create(self, validated_data):
        category_name = validated_data.pop('category')  # 카테고리 이름 추출

        try:
            # category_name을 CATEGORY_CHOICES에서 찾아서 검증
            category_choice = dict(BudgetCategory.CATEGORY_CHOICES).get(category_name)
            if not category_choice:
                raise serializers.ValidationError(f"Category '{category_name}' is not a valid choice.")
            
            # 현재 유저와 카테고리를 바탕으로 BudgetCategory를 찾음
            category = BudgetCategory.objects.get(user=self.context['request'].user, category=category_name)
        except BudgetCategory.DoesNotExist:
            raise serializers.ValidationError(f"Category '{category_name}' does not exist for this user.")
        
        # 현재 유저를 지출 항목에 추가
        validated_data['user'] = self.context['request'].user
        validated_data['category'] = category  # 카테고리 객체를 할당

        return super().create(validated_data)