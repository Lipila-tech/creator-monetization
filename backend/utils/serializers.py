from rest_framework import serializers

class SuccessResponseSerializer(serializers.Serializer):
    """
    Standard 202 Created response serializer.

    Used for successful resource creation responses.
    """
    status = serializers.CharField(default="success")
    data = serializers.JSONField()


class TipResponseSerializer(serializers.Serializer):
    """
    Standard 201 Created response serializer.

    Used for successful resource creation responses.
    """
    status = serializers.CharField(default="accepted")
    data = serializers.JSONField()


class CreatedResponseSerializer(serializers.Serializer):
    """
    Standard 201 Created response serializer.

    Used for successful resource creation responses.
    """
    status = serializers.CharField(default="success")
    data = serializers.JSONField()
    

class ErrorSerializer(serializers.Serializer):
    """
    Standard error response serializer.

    Used for non-field-specific errors such as authentication,
    authorization, not found, conflicts, rate limits, and server errors.
    """
    status = serializers.CharField(default="failed")
    error = serializers.CharField()
    message = serializers.CharField()
    errors = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField()
        )
    )


class ValidationErrorSerializer(serializers.Serializer):
    """
    Validation error response serializer.

    Used for 400 responses where one or more fields failed validation.
    """
    status = serializers.CharField(default="failed")
    error = serializers.CharField(default="validation_error")
    message = serializers.CharField()
    statusCode = serializers.IntegerField(default=400)
    errors = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField()
        )
    )

class UnauthorizedErrorSerializer(ErrorSerializer):
    """401 – Authentication required or token invalid"""
    error = serializers.CharField(default="forbidden")
    message = serializers.CharField(default="Client Authentication required or token invalid")


class ForbiddenErrorSerializer(ErrorSerializer):
    """403 – User does not have permission"""
    error = serializers.CharField(default="forbidden")
    message = serializers.CharField(default="User does not have permission")


class NotFoundErrorSerializer(ErrorSerializer):
    """404 – Resource not found"""
    error = serializers.CharField(default="not_found")


class ConflictErrorSerializer(ErrorSerializer):
    """409 – Duplicate or conflicting request"""


class RateLimitErrorSerializer(ErrorSerializer):
    """429 – Too many requests"""


class ServerErrorSerializer(ErrorSerializer):
    """500 – Unexpected server error"""
