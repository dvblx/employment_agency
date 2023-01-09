from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('vacancies', VacanciesView.as_view(), name='vacancies'),
    path('employers', EmployersView.as_view(), name='employers'),
    path('applicants', ApplicantsView.as_view(), name='applicants'),
    path('deals', DealsView.as_view(), name='deals'),
    path('register_apl', RegisterApplicant.as_view(), name='register_apl'),
    path('register_apl2', RegisterApplicant2.as_view(), name='register_apl2'),
    path('register_emp', RegisterEmployer.as_view(), name='register_emp'),
    path('register_emp2', RegisterEmployer2.as_view(), name='register_emp2'),
    path('login_apl', LoginApplicant.as_view(), name='login_apl'),
    path('login_emp', LoginEmployer.as_view(), name='login_emp'),
]
