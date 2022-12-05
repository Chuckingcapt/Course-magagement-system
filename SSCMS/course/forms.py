from django import forms
from .models import Course, Schedule, StudentCourse


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ['status', 'teacher']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ["course"]


class ScoreForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["student", "course", "scores", "comments"]

    student = forms.CharField(label="student", disabled=True)
    course = forms.CharField(label="course", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['student'] = self.instance.student
        self.initial['course'] = self.instance.course

    def clean_student(self):
        return self.initial['student']

    def clean_course(self):
        return self.initial['course']


class RateForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ["course", "scores", "comments", "rating", "assessment"]

    course = forms.CharField(label="Course", disabled=True)
    scores = forms.IntegerField(label="Score", disabled=True)
    comments = forms.CharField(label="Instructor's evaluation", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['course'] = self.instance.course
        self.initial['scores'] = self.instance.scores
        self.initial['comments'] = self.instance.comments

    def clean_course(self):
        return self.initial['course']

    def clean_scores(self):
        return self.initial['scores']

    def clean_comments(self):
        return self.initial['comments']
