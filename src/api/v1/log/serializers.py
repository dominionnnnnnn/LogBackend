from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['id', 'content', 'status', 'date', 'hours_worked']
        read_only_fields = ['id', 'status']
        
class LogUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['status']
        
    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        if new_status not in ['approved', 'rejected']:
            raise serializers.ValidationError({
                'status': "Only 'approved' or 'rejected' are valid status updates."
            })

        instance.status = new_status
        instance.save()
        return instance