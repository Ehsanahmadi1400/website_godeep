from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from resume.models import (UserProfile, SocialMedia, WorkExperience, Education, Skill,
                           Language, Course, Competence, Project, Image, Hobby, ArbeitsErfahrung, Ausbildung)


class SocialMediaInline(admin.StackedInline):
    model = SocialMedia
    extra = 1


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, ImageInline, SocialMediaInline)
    list_display_links = ["first_name"]
    list_display = ["id", "username", "email", "first_name", "last_name"]


# Register User with the new CustomUserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'finish_date', 'status', 'city',
                    'company', 'last_position', 'description']


@register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'finish_date', 'status', 'degree',
                    'institute', 'city', 'country', 'average', 'description']


@register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'level_of_skill', 'description']


@register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'level_of_language', 'certificate', 'description']


@register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'period', 'certificate', 'description']


@register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description']


@register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description']


@register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_image', 'signature_image']


@register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'link']


@register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description']


@register(ArbeitsErfahrung)
class ArbeitsErfahrungAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'finish_date', 'status', 'city',
                    'company', 'last_position', 'description']


@register(Ausbildung)
class AusbildungAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'finish_date', 'status', 'degree',
                    'institute', 'city', 'country', 'average', 'description']


# Add another German models in case
