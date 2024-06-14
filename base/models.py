from django.db import models
from django.contrib.auth.models import AbstractUser

class Korisnik(AbstractUser):
    ROLES = (('prof', 'profesor'), ('stu', 'student'),('adm', 'admin'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50,choices=ROLES,default='stu')
    status = models.CharField(blank=True,max_length=50,choices=STATUS,default='red')

    class Meta:
        verbose_name_plural = 'Korisnici'

    def save(self,*args,**kwargs):
        if self.role == 'adm':
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)

class Predmet(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    ime = models.CharField(max_length=50)
    kod = models.CharField(max_length=50) 
    program = models.CharField(max_length=50)
    bodovi = models.IntegerField()
    sem_redovni = models.IntegerField()
    sem_izvanredni = models.IntegerField()
    izborni = models.CharField(max_length=50,choices=IZBORNI)
    korisnik_id = models.ForeignKey(Korisnik, on_delete=models.CASCADE,null=True, default=None)

    class Meta:
        verbose_name_plural = 'Predmeti'

    def __str__(self):
        return f"{self.ime} {self.kod} {self.program} {self.bodovi} {self.izborni} {self.korisnik_id}"
    
class Upis(models.Model):
    STATUS = (('izg', 'Izgubljen potpis'), ('potne', 'Potpisan, nije položen'),('pol', 'Položen'))
    korisnik_id = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet_id = models.ForeignKey(Predmet, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=STATUS,default='potne')

    class Meta:
        verbose_name_plural = 'Upisi'

    def __str__(self):
        return f"{self.korisnik_id} {self.predmet_id} {self.status}"