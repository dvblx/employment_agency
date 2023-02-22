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
    path('applicant/<int:pk>', OneApplicantView.as_view(), name='one_applicant'),
    path('employer/<int:pk>', OneEmployerView.as_view(), name='one_employer'),
    path('employer/vacancies/<int:pk>', OneVacancyView.as_view(), name='one_vacancy'),
    path('applicant/summaries/<int:pk>', OneSummaryView.as_view(), name='one_summary'),
    path('create_vacancy', AddVacancyView.as_view(), name='create_vacancy'),
    path('create_summary', AddSummaryView.as_view(), name='create_summary'),
    path('applicant/summaries', OneApplicantSummariesView.as_view(), name='o_a_summaries'),
    path('employer/vacancies', OneEmployerVacanciesView.as_view(), name='o_e_vacancies'),
]
