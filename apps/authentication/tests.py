from django.test import TestCase
from apps.authentication.models import User

class UserTest(TestCase):

	def testUsersRawCreation(self):
		u = User(username = "hello", hashedID = "123452", email = "hello@hello.com")
		u2 = User(username = "hello2", hashedID = "123452", email = "hello2@hello.com")
		u.save()
		U = User.objects.filter(username = "hello").get();
		self.assertEqual(u.username, U.username)
		self.assertNotEqual(u2.username, U.username)
		U = User.objects.filter(username = "hello2");
		self.assertEqual(0, U.count())
		u2.save()
		U = User.objects.filter(username = "hello2");
		self.assertEqual(1, U.count())
		
	def testUsersCreation(self):
		u = User.add("user1","passwd",'user1@mail.com')
		U = User.objects.filter(username = "user1").get()
		self.assertEqual(u, U)
		u2 = User.add("user2", 'passwd','mail@mail.com')
		U = User.objects.filter(username = "user2").get()
		self.assertEqual(u2, U)
	
	def testTwoEqualUsersCreation(self):
		u = User.add("user1","passwd",'user1@mail.com')
		u2 = User.add("user1","passwd",'user1@mail.com')
		self.assertIsNone(u2)
		u2 = User.add("user1","passwd", "mail@mail.com")
		self.assertIsNone(u2)
	
		
	def testUserGetByUsername(self):
		self.assertEqual(User.getByUsername("user1"), None)
		u = User.add("user1","passwd",'user1@mail.com')
		self.assertEqual(User.getByUsername("user1"), u)
		self.assertEqual(User.getByUsername("user2"), None)
		
	def testUserValidation(self):
		User.add("user1","passwd",'user1@mail.com')
		User.add("user2","passwd2",'user2@mail.com')		
		result = User.isValidLogin("user1","passwd")
		self.assertEqual(result, True)
		result = User.isValidLogin("user1","passwd2")
		self.assertEqual(result, False)
		result = User.isValidLogin("user2","passwd")
		self.assertEqual(result, False)
		result = User.isValidLogin("user2","passwd2")
		self.assertEqual(result, True)
		result = User.isValidLogin("user","passwd5")
		self.assertEqual(result, False)
	
	def testCompleteFields(self):
		User.add("user1","passwd",'user1@mail.com','User1','One')
		User.add("user2","passwd2",'user2@mail.com','User2', 'Two')
		u = User.getByUsername("user1")
		self.assertEqual(u.firstname, 'User1')
		self.assertEqual(u.lastname, 'One')
		u2 = User.getByUsername("user2")
		self.assertEqual(u2.firstname, 'User2')
		self.assertEqual(u2.lastname, 'Two')
		
	def testUpdateUserEmail(self):
		User.add("user1","passwd",'user1@mail.com','User1','One')
		u = User.getByUsername("user1")
		self.assertEqual(u.email, 'user1@mail.com')
		u.updateUserEmail('user2@mail.com')
		u = User.getByUsername("user1")
		self.assertEqual(u.email, 'user2@mail.com')
		
	def testUpdateUserFirstName(self):
		User.add("user1","passwd",'user1@mail.com','User1','One')
		u = User.getByUsername("user1")
		self.assertEqual(u.firstname, 'User1')
		u.updateUserFirstname('User2')
		u = User.getByUsername("user1")
		self.assertEqual(u.firstname, 'User2')
		
	def testUpdateUserLastName(self):
		User.add("user1","passwd",'user1@mail.com','User1','One')
		u = User.getByUsername("user1")
		self.assertEqual(u.lastname, 'One')
		u.updateUserLastname('Two')
		u = User.getByUsername("user1")
		self.assertEqual(u.lastname, 'Two')