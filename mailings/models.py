from django.db import models

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О.")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = [
            "full_name",
        ]

    def __str__(self):
        return self.email


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = [
            "subject",
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    CREATED = "Создана"
    RUNNING = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (RUNNING, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    sending_start = models.DateTimeField(
        verbose_name="Дата и время первой отправки", blank=True, null=True
    )
    sending_end = models.DateTimeField(
        verbose_name="Дата и время окончания отправки", blank=True, null=True
    )
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    recipient_list = models.ManyToManyField(Recipient)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = [
            "sending_start",
            "sending_end",
        ]
        permissions = [
            ('can_stop_mailing', 'Can stop mailing'),
        ]

    def __str__(self):
        return f"{self.sending_start} {self.message}"


class MailingTry(models.Model):
    SUCCESS = "Успешно"
    FAILURE = "Не успешно"

    STATUS_CHOICES = [
        (SUCCESS, "Успешно"),
        (FAILURE, "Не успешно"),
    ]

    date_time = models.DateTimeField(verbose_name="Дата и время попытки", auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Статус попытки"
    )
    response = models.TextField(verbose_name="Ответ почтового сервера", blank=True, null=True)
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = [
            "date_time",
        ]

    def __str__(self):
        return f"{self.date_time} {self.status}"
