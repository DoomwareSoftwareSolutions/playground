from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.authentication.models import User

# Create your views here.

def SignInView(self, request):
        if request.method == 'GET':
            # GET METHOD: Aca envio el formulario de logueo de usuario
            pass
        else:
            # POST METHOD: Aca valido la informacion de creacion de usuario 
            username = request.GET.get('username', '')
            password = request.GET.get('password', '')
            email = request.GET.get('email', '')
            
            if not User.isValidUsername(username):
                pass # Respondo con el formulario marcando el error de username invaludo
            elif not User.isValidPassword(password):
                pass # Respondo con el formulario marcando el error de password invaludo
            elif not User.isValidEmail(email):
                pass # Respondo con el formulario marcando el error de password invaludo
            elif user == User.add(username,password,email) == None:
                pass # Respondo con el formulario marcando usuario ya existente
            
            pass        
    
# Esta view maneja '/signup'. Renderea el formulario de registro y valida los datos ingresados y guarda el nuevo
# usuario en la DB
def SignUpView(request):
    if request.method == 'GET':
        # GET METHOD: Aca envio el formulario de logueo de usuario
        return render_to_response('signup.html',{},RequestContext(request))
    else:
        pass # TODO POST METHOD