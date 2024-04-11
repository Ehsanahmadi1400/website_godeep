from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, FormView, DeleteView, DetailView


from resume.forms import (CustomUserCreationForm, WorkExperienceForm, EducationForm, LanguageForm, SkillForm,
                          CourseForm, ProjectForm, CompetenceForm, ImageForm, SocialMediaForm, HobbyForm,
                          ModifyUserInfoForm, ArbeitsErfahrungForm, AusbildungForm, FahigkeitenForm, SprachenForm,
                          ProjekteForm, KurseForm, FotosForm, KompetenzenForm, HobbyDEForm, SozialMedienForm,
                          BenutzerDatenForm)
from resume.models import (UserProfile, WorkExperience, Education, Language, Skill, Course, Project, Competence,
                           Image, SocialMedia, Hobby, ArbeitsErfahrung, Ausbildung, Fahigkeiten, Sprachen, Projekte,
                           Kurse, Fotos, Kompetenzen, HobbyDE, SozialMedien, Benutzerprofil)

from utils.pdf_generator import PDFGeneratorEN, PDFGeneratorDE


class HomepageView(TemplateView):
    template_name = 'godeep/homepage.html'


class CustomSignInView(LoginView):
    template_name = 'godeep/sign-in.html'
    authentication_form = AuthenticationForm


class ProfileDetailView(DetailView):
    model = User
    template_name = 'godeep/profile.html'
    context_object_name = 'person'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


class CustomSignOutView(View):

    @staticmethod
    def get(request):
        logout(request)
        return redirect('homepage')


@method_decorator(require_http_methods(["GET", "POST"]), name="dispatch")
class CustomSignUpView(FormView):
    template_name = 'godeep/sign-up.html'
    form_class = CustomUserCreationForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            form.fields[field_name].widget.attrs['class'] = 'form-control'
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()

        UserProfile.objects.create(
            user=instance,
            date_of_birth=form.cleaned_data['date_of_birth'],
            marital_status=form.cleaned_data['marital_status'],
            phone_number=form.cleaned_data['phone_number'],
            home_address=form.cleaned_data['home_address']
        )

        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        print('form is not valid')
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('user-profile')


class BaseModifyView(TemplateView):
    """Base view for handling resume modifications"""

    object_name = None
    form_name = None
    template_name = None
    redirect_url = None
    form_class = None
    model = None
    success_url = reverse_lazy(None)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['person'] = user
        # Retrieve data for the current user
        context[self.object_name] = self.model.objects.filter(user=user)
        context[self.form_name] = self.form_class()  # Add the form to context
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect(self.redirect_url)  # Redirect to the success URL after successful submission
        else:
            # Handle invalid form submission
            context = self.get_context_data()
            context[self.form_name] = form
            return self.render_to_response(context)


# English CV Modifying Classes
class WorkExperienceModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'work_experiences'
    form_name = 'work_experience'
    redirect_url = 'work-experience'
    template_name = 'resume/work-experience.html'
    form_class = WorkExperienceForm
    model = WorkExperience
    success_url = reverse_lazy('work-experience')


class EducationModifyView(BaseModifyView):
    """Display user education experiences"""
    object_name = 'educations'
    form_name = 'education'
    redirect_url = 'education'
    template_name = 'resume/education.html'
    form_class = EducationForm
    model = Education
    success_url = reverse_lazy('education')


class SkillModifyView(BaseModifyView):
    """Display user skills"""
    object_name = 'skills'
    form_name = 'skill'
    redirect_url = 'skills'
    template_name = 'resume/skills.html'
    form_class = SkillForm
    model = Skill
    success_url = reverse_lazy('skills')


class LanguageModifyView(BaseModifyView):
    """Display user languages"""
    object_name = 'languages'
    form_name = 'language'
    redirect_url = 'languages'
    template_name = 'resume/languages.html'
    form_class = LanguageForm
    model = Language
    success_url = reverse_lazy('language')


class ProjectModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'projects'
    form_name = 'project'
    redirect_url = 'projects'
    template_name = 'resume/projects.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('project')


class CourseModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'courses'
    form_name = 'course'
    redirect_url = 'courses'
    template_name = 'resume/courses.html'
    form_class = CourseForm
    model = Course
    success_url = reverse_lazy('courses')


class CompetenceModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'qualities'
    form_name = 'competence'
    redirect_url = 'qualities'
    template_name = 'resume/qualities.html'
    form_class = CompetenceForm
    model = Competence
    success_url = reverse_lazy('qualities')


class ImageModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'images'
    form_name = 'image'
    redirect_url = 'images'
    template_name = 'resume/images.html'
    form_class = ImageForm
    model = Image
    success_url = reverse_lazy('images')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect(self.redirect_url)  # Redirect to the success URL after successful submission
        else:
            # Handle invalid form submission
            context = self.get_context_data()
            context[self.form_name] = form
            return self.render_to_response(context)


class SocialMediaModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'social_medias'
    form_name = 'social_media'
    redirect_url = 'social-media'
    template_name = 'resume/social-media.html'
    form_class = SocialMediaForm
    model = SocialMedia
    success_url = reverse_lazy('social-media')


class HobbyModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'hobbies'
    form_name = 'hobby'
    redirect_url = 'hobbies'
    template_name = 'resume/hobbies.html'
    form_class = HobbyForm
    model = Hobby
    success_url = reverse_lazy('hobbies')


class UserInfoModifyView(TemplateView):
    info_form_class = ModifyUserInfoForm
    template_name = 'resume/information.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        info_form = self.info_form_class(instance=request.user)
        return render(request, self.template_name, {'info_form': info_form})

    def post(self, request):
        info_form = self.info_form_class(request.POST, instance=request.user)

        if info_form.is_valid():
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.date_of_birth = info_form.cleaned_data['date_of_birth']
            user_profile.marital_status = info_form.cleaned_data['marital_status']
            user_profile.phone_number = info_form.cleaned_data['phone_number']
            user_profile.home_address = info_form.cleaned_data['home_address']
            user_profile.first_name_resume = info_form.cleaned_data['first_name_resume']
            user_profile.last_name_resume = info_form.cleaned_data['last_name_resume']
            user_profile.user_title = info_form.cleaned_data['user_title']
            user_profile.save()

            messages.success(request, 'Your information has been updated successfully.')
            return redirect('user-profile')

        else:
            messages.error(request, 'There was an error updating your information. Please try again.')
            return render(request, self.template_name, {'info_form': info_form})


