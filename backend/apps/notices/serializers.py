from rest_framework import serializers
from .models import Notice
from apps.accounts.serializers import UserProfileSerializer

class NoticeSerializer(serializers.ModelSerializer):
    author_details = UserProfileSerializer(source='author', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    audience_display = serializers.CharField(source='get_audience_display', read_only=True)

    class Meta:
        model = Notice
        fields = [
            'id', 'title', 'content', 'category', 'category_display',
            'audience', 'audience_display', 'author', 'author_details',
            'is_urgent', 'views', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'views']

    def create(self, validated_data):
        # Automatically set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
