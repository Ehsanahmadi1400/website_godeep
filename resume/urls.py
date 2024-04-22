from django.urls import path

from resume.views import (CustomSignInView, CustomSignUpView, CustomSignOutView, WorkExperienceDeleteView,
                          WorkExperienceModifyView, EducationModifyView, EducationDeleteView, SkillModifyView,
                          LanguageModifyView, ProjectModifyView, CourseModifyView, CompetenceModifyView,
                          ImageModifyView, HobbyModifyView, SocialMediaModifyView, SkillDeleteView, LanguageDeleteView,
                          ProjectDeleteView, CourseDeleteView, ImageDeleteView, SocialMediaDeleteView,
                          CompetenceDeleteView, HobbyDeleteView, UserInfoModifyView, ChangePasswordView,
                          PrintPageView, ArbeitsErfahrungDeleteView, ArbeitsErfahrungModifyView, AusbildungModifyView,
                          FahigkeitenModifyView, SprachenModifyView, ProjekteModifyView, KurseModifyView,
                          AusbildungDeleteView, FahigkeitenDeleteView, SprachenDeleteView, ProjekteDeleteView,
                          KurseDeleteView, FotosModifyView, FotosDeleteView, KompetenzenModifyView,
                          KompetenzenDeleteView, HobbyDEDeleteView, HobbyDEModifyView, SozialMedienModifyView,
                          SozialMedienDeleteView, BenutzerprofilModifyView, PrintPageDEView, ContactMeView)

urlpatterns = [
    # login/ logout urls
    path('sign-in/', CustomSignInView.as_view(), name='sign-in'),
    path('sign-up/', CustomSignUpView.as_view(), name='sign-up'),
    path('sign-out/', CustomSignOutView.as_view(), name='sign-out'),

    # Contact me
    path('contact-m/', ContactMeView.as_view(), name='contact-me'),

    # English resume main URLs
    path('work-experience/', WorkExperienceModifyView.as_view(), name='work-experience'),
    path('education/', EducationModifyView.as_view(), name='education'),
    path('skills/', SkillModifyView.as_view(), name='skills'),
    path('languages/', LanguageModifyView.as_view(), name='languages'),
    path('projects/', ProjectModifyView.as_view(), name='projects'),
    path('courses/', CourseModifyView.as_view(), name='courses'),
    path('images/', ImageModifyView.as_view(), name='images'),
    path('social-media/', SocialMediaModifyView.as_view(), name='social-media'),
    path('competence/', CompetenceModifyView.as_view(), name='qualities'),
    path('hobbies/', HobbyModifyView.as_view(), name='hobbies'),
    path('info/', UserInfoModifyView.as_view(), name='info'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # English resume delete views
    path('work-experience/<int:pk>/delete/', WorkExperienceDeleteView.as_view(), name='work-experience-delete'),
    path('education/<int:pk>/delete/', EducationDeleteView.as_view(), name='education-delete'),
    path('skills/<int:pk>/delete/', SkillDeleteView.as_view(), name='skill-delete'),
    path('languages/<int:pk>/delete/', LanguageDeleteView.as_view(), name='language-delete'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('images/<int:pk>/delete/', ImageDeleteView.as_view(), name='image-delete'),
    path('social-media/<int:pk>/delete/', SocialMediaDeleteView.as_view(), name='social-media-delete'),
    path('competence/<int:pk>/delete/', CompetenceDeleteView.as_view(), name='quality-delete'),
    path('hobbies/<int:pk>/delete/', HobbyDeleteView.as_view(), name='hobby-delete'),

    # German resume main URLs
    path('arbeitserfahrung/', ArbeitsErfahrungModifyView.as_view(), name='arbeitserfahrung'),
    path('ausbildung/', AusbildungModifyView.as_view(), name='ausbildung'),
    path('fahigkeiten/', FahigkeitenModifyView.as_view(), name='fahigkeiten'),
    path('sprachen/', SprachenModifyView.as_view(), name='sprachen'),
    path('projekte/', ProjekteModifyView.as_view(), name='projekte'),
    path('kurse/', KurseModifyView.as_view(), name='kurse'),
    path('fotos/', FotosModifyView.as_view(), name='fotos'),
    path('sozial-medien/', SozialMedienModifyView.as_view(), name='sozial-medien'),
    path('kompetenzen/', KompetenzenModifyView.as_view(), name='kompetenzen'),
    path('hobbys/', HobbyDEModifyView.as_view(), name='hobbys'),
    path('daten/', BenutzerprofilModifyView.as_view(), name='daten'),

    # German resume delete views
    path('arbeitserfahrung/<int:pk>/delete/', ArbeitsErfahrungDeleteView.as_view(), name='arbeitserfahrung-delete'),
    path('ausbildung/<int:pk>/delete/', AusbildungDeleteView.as_view(), name='ausbildung-delete'),
    path('fahigkeiten/<int:pk>/delete/', FahigkeitenDeleteView.as_view(), name='fahigkeiten-delete'),
    path('sprachen/<int:pk>/delete/', SprachenDeleteView.as_view(), name='sprachen-delete'),
    path('projekte/<int:pk>/delete/', ProjekteDeleteView.as_view(), name='projekte-delete'),
    path('kurse/<int:pk>/delete/', KurseDeleteView.as_view(), name='kurse-delete'),
    path('fotos/<int:pk>/delete/', FotosDeleteView.as_view(), name='fotos-delete'),
    path('sozial-medien/<int:pk>/delete/', SozialMedienDeleteView.as_view(), name='sozial-medien-delete'),
    path('kompetenzen/<int:pk>/delete/', KompetenzenDeleteView.as_view(), name='kompetenzen-delete'),
    path('hobbys/<int:pk>/delete/', HobbyDEDeleteView.as_view(), name='hobbys-delete'),

    # pdf output
    path('print/<int:pk>/', PrintPageView.as_view(), name='print-pdf'),
    path('print-de/<int:pk>/', PrintPageDEView.as_view(), name='print-pdf-de')

]
