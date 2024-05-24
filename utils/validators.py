from rest_framework import serializers

def validate_name(value):
    if len(value) < 3:
        raise serializers.ValidationError("The name must have at least 3 characters.")
    return value

def validate_price(value):
    if value <= 0:
        raise serializers.ValidationError("The price must be positive.")
    return value