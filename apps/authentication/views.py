from django.http import HttpResponse
from app.authentication.models import User

# Create your views here.

class AuthAppView:
    @require_GET()
    def SigninGET(self, request):
        #Aca envio el formulario de creacion de usuario
        pass
    
    @require_POST()
    def SigninPOST(self, request):
        #Aca valido la informacion de creacion de usuario
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        email = request.GET.get('email', '')
        
        if not User.isValidUsername(username):
            pass # Respondo con el formulario marcando el error de username invaludo
        elif not User.isValidPassword(password):
            pass # Respondo con el formulario marcando el error de password invaludo
        elif not User.isValidEmail(email):
            pass # Respondo con el formulario marcando el error de password invaludo
        elif user = User.add(username,password,email) == None:
            pass # Respondo con el formulario marcando usuario ya existente
        
        pass