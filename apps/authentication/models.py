from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from lib.utils import Crypt


# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=40)
	hashedID = models.CharField(max_length=256)
	created = models.DateField(auto_now_add=True)
	email = models.EmailField(blank=True)
	
	# Aca va mas informacion del usuario que tenemos que agregar ademas en el metodo ADD
	#fistname = model.CharField(max_length=40, blank=True)
	#lastname = model.CharField(max_length=40, blank=True)
	
	def __unicode__(self):
		return self.username + " - " + self.email
		
	# Debemos agregar aqui la informacion adicional que podea el usuario,
	# para poder inicializarlo correctamente
	@classmethod
	def add(self, username, passwd, email = ''):
		hashedID = Crypt.encryptUserInfo(username,passwd)
		if User.objects.filter(username = username).count() != 0:
			return None
		u = User(username = username,hashedID = hashedID, email = email)
		u.save()
		return u

	@classmethod
	def getByUsername(self, username):
		try:
			user = User.objects.filter(username = username).get()
		except ObjectDoesNotExist:
			return None
		
		return user
	
	@classmethod
	def isValidLogin(self, username, passwd):
		user = User.getByUsername(username)
		if not user:
			return False
		# Si el usuario existe, chequeo su correspondiente hash con el generado con la informacion
		# que se recibio.
		return Crypt.verifyUserInfo(username,passwd,user.hashedID)
		
		
	@classmethod
	def isValidUsername(self, username):
		# Logica de validacion de usuario
		return True
	
	@classmethod
	def isValidPassword(self, username):
		# Logica de validacion de contrasenia
		return True
	
	@classmethod
	def isValidEmail(self, username):
		# Logica de validacion de email
		return True
	
