from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, LookupError):
        return Response(
            {"error": str(exc)},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ValueError):
        return Response(
            {"error": str(exc)},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return Response(
        {"error": "An unexpected error occurred."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

def custom_exception_handler(exc, context):
    import traceback
    traceback.print_exc()
    return Response({"error": str(exc)}, status=500)