from rest_framework import exceptions
class BadRequest(exceptions.APIException):
    status_code = 400
    default_detail = 'Bad Request.'
    default_code = 'bad_request'
    