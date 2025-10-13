from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
class CustomerRegisterManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
class CustomerRegister(AbstractUser):
    # first_name = models.CharField(null = False, max_length = 50)
    # last_name = models.CharField(null= False , max_length= 50)
    height = models.FloatField(null = False , help_text = "height in cm")
    weight  = models.FloatField(null = False , help_text= "weight in km")
    # use snake_case to match serializers/tests
    fitness_goal = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length = 15 , blank = True)
    picture_url = models.URLField(blank=True, null=True)
    # Make email unique since we use it as the username field
    email = models.EmailField(unique=True, blank=False)
    
    # google sign in 
    google_id = models.CharField(max_length= 100 ,blank = True , null = True ,unique = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'height', 'weight']
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'auth_customerregister'
    
    #  the Abstractuser already have the email , password, firstname,lastname , is_active , last_viewed and many other things so make sure to do that 
    