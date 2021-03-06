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
		
	def testUpdateUserPassword(self):
		u = User.add("user1","passwd",'user1@mail.com')
		self.assertTrue(User.isValidLogin("user1","passwd"))
		u.updateUserPassword("newpasswd")
		self.assertFalse(User.isValidLogin("user1","passwd"))
		self.assertTrue(User.isValidLogin("user1","newpasswd"))
				
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
		
	def testUsernameValidation(self):
		self.assertTrue(User.isValidUsername('abcdef12345_ghijk678')) #Normal characters
		self.assertTrue(User.isValidUsername('abcdef12345-ghijk678')) #Normal characters
		self.assertTrue(User.isValidUsername('abcdef1_345_ghijk678')) #Two Undercords
		self.assertTrue(User.isValidUsername('abcdef1-345-ghijk678')) #Two cords
		self.assertTrue(User.isValidUsername('123')) #ThreeChars
		self.assertTrue(User.isValidUsername('12345678901234567890')) #TwentyChars
		
		self.assertFalse(User.isValidUsername('')) #Empty
		self.assertFalse(User.isValidUsername('12')) #TwoChars
		self.assertFalse(User.isValidUsername('123456789012345678901')) #TwentyOneChars
		self.assertFalse(User.isValidUsername('randomchars++=?')) #Rare Characters
		
	def testPasswordValidation(self):
		self.assertTrue(User.isValidPassword('abcdef12345_ghijk678')) #Normal characters
		self.assertTrue(User.isValidPassword('abcdef12345-ghijk678')) #Normal characters
		self.assertTrue(User.isValidPassword('abcdef1_345_ghijk678')) #Two Undercords
		self.assertTrue(User.isValidPassword('abcdef1-345-ghijk678')) #Two cords
		self.assertTrue(User.isValidPassword('123')) #ThreeChars
		self.assertTrue(User.isValidPassword('12345678901234567890')) #TwentyChars
		self.assertTrue(User.isValidPassword('randomchars++=?')) #Rare Characters
		
		self.assertFalse(User.isValidPassword('')) #Empty
		self.assertFalse(User.isValidPassword('12')) #TwoChars
		self.assertFalse(User.isValidPassword('123456789012345678901')) #TwentyOneChars
		
	def testEmailValidation(self):
		self.assertTrue(User.isValidEmail('unstring@otrostring.str')) #Normal mail
		
		self.assertFalse(User.isValidEmail('unstring@otrostring')) #Mail without.com
		self.assertFalse(User.isValidEmail('unstring@otrostring.')) #Mail without com
		self.assertFalse(User.isValidEmail('unstring.com')) #Mail without @
		self.assertFalse(User.isValidEmail('@otrostring.com')) #Mail without name
		self.assertFalse(User.isValidEmail('otrostring')) #Normal string