class ChangePasswordView(TemplateView):
    password_form_class = PasswordChangeForm
    template_name = 'godeep/change-password.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        password_form = self.password_form_class(user=request.user)
        return render(request, self.template_name, {'password_form': password_form})

    def post(self, request):
        password_form = self.password_form_class(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important to prevent user from being logged out
            messages.success(request, 'Your password changed successfully.')
            return redirect('user-profile')
        else:
            messages.error(request, 'There was an error updating your information. Please try again.')
            return render(request, self.template_name, {'password_form': password_form})


# English CV deleting Classes
class WorkExperienceDeleteView(DeleteView):

    model = WorkExperience
    success_url = reverse_lazy('work-experience')


class EducationDeleteView(DeleteView):

    model = Education
    success_url = reverse_lazy('education')


class SkillDeleteView(DeleteView):

    model = Skill
    success_url = reverse_lazy('skills')


class LanguageDeleteView(DeleteView):

    model = Language
    success_url = reverse_lazy('languages')


class ProjectDeleteView(DeleteView):

    model = Project
    success_url = reverse_lazy('projects')


class CourseDeleteView(DeleteView):

    model = Course
    success_url = reverse_lazy('courses')


class ImageDeleteView(DeleteView):

    model = Image
    success_url = reverse_lazy('images')


class SocialMediaDeleteView(DeleteView):

    model = SocialMedia
    success_url = reverse_lazy('social-media')


class CompetenceDeleteView(DeleteView):

    model = Competence
    success_url = reverse_lazy('qualities')


class HobbyDeleteView(DeleteView):

    model = Hobby
    success_url = reverse_lazy('hobbies')


class PrintPageView(PDFGeneratorEN):
    # template_name = 'resume/print.html'
    model = UserProfile
    context_object_name = 'person'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get(self, request, *args, **kwargs):
        person = self.get_object()
        pdf = self.generate_pdf(person)
        return pdf


# German CV Modifying Classes
class ArbeitsErfahrungModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'arbeit_erfahrungen'
    form_name = 'arbeit_erfahrung'
    redirect_url = 'arbeitserfahrung'
    template_name = 'resume/arbeitserfahrung.html'
    form_class = ArbeitsErfahrungForm
    model = ArbeitsErfahrung
    success_url = reverse_lazy('arbeitserfahrung')


class AusbildungModifyView(BaseModifyView):
    """Display user education experiences"""
    object_name = 'ausbildungen'
    form_name = 'ausbildung'
    redirect_url = 'ausbildung'
    template_name = 'resume/ausbildung.html'
    form_class = AusbildungForm
    model = Ausbildung
    success_url = reverse_lazy('ausbildung')


class FahigkeitenModifyView(BaseModifyView):
    """Display user skills"""
    object_name = 'fahigkeiten'
    form_name = 'fahigkeit'
    redirect_url = 'fahigkeiten'
    template_name = 'resume/fahigkeiten.html'
    form_class = FahigkeitenForm
    model = Fahigkeiten
    success_url = reverse_lazy('fahigkeiten')


class SprachenModifyView(BaseModifyView):
    """Display user languages"""
    object_name = 'sprachen'
    form_name = 'sprache'
    redirect_url = 'sprachen'
    template_name = 'resume/sprachen.html'
    form_class = SprachenForm
    model = Sprachen
    success_url = reverse_lazy('sprachen')


class ProjekteModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'projekte'
    form_name = 'projekt'
    redirect_url = 'projekte'
    template_name = 'resume/projekte.html'
    form_class = ProjekteForm
    model = Projekte
    success_url = reverse_lazy('projekte')


class KurseModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'kurse'
    form_name = 'kurs'
    redirect_url = 'kurse'
    template_name = 'resume/kurse.html'
    form_class = KurseForm
    model = Kurse
    success_url = reverse_lazy('kurse')


class KompetenzenModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'kompetenzen'
    form_name = 'kompetenz'
    redirect_url = 'kompetenzen'
    template_name = 'resume/kompetenzen.html'
    form_class = KompetenzenForm
    model = Kompetenzen
    success_url = reverse_lazy('kompetenzen')


class FotosModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'fotos'
    form_name = 'foto'
    redirect_url = 'fotos'
    template_name = 'resume/fotos.html'
    form_class = FotosForm
    model = Fotos
    success_url = reverse_lazy('fotos')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect(self.redirect_url)  # Redirect to the success URL after successful submission
        else:
            # Handle invalid form submission
            context = self.get_context_data()
            context[self.form_name] = form
            return self.render_to_response(context)


class SozialMedienModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'sozial_medien'
    form_name = 'sozial_media'
    redirect_url = 'sozial-medien'
    template_name = 'resume/sozial-medien.html'
    form_class = SozialMedienForm
    model = SozialMedien
    success_url = reverse_lazy('sozial-medien')


class HobbyDEModifyView(BaseModifyView):
    """Display user work experience"""
    object_name = 'hobbys'
    form_name = 'hobby'
    redirect_url = 'hobbys'
    template_name = 'resume/hobbys.html'
    form_class = HobbyDEForm
    model = HobbyDE
    success_url = reverse_lazy('hobbys')


class BenutzerprofilModifyView(TemplateView):
    info_form_class = BenutzerDatenForm
    template_name = 'resume/benutzer-daten.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        info_form = self.info_form_class(instance=request.user)
        return render(request, self.template_name, {'info_form': info_form})

    def post(self, request):
        info_form = self.info_form_class(request.POST, instance=request.user)

        if info_form.is_valid():
            user_profile, created = Benutzerprofil.objects.get_or_create(user=request.user)
            user_profile.date_of_birth = info_form.cleaned_data['date_of_birth']
            user_profile.marital_status = info_form.cleaned_data['marital_status']
            user_profile.phone_number = info_form.cleaned_data['phone_number']
            user_profile.home_address = info_form.cleaned_data['home_address']
            user_profile.first_name_resume = info_form.cleaned_data['first_name_resume']
            user_profile.last_name_resume = info_form.cleaned_data['last_name_resume']
            user_profile.user_title = info_form.cleaned_data['user_title']
            user_profile.save()

            messages.success(request, 'Your information has been updated successfully.')
            return redirect('user-profile')

        else:
            messages.error(request, 'There was an error updating your information. Please try again.')
            return render(request, self.template_name, {'info_form': info_form})


# German CV deleting Classes
class ArbeitsErfahrungDeleteView(DeleteView):

    model = ArbeitsErfahrung
    success_url = reverse_lazy('arbeitserfahrung')


class AusbildungDeleteView(DeleteView):

    model = Ausbildung
    success_url = reverse_lazy('ausbildung')


class FahigkeitenDeleteView(DeleteView):

    model = Fahigkeiten
    success_url = reverse_lazy('fahigkeiten')


class SprachenDeleteView(DeleteView):

    model = Sprachen
    success_url = reverse_lazy('sprachen')


class ProjekteDeleteView(DeleteView):

    model = Projekte
    success_url = reverse_lazy('projekte')


class KurseDeleteView(DeleteView):

    model = Kurse
    success_url = reverse_lazy('kurse')


class KompetenzenDeleteView(DeleteView):

    model = Kompetenzen
    success_url = reverse_lazy('kompetenzen')


class FotosDeleteView(DeleteView):

    model = Fotos
    success_url = reverse_lazy('fotos')


class SozialMedienDeleteView(DeleteView):

    model = SozialMedien
    success_url = reverse_lazy('sozial-medien')


class HobbyDEDeleteView(DeleteView):

    model = HobbyDE
    success_url = reverse_lazy('hobbys')


class PrintPageDEView(PDFGeneratorDE):
    # template_name = 'resume/print-de.html'
    model = Benutzerprofil
    context_object_name = 'person'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.benutzer_profil

    def get(self, request, *args, **kwargs):
        person = self.get_object()
        pdf = self.generate_pdf(person)
        return pdf
