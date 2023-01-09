from django.db import models
from django.conf import settings


class TypeOfBusiness(models.Model):
    tob_name = models.CharField(max_length=40, verbose_name="Название вида деятельности")

    def __str__(self):
        return self.tob_name


class Professions(models.Model):
    profession_name = models.CharField(max_length=40, verbose_name="Название профессии")

    def __str__(self):
        return self.profession_name


class Qualifications(models.Model):
    qualification_name = models.CharField(max_length=40, verbose_name="Название квалификации")

    def __str__(self):
        return self.qualification_name


class Skills(models.Model):
    skill_name = models.CharField(max_length=40, verbose_name="Название навыка")

    def __str__(self):
        return self.skill_name


class Applicant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    l_name = models.CharField(max_length=15, verbose_name="Фамилия")
    f_name = models.CharField(max_length=15, verbose_name="Имя")
    p_name = models.CharField(max_length=15, verbose_name="Отчество")
    age = models.PositiveIntegerField(verbose_name="Возраст", default=20)
    experience = models.FloatField(verbose_name="Стаж", default=0)
    other_data = models.TextField(verbose_name="Другие данные", blank=True, default="нет")
    photo = models.ImageField(verbose_name="Фотография", null=True, blank=True)

    def __str__(self):
        if self.experience >= 12 and ((self.experience / 12) % 1 == 0):
            return f'{self.l_name}, {str(self.f_name)[0]}. {str(self.p_name)[0]}. Возраст: {self.age}. ' \
                   f'Стаж (лет): {int(self.experience / 12)}. Дополнительная информация: {self.other_data}'
        elif self.experience >= 12:
            return f'{self.l_name}, {str(self.f_name)[0]}. {str(self.p_name)[0]}. Возраст: {self.age}. ' \
                   f'Стаж (лет): {round((self.experience / 12), 1)}. Дополнительная информация: {self.other_data}'
        elif self.experience < 12 and (self.experience % 1 == 0):
            return f'{self.l_name}, {str(self.f_name)[0]}. {str(self.p_name)[0]}. Возраст: {self.age}. ' \
                   f'Стаж (месяцев): {int(self.experience)}. Дополнительная информация: {self.other_data}'
        else:
            return f'{self.l_name}, {str(self.f_name)[0]}. {str(self.p_name)[0]}. Возраст: {self.age}. ' \
                   f'Стаж (месяцев): {self.experience}. Дополнительная информация: {self.other_data}'


class Education(models.Model):
    applicant_id = models.ForeignKey(Applicant, on_delete=models.PROTECT, verbose_name="Соискатель")
    qualification_id = models.ForeignKey(Qualifications, on_delete=models.PROTECT, verbose_name="Квалификация")
    profession_id = models.ForeignKey(Professions, on_delete=models.PROTECT, verbose_name="Профессия")

    def __str__(self):
        return f'{self.applicant_id}, ({self.qualification_id} - {self.profession_id})'


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, verbose_name="Название компании")
    type_of_business = models.ForeignKey(TypeOfBusiness, on_delete=models.PROTECT,
                                         verbose_name="Вид деятельности")
    address = models.CharField(max_length=60, verbose_name="Адрес")
    phone = models.CharField(max_length=11, verbose_name="Номер телефона", blank=True, null=True, default="Не указан")
    other_contact_information = models.CharField(max_length=70, verbose_name="Другие контактные данные", blank=True,
                                                 default="Не указано")

    def __str__(self):
        return f'{self.company_name}. Вид деятельности: {self.type_of_business}' \
               f' Адрес:{self.address} Номер телефона: {self.phone} ' \
               f'Другие контактные данные: {self.other_contact_information}'


class Vacancy(models.Model):
    profession_id = models.ForeignKey(Professions, on_delete=models.PROTECT, verbose_name="Профессия")
    vacancy_about = models.TextField(verbose_name="Описание вакансии", default="", blank=True)
    salary = models.PositiveIntegerField(verbose_name="Зарплата")
    employer_id = models.ForeignKey(Employer, on_delete=models.PROTECT, verbose_name="Работодатель")
    minimum_qualification = models.ForeignKey(Qualifications, on_delete=models.PROTECT,
                                              verbose_name="Минимальная допустимая квалификация")

    def __str__(self):
        return f'Должность: {self.profession_id}. Описание: {self.vacancy_about}. Зарплата: {self.salary}. ' \
               f'Минимальная квалификация: {self.minimum_qualification}. Работодатель: {self.employer_id}.'


class Deals(models.Model):
    applicant_id = models.ForeignKey(Applicant, on_delete=models.PROTECT, verbose_name="Соискатель")
    vacancy_id = models.ForeignKey(Vacancy, on_delete=models.PROTECT, verbose_name="Вакансия")
    comission = models.IntegerField(verbose_name="Комиссионные")

    def __str__(self):
        return f"Соискатель: {self.applicant_id}. {self.vacancy_id}." \
               f" Комиссионные: {self.comission}"


class UserAndHisType(models.Model):
    APPLICANT = "APL"
    EMPLOYER = "EMP"
    MODERATOR = "MDR"
    Type_Choices = [
        (APPLICANT, "Соискатель"),
        (EMPLOYER, "Работодатель"),
        (MODERATOR, "Модератор"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)
    type_of_user = models.CharField(max_length=3, choices=Type_Choices, verbose_name="Тип пользователя",
                                    default=APPLICANT)



