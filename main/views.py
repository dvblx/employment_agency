from django.contrib.auth.views import LoginView
from django.db.models import Q, Sum, Avg
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView
from django.contrib.auth import login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *


class MainPageView(TemplateView):
    template_name = "main/main_page.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id:
            context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context


class RegisterApplicant(CreateView):
    form_class = RegisterUserForm
    template_name = "main/register_apl.html"

    def form_valid(self, form):
        new_user = form.save()
        UserAndHisType.objects.create(user=new_user, type_of_user="APL")
        login(self.request, new_user)
        return redirect('register_apl2')


class RegisterApplicant2(CreateView):
    form_class = ApplicantForm
    template_name = "main/register2.html"

    def form_valid(self, form):
        u = UserAndHisType.objects.get(user=self.request.user)
        Applicant.objects.create(user=u.user, l_name=form.cleaned_data['l_name'], f_name=form.cleaned_data['f_name'],
                                 p_name=form.cleaned_data['p_name'], age=form.cleaned_data['age'],
                                 experience=form.cleaned_data['experience'], other_data=form.cleaned_data['other_data'])
        return redirect('vacancies')


class RegisterEmployer(CreateView):
    form_class = RegisterUserForm
    template_name = "main/register_emp.html"

    def form_valid(self, form):
        new_user = form.save()
        UserAndHisType.objects.create(user=new_user, type_of_user="EMP")
        login(self.request, new_user)
        return redirect('register_emp2')


class RegisterEmployer2(CreateView):
    form_class = EmployerForm
    template_name = "main/register2.html"

    def form_valid(self, form):
        u = UserAndHisType.objects.get(user=self.request.user)
        Employer.objects.create(user=u.user, company_name=form.cleaned_data['company_name'],
                                type_of_business=form.cleaned_data['type_of_business'],
                                address=form.cleaned_data['address'], phone=form.cleaned_data['phone'],
                                other_contact_information=form.cleaned_data['other_contact_information'])
        return redirect('applicants')


