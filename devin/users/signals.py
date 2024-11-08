from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

# Signal handlers
@receiver(post_save, sender=User)  # Create a Profile when a new User is created
def createProfile(sender, instance, created, **kwargs):
    print("Signal triggered")
    if created:
        # Create a Profile instance associated with the new User
        profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )
        subject = 'Welcome to DevIn – Where Developers Connect, Learn, and Grow!'
        message = """
        Hello {name},

        Welcome to DevIn – we're thrilled to have you join our community of passionate developers!

        At DevIn, we’re dedicated to helping developers like you connect, collaborate, and grow in a supportive environment. Here’s how you can get started:

        1. Complete Your Profile: Add details about your skills, interests, and experiences to connect with like-minded developers.
        2. Explore and Connect: Browse through our network, follow others, and connect with mentors and peers.
        3. Join Discussions & Projects: Engage in insightful discussions, contribute to projects, and stay updated with the latest in development.
        4. Share Your Work: Showcase your projects, write blogs, and share achievements to inspire others and get feedback.

        If you have any questions, feel free to reach out to our support team at support@devin.com.

        Welcome to DevIn, where developers like you are building the future together!

        Happy developing!

        Warm regards,
        The DevIn Team
        """
        send_mail(
        subject,
            message.format(name=profile.name),  # Using the profile name for a personal touch
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
        print('ProfileCreated!') 
        print('Profile instance:', profile)  # Debug: Show created profile instance
        print('User instance:', instance)  # Debug: Show user instance
        print("CREATED:", created)
@receiver(post_save,sender = Profile)
def updateUser(sender, instance, created, **kwargs):     
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
   


@receiver(post_delete, sender=User)  # Delete the Profile when a User is deleted
def deleteUser(sender, instance, **kwargs):
    # Attempt to delete the Profile instance associated with the deleted User
    try:
        profile = Profile.objects.get(user=instance)  # Get the associated Profile
        profile.delete()  # Delete the associated profile
        print('ProfileDeleted!', profile)  # Debug: Show deleted profile instance
    except Profile.DoesNotExist:
        print('No profile found for deleted user:', instance)  # Debug: Handle case where profile does not exist

@receiver(post_delete, sender=Profile)  # Delete the User when a Profile is deleted
def deleteUserFromProfile(sender, instance, **kwargs):
    user = instance.user  # Get the associated User
    if user:  # Check if the User exists
        user.delete()  # Delete the associated user
        print('UserDeleted!', user)  # Debug: Show deleted user instance
    else:
        print('No user found for deleted profile:', instance)  # Debug: Handle case where user does not exist

# Connect the signals
post_save.connect(updateUser,sender=Profile)
post_save.connect(createProfile, sender=User)  # Connect to User model
post_delete.connect(deleteUser, sender=User)  # Connect to User model
post_delete.connect(deleteUserFromProfile, sender=Profile)  # Connect to Profile model
