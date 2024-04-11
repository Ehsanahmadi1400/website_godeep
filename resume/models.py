from django.db import models
from django.contrib.auth.models import User


# English resume models
class UserProfile(models.Model):
    SINGLE = 1
    MARRIED = 2

    MARITAL_STATUS_CHOICES = [
        (SINGLE, 'Single'),
        (MARRIED, 'Married'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_title = models.CharField(max_length=32, null=True, blank=True)
    first_name_resume = models.CharField(max_length=32, null=True, blank=True)
    last_name_resume = models.CharField(max_length=32, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='birth', null=True, blank=True)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_STATUS_CHOICES, default=SINGLE, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    home_address = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name_resume} {self.last_name_resume}"


class WorkExperience(models.Model):
    WORKING = 1
    FINISHED = 2

    WORK_EXPERIENCE_CHOICES = [
        (WORKING, 'Working'),
        (FINISHED, 'Finished')
    ]

    user = models.ForeignKey(User, related_name='work_experiences', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=WORK_EXPERIENCE_CHOICES)
    city = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    company = models.CharField(max_length=64, null=True, blank=True)
    last_position = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.company}"


class Education(models.Model):
    CONTINUING = 1
    FINISHED = 2

    EDUCATION_CHOICES = [
        (CONTINUING, 'Continuing'),
        (FINISHED, 'Finished')
    ]

    user = models.ForeignKey(User, related_name='educations', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=EDUCATION_CHOICES)
    degree = models.CharField(max_length=32, null=True, blank=True)
    institute = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    average = models.FloatField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.institute} {self.average}"


class Skill(models.Model):

    user = models.ForeignKey(User, related_name='skills', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True, blank=True)
    level_of_skill = models.CharField(max_length=48, null=True, blank=True, verbose_name='level')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}  {self.level_of_skill}"


class Language(models.Model):
    user = models.ForeignKey(User, related_name='languages', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True, blank=True)
    level_of_language = models.CharField(max_length=48, null=True, blank=True, verbose_name='level')
    certificate = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}  {self.level_of_language}"


class Course(models.Model):
    user = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    period = models.CharField(max_length=48, null=True, blank=True)
    certificate = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}  {self.certificate}"


class Project(models.Model):
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}"


class Competence(models.Model):  # Quality
    user = models.ForeignKey(User, related_name='competences', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.title}"


class Image(models.Model):
    user = models.ForeignKey(User, related_name='images', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    signature_image = models.ImageField(upload_to='signature_images/', null=True, blank=True)

    def __str__(self):
        return str(self.user)


class SocialMedia(models.Model):
    user = models.ForeignKey(User, related_name='social_media', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.title} {self.link}"


class Hobby(models.Model):
    user = models.ForeignKey(User, related_name='hobbies', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Hobby'
        verbose_name_plural = 'Hobbies'

    def __str__(self):
        return f"{self.title}"


# German resume models
class Benutzerprofil(models.Model):

    ALLEINSTEHENND = 1
    VERHEIRATET = 2

    MARITAL_STATUS_CHOICES_DE = [
        (ALLEINSTEHENND, 'Alleinstehend'),
        (VERHEIRATET, 'Verheiratet'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='benutzer_profil')
    user_title = models.CharField(max_length=32, null=True, blank=True)
    first_name_resume = models.CharField(max_length=32, null=True, blank=True)
    last_name_resume = models.CharField(max_length=32, null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='birth', null=True, blank=True)
    marital_status = models.PositiveSmallIntegerField(choices=MARITAL_STATUS_CHOICES_DE, default=ALLEINSTEHENND,
                                                      null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    home_address = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name_resume} {self.last_name_resume}"


class ArbeitsErfahrung(models.Model):

    ARBEITEND = 1
    BEENDET = 2

    WORK_EXPERIENCE_CHOICES_DE = [
        (ARBEITEND, 'Arbeitend'),
        (BEENDET, 'Beendet')
    ]

    user = models.ForeignKey(User, related_name='arbeit_erfahrung', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=WORK_EXPERIENCE_CHOICES_DE, default=ARBEITEND,
                                              null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    company = models.CharField(max_length=64, null=True, blank=True)
    last_position = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.company}"


class Ausbildung(models.Model):

    AKTIV = 1
    BEENDET = 2

    EDUCATION_CHOICES_DE = [
        (AKTIV, 'Aktiv'),
        (BEENDET, 'Beendet')
    ]

    user = models.ForeignKey(User, related_name='ausbildung', on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=EDUCATION_CHOICES_DE, default=AKTIV, null=True, blank=True)
    degree = models.CharField(max_length=32, null=True, blank=True)
    institute = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    average = models.FloatField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.institute} {self.average}"


class Fahigkeiten(models.Model):

    user = models.ForeignKey(User, related_name='fahigkeiten', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True, blank=True)
    level_of_skill = models.CharField(max_length=48, null=True, blank=True, verbose_name='level')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}  {self.level_of_skill}"


class Sprachen(models.Model):

    user = models.ForeignKey(User, related_name='sprachen', on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=True, blank=True)
    level_of_language = models.CharField(max_length=48, null=True, blank=True, verbose_name='level')
    certificate = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}  {self.level_of_language}"


class Projekte(models.Model):

    user = models.ForeignKey(User, related_name='projekte', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}"


class Kurse(models.Model):

    user = models.ForeignKey(User, related_name='kurse', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    period = models.CharField(max_length=48, null=True, blank=True)
    certificate = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.user}: {self.title}  {self.certificate}"


class Kompetenzen(models.Model):  # Quality

    user = models.ForeignKey(User, related_name='kompetenzen', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f" {self.title}"


class Fotos(models.Model):

    user = models.ForeignKey(User, related_name='fotos', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    signature_image = models.ImageField(upload_to='signature_images/', null=True, blank=True)

    def __str__(self):
        return str(self.user)


class SozialMedien(models.Model):

    user = models.ForeignKey(User, related_name='sozial_medien', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}: {self.title} {self.link}"


class HobbyDE(models.Model):

    user = models.ForeignKey(User, related_name='hobbys', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Hobby'
        verbose_name_plural = 'Hobbies'

    def __str__(self):
        return f"{self.title}"
