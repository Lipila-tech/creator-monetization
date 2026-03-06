from rest_framework import serializers

class LoginResponseSerializer(serializers.Serializer):
    """
    Standard 200 OK response serializer for login endpoint.

    Used to return user access and refresh tokens upon successful login.
    """
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = serializers.DictField(
        child=serializers.CharField(),
        help_text="Authenticated user details",
    )
    

class RegistrationResponseSerializer(serializers.Serializer):
    """
    Standard 201 Created response serializer for registration endpoint.

    Used to return newly created user access and refresh tokens upon successful registration.
    """
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = serializers.DictField(
        child=serializers.CharField(),
        help_text="Authenticated user details",
    )
    
class SuccessResponseSerializer(serializers.Serializer):
    """
    Standard 200 OK response serializer.

    Used for successful resource creation responses.
    """
    status = serializers.CharField(default="success")
    data = serializers.DictField(
        child=serializers.CharField(),
        allow_null=True,
        default=None
    )


class CreatedResponseSerializer(serializers.Serializer):
    """
    Standard 201 Created response serializer.

    Used for successful resource creation responses.
    """
    status = serializers.CharField(default="success")
    data = serializers.DictField(
        child=serializers.CharField(),
        allow_null=True,
        default=None
    )
    

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
    error = serializers.CharField(default="conflict")
    message = serializers.CharField(default="Duplicate or conflicting request")


class RateLimitErrorSerializer(ErrorSerializer):
    """429 – Too many requests"""
    error = serializers.CharField(default="rate_limit_exceeded")
    message = serializers.CharField(default="Too many requests - rate limit exceeded")


class ServerErrorSerializer(ErrorSerializer):
    """500 – Unexpected server error"""
    error = serializers.CharField(default="server_error")
    message = serializers.CharField(default="An unexpected error occurred on the server")
