from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

class ExceptionHandlerMixin:
    def handle_exceptions(self, method, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ValidationError as exc:
            return Response({'error': exc.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def create(self, request, *args, **kwargs):
        return self.handle_exceptions(super().create, request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return self.handle_exceptions(super().update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.handle_exceptions(super().destroy, request, *args, **kwargs)
