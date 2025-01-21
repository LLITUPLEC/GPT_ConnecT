from django.db import models
from django.contrib.auth.models import User
from BS.models import Bs_depowner, Bs_department, Bs_position
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    third_name = models.CharField('Отчество', max_length=150, blank=True)
    d_birthday = models.DateField('Дата рождения', null=True, blank=True)
    d_hiring = models.DateField('Дата приёма', null=True, blank=True)
    d_dismissal = models.DateField('Дата увольнения', null=True, blank=True)
    s_create_user = models.CharField('Создатель', max_length=25, null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    iddepowner = models.ForeignKey(Bs_depowner, on_delete=models.CASCADE, verbose_name='Филиал', null=True, blank=True)
    iddepartment = models.ForeignKey(Bs_department, on_delete=models.CASCADE, verbose_name='Подразделение', null=True, blank=True)
    idposition = models.ForeignKey(Bs_position, on_delete=models.CASCADE, verbose_name='Должность', null=True, blank=True)
    chairman = models.BooleanField('Является председателем', default=False)
    member_kmo = models.BooleanField('Является членом комиссии', default=False)

    def __str__(self):
        return str(self.idposition) + ' | ' + str(self.get_fio())

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.third_name)
        return full_name.strip()

    def get_fio(self):
        fio = "%s %s %s" % (str(self.first_name)[:1] + '.', str(self.third_name)[:1] + '.', self.last_name)
        return fio.strip()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