class LoginApplicant(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login_apl.html'

    def get_success_url(self):
        u = UserAndHisType.objects.get(user=self.request.user)
        if u.type_of_user == 'APL':
            return reverse_lazy('vacancies')
        logout(self.request)
        return reverse_lazy('login_apl')


class LoginEmployer(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login_emp.html'

    def get_success_url(self):
        u = UserAndHisType.objects.get(user=self.request.user)
        if u.type_of_user == 'EMP':
            return reverse_lazy('applicants')
        return reverse_lazy('login_emp')


class VacanciesView(ListView):
    model = Vacancy
    template_name = "main/vacancies.html"
    context_object_name = 'queryset'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Employer.objects.all()
        context['qualifications'] = Qualifications.objects.all()
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        search_employer = self.request.GET.getlist("organization")
        search_qual = self.request.GET.getlist("qualification")
        select_order_type = self.request.GET.get("sort")
        queryset = Vacancy.objects.all()

        if search_employer:
            queryset = queryset.filter(
                Q(employer_id__company_name__in=search_employer)
            )
        if search_qual:
            queryset = queryset.filter(
                Q(minimum_qualification__qualification_name__in=search_qual)
            )
        if select_order_type:
            if select_order_type == "asc":
                queryset = queryset.order_by('salary')
            elif select_order_type == "desc":
                queryset = queryset.order_by('-salary')

        return queryset


class ApplicantsView(ListView):
    model = Education
    template_name = "main/applicants.html"
    context_object_name = 'queryset'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professions'] = Professions.objects.all()
        context['qualifications'] = Qualifications.objects.all()
        context['applicant'] = Applicant.objects.all()
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        search_query_other_data = self.request.GET.get('search', '')
        search_query_profession = self.request.GET.getlist("profession")
        search_query_qualification = self.request.GET.getlist("qualification")
        search_query_min_exp = self.request.GET.get('months', '')
        try:
            search_query_min_exp = int(search_query_min_exp)
        except ValueError:
            search_query_min_exp = ''
        queryset = Education.objects.all()
        if search_query_other_data:
            queryset = queryset.filter(Q(applicant_id__other_data__icontains=search_query_other_data))
        if search_query_profession:
            queryset = queryset.filter(Q(profession_id__profession_name__in=search_query_profession))
        if search_query_qualification:
            queryset = queryset.filter(Q(qualification_id__qualification_name__in=search_query_qualification))
        if search_query_min_exp:
            queryset = queryset.filter(Q(applicant_id__experience__gt=search_query_min_exp))
        result = {}
        for apl in queryset:
            result[apl.applicant_id] = []
        for q in Education.objects.all():
            if q.applicant_id in result.keys():
                result[q.applicant_id].append(f'{str(q.qualification_id)}: {str(q.profession_id)}')
        queryset = result
        return queryset


class EmployersView(ListView):
    model = Employer
    template_name = "main/employers.html"
    context_object_name = 'queryset'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_of_business'] = TypeOfBusiness.objects.all()
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        queryset = Employer.objects.all()
        search_company_name = self.request.GET.get('search', '')
        search_type_of_business = self.request.GET.get('business')
        if search_company_name:
            queryset = queryset.filter(Q(company_name__icontains=search_company_name))
        if search_type_of_business:
            queryset = queryset.filter(Q(type_of_business__tob_name__icontains=search_type_of_business))
        return queryset


class DealsView(ListView):
    model = Deals
    template_name = "main/deals.html"
    context_object_name = 'queryset'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if len(self.get_queryset()) > 0:
            context['comission_agg'] = self.get_queryset().aggregate(Sum('comission'), Avg('comission'))
        else:
            context['comission_agg'] = False
        context['employers'] = Employer.objects.all()
        context['vacancies'] = Vacancy.objects.all()
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        search_query1 = self.request.GET.get('employer')
        search_query2 = self.request.GET.get('vacancy')
        search_query3 = self.request.GET.get('search3', '')
        queryset = Deals.objects.all()
        if search_query1:
            queryset = queryset.filter(
                Q(vacancy_id__employer_id__company_name__icontains=search_query1)
            )
        if search_query2:
            queryset = queryset.filter(
                Q(vacancy_id__profession_id__profession_name__icontains=search_query2)
            )
        if search_query3:
            queryset = queryset.filter(
                Q(applicant_id__l_name__icontains=search_query3) |
                Q(applicant_id__f_name__icontains=search_query3) |
                Q(applicant_id__p_name__icontains=search_query3) |
                Q(applicant_id__other_data__icontains=search_query3)
            )
        return queryset


class OneApplicantView(DetailView):
    template_name = "main/one_applicant.html"
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apl'] = Applicant.objects.get(user=self.request.user)
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        context['education'] = Education.objects.filter(applicant_id=context['apl'])
        context['summaries'] = Summary.objects.filter(applicant=context['apl'])
        return context


class OneApplicantSummariesView(ListView):
    template_name = "main/one_applicant_summaries.html"
    model = Summary
    context_object_name = 'queryset'

    def get_queryset(self):
        applicant = Applicant.objects.get(user=self.request.user)
        queryset = Summary.objects.filter(applicant=applicant)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apl'] = Applicant.objects.get(user=self.request.user)
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context


class OneSummaryView(DetailView):
    template_name = "main/one_summary.html"
    model = Summary

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context


class OneEmployerView(DetailView):
    template_name = "main/one_employer.html"
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emp'] = Employer.objects.get(user=self.request.user)
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        context['vacancies'] = Vacancy.objects.filter(employer_id=context['emp'])
        return context


class OneEmployerVacanciesView(ListView):
    template_name = "main/one_employer_vacancies.html"
    model = Vacancy
    context_object_name = 'queryset'

    def get_queryset(self):
        employer = Employer.objects.get(user=self.request.user)
        queryset = Vacancy.objects.filter(employer_id=employer)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['emp'] = Employer.objects.get(user=self.request.user)
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context


class OneVacancyView(DetailView):
    template_name = "main/one_vacancy.html"
    model = Vacancy

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = UserAndHisType.objects.get(user=self.request.user)
        return context


class AddSummaryView(CreateView):
    form_class = SummaryForm
    template_name = 'main/add_summary.html'

    def form_valid(self, form):
        apl = Applicant.objects.get(user=self.request.user)
        Summary.objects.create(applicant=apl, desired_position=form.cleaned_data['desired_position'],
                               skills=form.cleaned_data['skills'],
                               information_about_yourself=form.cleaned_data['information_about_yourself'],
                               work_experience_information=form.cleaned_data['work_experience_information'],
                               education=form.cleaned_data['education'])
        return redirect('o_a_summaries')


class AddVacancyView(CreateView):
    form_class = VacancyForm
    template_name = 'main/add_vacancy.html'

    def form_valid(self, form):
        emp = Employer.objects.get(user=self.request.user)
        Vacancy.objects.create(profession_id=form.cleaned_data['profession_id'],
                               vacancy_about=form.cleaned_data['vacancy_about'], salary=form.cleaned_data['salary'],
                               employer_id=emp, minimum_qualification=form.cleaned_data['minimum_qualification'])
        return redirect('o_e_vacancies')
