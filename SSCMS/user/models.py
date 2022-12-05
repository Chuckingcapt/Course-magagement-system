from django.db import models

genders = [
    ('m', 'Male'),
    ('f', 'Female')
]


class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="Gender")
    birthday = models.DateField(verbose_name="Birthday")
    email = models.EmailField(verbose_name="Email")
    info = models.CharField(max_length=255, verbose_name="Personal Info",
                            help_text="Introduce yourself in one sentence :)")
    grade = models.CharField(max_length=4, verbose_name="School Year")
    number = models.CharField(max_length=6, verbose_name="ID in School Year")
    password = models.CharField(max_length=30, verbose_name="Password")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['grade', 'number'], name='student_id')
        ]

    def get_id(self):
        return "%s%s" % (self.grade, self.number)

    def __str__(self):
        return "%s (%s)" % (self.get_id(), self.name)


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    gender = models.CharField(max_length=10, choices=genders, default='m', verbose_name="Gender")
    birthday = models.DateField(verbose_name="Birthday")
    email = models.EmailField(verbose_name="Email")
    info = models.CharField(max_length=255, verbose_name="Personal Info",
                            help_text="Introduce yourself in one sentence :)")
    department_no = models.CharField(max_length=3, verbose_name="Department Number")
    number = models.CharField(max_length=7, verbose_name="ID in Department")
    password = models.CharField(max_length=30, verbose_name="Password")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department_no', 'number'], name='teacher_id')
        ]

    def get_id(self):
        return "%s%s" % (self.department_no, self.number)

    def __str__(self):
        return "%s (%s)" % (self.get_id(), self.name)
