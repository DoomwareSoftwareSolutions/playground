from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from apps.authentication.models import User
from lib.utils import Crypt

# Create your views here.

# Esta view maneja '/signin'. Renderea el formulario de inicio de sesion y valida los datos ingresados
# buscando el usuario en la database.
def SignInView(request):
        if request.method == 'GET':
            # GET METHOD: Aca envio el formulario de logueo de usuario
            return render_to_response('signin.html',{},RequestContext(request))
        elif request.method == 'POST':
            # POST METHOD: Aca valido la informacion de inicio de sesion
            information = {}
            information['username'] = request.POST.get('username', '')
            password = request.POST.get('password', '')
            leave_open = request.POST.get('remember',None)
            
            valid = User.isValidLogin(information['username'], password)
            if not valid:
                information['error'] = "No existe el nombre de usuario especificado o la clave no es correcta"
                return render_to_response('signin.html',information,RequestContext(request))
            else:
                response = redirect('/')
                if leave_open is None:
                    Crypt.set_secure_cookie(response,'user_id',information['username'],expires=True) # Expira al cerrar el navegador
                else:
                    Crypt.set_secure_cookie(response,'user_id',information['username'],expires=False) # No expira la cookie
                return response
        else:
            raise PermissionDenied  
                
    
# Esta view maneja '/signup'. Renderea el formulario de registro y valida los datos ingresados y guarda el nuevo
# usuario en la DB
def SignUpView(request):
    if request.method == 'GET':
        # GET METHOD: Aca envio el formulario de creacion de usuario
        return render_to_response('signup.html',{},RequestContext(request))
    elif request.method == 'POST':
        # POST METHOD: Aca valido la informacion de creacion de usuario
        information = {}
        valid = True
        
        # Obtengo la informacon ingresada
        information['username'] = request.POST.get('username', '')
        password = request.POST.get('password', '')
        vpassword = request.POST.get('vpassword', '')
        information['email'] = request.POST.get('email', '')
        information['name'] = request.POST.get('name', '')
        information['lastname'] = request.POST.get('lastname', '')
        information['country'] = request.POST.get('country', '')
        leave_open = request.POST.get('remember',None)
        
        # Valido los datos.
        if not User.isValidUsername(information['username']):
            # Marco el error de username invaludo
            valid = False
            information['username_error'] = 'El nombre de usuario no es valido'
        elif not User.isValidPassword(password):
            # Marco el error de password invaludo
            valid = False
            information['password'] = ''
            information['password_error'] = 'La clave no es valida'
        elif password != vpassword:
            # Marco el error de passwords distintas
            valid = False
            information['vpassword'] = ''
            information['password_error'] = 'Las claves no coinciden'
        elif not User.isValidEmail(information['email']):
            # Marco el error de password invaludo
            valid = False
            information['email_error'] = 'El email ingresado no es valido'
        else:
            user = User.add(information['username'],password,information['email'],information['name'], information['lastname']);
            if  user == None:
                # Marco el error de usuario ya existente
                valid = False
                information['username_error'] = 'El usuario ya existe. Ingrese otro'
        
        
        if valid == False:
            # Hubo un error al crear el usuario. Vuelvo a enviar el formulario de creacion con los errores respectivos
            return render_to_response('signup.html',information ,RequestContext(request))
        else:
            # Se creo un usuario, redirijo pero seteo la cookie para identificar
            response = redirect('/')
            response.set_signed_cookie('user_id', information['username'])
            return response
    else:
        raise PermissionDenied
    
def LogOutView(request):
    if request.method == 'GET':
        response = redirect('/')
        response.delete_cookie('user_id')
        return response
    else:
        raise PermissionDenied
    
def PasswordRecoverView(request):
    if request.method == 'GET':
        # GET METHOD: Aca envio el formulario de recuperacion de contrasenia
        cookie = request.get_signed_cookie(key='lpwd_ok', default=None)
        if cookie is None:
            return render_to_response('passwd_recover.html',{},RequestContext(request))
        else:
            information = {}
            information['username'] = cookie.split('|')[0]
            information['email'] = cookie.split('|')[1]
            return render_to_response('passwd_recover_confirm.html',information,RequestContext(request))
    elif request.method == 'POST':
        information = {}
        information['username'] = request.POST.get('username', None)
        if not User.isValidUsername(information['username']):
            information['error'] = 'Por favor ingrese el nombre de usuario correctamente'
        else:
            user = User.getByUsername(information['username'])
            if user is None:
                information['error'] = 'El nombre de usuario especificado no existe'
            else:
                information['email'] = user.email;
                response = redirect('/passwd_recover') #Redirect to confirmation
                Crypt.set_secure_cookie(response,'lpwd_ok',information['username']+ '|' + information['email'] , expires=False,  time=7200)
                # Send mail TODO
                return response
            
        return render_to_response('passwd_recover.html',information,RequestContext(request))
    else:
        raise PermissionDenied
        
def PasswordRecoverResetView(request):
    if request.method == 'GET':
        response = redirect('/passwd_recover')
        response.delete_cookie(key='lpwd_ok')
        return response
    else:
        raise PermissionDenied