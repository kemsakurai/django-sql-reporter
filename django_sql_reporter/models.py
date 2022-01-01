from django.db import models
from django.utils import timezone


# Create your models here.
class SQLResultReport(models.Model):
    name = models.CharField(max_length=1000)
    body = models.JSONField()
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    RESULT_STATUS = (
        (0, 'ok'),
        (1, 'ng')
    )
    result_status = models.IntegerField(choices=RESULT_STATUS, default=0)

    SEND_STATUS = (
        (0, 'Todo'),
        (1, 'Doing'),
        (2, 'Done'),
        (9, 'Error'),
    )
    send_status = models.IntegerField(choices=SEND_STATUS, default=0)
