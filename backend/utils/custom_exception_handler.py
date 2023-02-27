from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__
    
    print(exception_class)
    
    if exception_class == 'AuthenticationFailed':
        response.data = {
            "error" : "Email and Password is invalid."
        }
    elif exception_class == 'NotAuthenticated':
        response.data = {
            "error" : "Login Required."
        }
        
    return response