from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    # Call the default DRF exception handler
    response = exception_handler(exc, context)
    return response