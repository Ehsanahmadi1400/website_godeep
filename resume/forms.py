from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from resume.models import UserProfile, Skill, WorkExperience, Education, Language, Course, Project, Competence, Hobby, \
    SocialMedia, Image, Benutzerprofil, ArbeitsErfahrung, Ausbildung, Fahigkeiten, Sprachen, Kurse, Projekte, \
    Kompetenzen, Fotos, SozialMedien, HobbyDE


class CustomUserCreationForm(UserCreationForm):
    # Additional fields from UserProfile
    date_of_birth = forms.DateField(label='Date of Birth', help_text='2000-12-21', required=False)
    marital_status = forms.ChoiceField(choices=UserProfile.MARITAL_STATUS_CHOICES, required=False)
    phone_number = forms.CharField(max_length=32, required=False)
    home_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ('username', 'date_of_birth', 'marital_status', 'phone_number', 'home_address',
                  'first_name', 'last_name', 'email', 'password1', 'password2')


class ModifyUserInfoForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Date of Birth', help_text='2000-12-21', required=False)
    marital_status = forms.ChoiceField(choices=UserProfile.MARITAL_STATUS_CHOICES, required=False)
    phone_number = forms.CharField(max_length=32, required=False)
    home_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = UserProfile
        fields = ('first_name_resume', 'last_name_resume', 'date_of_birth', 'marital_status',
                  'phone_number', 'home_address', 'user_title')


class WorkExperienceForm(forms.ModelForm):

    class Meta:
        model = WorkExperience
        fields = ('start_date', 'finish_date', 'status', 'city', 'country', 'company', 'last_position', 'description')


class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = ('start_date', 'finish_date', 'status', 'city', 'country', 'degree', 'institute', 'average',
                  'description')


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ('title', 'level_of_skill', 'description')


class LanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = ('title', 'level_of_language', 'certificate', 'description')


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('title', 'period', 'certificate', 'description')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('title', 'description')


class CompetenceForm(forms.ModelForm):

    class Meta:
        model = Competence
        fields = ('title', 'description')


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('profile_image', 'signature_image')


class SocialMediaForm(forms.ModelForm):

    class Meta:
        model = SocialMedia
        fields = ('title', 'link')


class HobbyForm(forms.ModelForm):

    class Meta:
        model = Hobby
        fields = ('title', 'description')


class BenutzerDatenForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Date of Birth', help_text='2000-12-21', required=False)
    marital_status = forms.ChoiceField(choices=Benutzerprofil.MARITAL_STATUS_CHOICES_DE, required=False)
    phone_number = forms.CharField(max_length=32, required=False)
    home_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Benutzerprofil
        fields = ('first_name_resume', 'last_name_resume', 'date_of_birth', 'marital_status',
                  'phone_number', 'home_address', 'user_title')


class ArbeitsErfahrungForm(forms.ModelForm):

    class Meta:
        model = ArbeitsErfahrung
        fields = ('start_date', 'finish_date', 'status', 'city', 'country', 'company', 'last_position', 'description')


class AusbildungForm(forms.ModelForm):

    class Meta:
        model = Ausbildung
        fields = ('start_date', 'finish_date', 'status', 'city', 'country', 'degree', 'institute', 'average',
                  'description')


class FahigkeitenForm(forms.ModelForm):

    class Meta:
        model = Fahigkeiten
        fields = ('title', 'level_of_skill', 'description')


class SprachenForm(forms.ModelForm):

    class Meta:
        model = Sprachen
        fields = ('title', 'level_of_language', 'certificate', 'description')


class KurseForm(forms.ModelForm):

    class Meta:
        model = Kurse
        fields = ('title', 'period', 'certificate', 'description')


class ProjekteForm(forms.ModelForm):

    class Meta:
        model = Projekte
        fields = ('title', 'description')


class KompetenzenForm(forms.ModelForm):

    class Meta:
        model = Kompetenzen
        fields = ('title', 'description')


class FotosForm(forms.ModelForm):

    class Meta:
        model = Fotos
        fields = ('profile_image', 'signature_image')


class SozialMedienForm(forms.ModelForm):

    class Meta:
        model = SozialMedien
        fields = ('title', 'link')


class HobbyDEForm(forms.ModelForm):

    class Meta:
        model = HobbyDE
        fields = ('title', 'description')
