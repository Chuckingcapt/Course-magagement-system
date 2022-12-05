from django.db import models
import datetime
from user.models import Student, Teacher
from constants import COURSE_STATUS, COURSE_OPERATION


def current_year():
    return datetime.date.today().year


class Course(models.Model):
    credits = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    semesters = [
        ('Autumn', "Fall"),
        ('Spring', "Spring")
    ]

    name = models.CharField(max_length=50, verbose_name="Course name")
    introduction = models.CharField(max_length=250, verbose_name="Introduction")
    credit = models.IntegerField(verbose_name="Credits")
    max_number = models.IntegerField(verbose_name="Max enrollment")
    year = models.IntegerField(verbose_name="Year", default=current_year)
    semester = models.CharField(max_length=20, verbose_name="Semester", choices=semesters)
    status = models.IntegerField(verbose_name="Course status", default=1)
    teacher = models.ForeignKey(Teacher, verbose_name="Course instructor", on_delete=models.CASCADE)

    def get_status_text(self):
        return COURSE_STATUS[self.status]

    def get_op_text(self):
        return COURSE_OPERATION[self.status]

    def get_current_count(self):
        courses = StudentCourse.objects.filter(course=self, with_draw=False)
        return len(courses)

    def get_schedules(self):
        schedules = Schedule.objects.filter(course=self)
        return schedules

    def __str__(self):
        return "%s (%s)" % (self.name, self.teacher.name)


def weekday_choices():
    weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return [(i + 1, weekday[i]) for i in range(7)]


class Schedule(models.Model):
    weekday = models.IntegerField(choices=weekday_choices(), verbose_name="Date")
    start_time = models.TimeField(verbose_name="Course begin at")
    end_time = models.TimeField(verbose_name="Course end at")
    location = models.CharField(max_length=100, verbose_name="Course location")
    remarks = models.CharField(max_length=100, verbose_name="Note", null=True, blank=True)

    start_week = models.IntegerField(verbose_name="Starting week")
    end_week = models.IntegerField(verbose_name="Ending week")

    intervals = [
        (1, "Once every week"),
        (2, "Once every two weeks")
    ]
    week_interval = models.IntegerField(verbose_name="Week intervals", choices=intervals, default=1)

    course = models.ForeignKey(Course, verbose_name="Course name", on_delete=models.CASCADE)

    def __str__(self):
        s = "From week %s to week %s " % (self.start_week, self.end_week)
        if self.week_interval == 2:
            s += "(once every two weeks) "
        s += "on %s %s-%s " % (self.get_weekday_display(), self.start_time.strftime("%H:%M"),
                            self.end_time.strftime("%H:%M"))
        s += "at %s" % self.location
        if self.remarks:
            s += " (Note: %s)" % self.remarks
        return s


class StudentCourse(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    with_draw = models.BooleanField(default=False)
    with_draw_time = models.DateTimeField(default=None, null=True)
    scores = models.IntegerField(verbose_name="Score", null=True)
    comments = models.CharField(max_length=250, verbose_name="Instructor's comment", null=True)

    rates = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    rating = models.IntegerField(verbose_name="Student's rating", choices=rates, null=True,
                                 help_text="5 being the highest, 1 being the lowest.")
    assessment = models.CharField(max_length=250, verbose_name="Student's comment", null=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
