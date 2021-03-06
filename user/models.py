from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from education.models import Education
from technical_skill.models import SpecializationSkillExperience
from experience.models import Experience
# Allow Spaces in User names


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'


class Setting(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='Settings',
        on_delete=models.CASCADE,)

    show_footer = models.BooleanField(default=True)
    push_messages = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Setting'
        verbose_name_plural = 'Settings'
        ordering = ('-user',)

    # def __str__(self):
    #     return '%s: show_footer: %d, push_messages: %d' % (self.user, self.show_footer, self.push_messages)


class User(AbstractUser):
    facebook_id = models.CharField(blank=True, max_length=256)
    google_id = models.CharField(blank=True, max_length=256)
    picture = models.TextField(blank=True)
    uploaded_picture = models.ImageField(blank=True, null=True)
    username_validator = MyValidator()
    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username or email already exists."),
        },
    )
    bio = models.TextField(blank=True, max_length=1000)
    opt_in = models.BooleanField(blank=True, default=False)

    location = models.CharField(blank=True, max_length=256)

    profile_uri = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('-username',)
        unique_together = ('email',)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
            Setting.objects.create(user=instance)
    pass

    @property
    def get_picture(self):
        return self.picture
