from rest_framework import serializers

class VerifySerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.ChoiceField(choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ])
    tx_ref = serializers.CharField()

class TransferSerializer(serializers.Serializer):
    account_name = serializers.CharField()
    account_number = serializers.CharField()
    bank_code = serializers.IntegerField()