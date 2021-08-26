from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.db import models


class User(AbstractUser):
    is_organisor = models.BooleanField(default=False, verbose_name='Организатор группы')
    is_salesmanager = models.BooleanField(default=False, verbose_name='Менеджер')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.user.username


class SalesManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,
                                     verbose_name='Группа')

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField()

    # phoned = models.BooleanField(default=False)
    # profile_picture = models.ImageField(height_field=100, width_field=100, verbose_name='Аватар', blank=True, null=True)
    # spec_files = models.FileField(blank=True, null=True)

    # @property
    # def full_name(self):
    #     return f'{self.user}'

    def __str__(self):
        return self.full_name


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField()
    sales_manager = models.ForeignKey(SalesManager,
                                      blank=True,
                                      null=True,
                                      on_delete=models.SET_NULL,
                                      verbose_name='Менеджер')
    organisation = models.ForeignKey(UserProfile,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     verbose_name='Группа')
    category = models.ForeignKey("Category",
                                 related_name='clients',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Категория')
    description = models.TextField(default='This description',
                                   blank=True,
                                   null=True,
                                   verbose_name='Описание')
    date_added = models.DateTimeField(auto_now_add=True,
                                      blank=True,
                                      null=True,
                                      verbose_name='Добавление в базу')
    phoned = models.CharField(max_length=100,blank=True, null=True, verbose_name='Дата последнего звонка')

    def upload_path(instance, filename):

        return f'media/uploads/{instance.pk}/detail/{filename}/'

    spec_files = models.FileField(blank=True, null=True, verbose_name='Файл', upload_to=upload_path)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # class Meta:
    #     verbose_name_plural = ""

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название')
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True,
                                     verbose_name='Группа')

    def __str__(self):
        return self.name

    pass


def post_user_created_signal(sender, instance, created, **kwargs):
    print(sender, instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)
