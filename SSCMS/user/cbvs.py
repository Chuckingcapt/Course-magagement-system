import random

from django.shortcuts import reverse, redirect
from django.views.generic import CreateView, UpdateView

from user.forms import StuRegisterForm, TeaRegisterForm, StuUpdateForm

from user.models import Student, Teacher


class CreateStudentView(CreateView):
    model = Student
    form_class = StuRegisterForm
    template_name = "user/register.html"
    success_url = "login"

    def get_context_data(self, **kwargs):
        context = super(CreateStudentView, self).get_context_data(**kwargs)
        context["kind"] = "student"
        return context

    def form_valid(self, form):
        grade = form.cleaned_data['grade']
        student_set = Student.objects.filter(grade=grade).order_by("-number")
        if student_set.count() > 0:
            last_student = student_set[0]
            new_number = str(int(last_student.number) + 1)
            for i in range(6 - len(new_number)):
                new_number = "0" + new_number
        else:
            new_number = "000001"

        new_student = form.save(commit=False)
        # new_student.grade = grade
        new_student.number = new_number
        new_student.save()

        form.save_m2m()

        self.object = new_student

        uid = grade + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'student'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))


class CreateTeacherView(CreateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/register.html"
    success_url = "login"

    def get_context_data(self, **kwargs):
        context = super(CreateTeacherView, self).get_context_data(**kwargs)
        context["kind"] = "teacher"
        return context

    def form_valid(self, form):
        department_no = random.randint(0, 300)
        department_no = '{:0>3}'.format(department_no)
        teacher_set = Teacher.objects.filter(department_no=department_no).order_by("-number")
        if teacher_set.count() > 0:
            last_teacher = teacher_set[0]
            new_number = str(int(last_teacher.number) + 1)
            new_number = '{:0>7}'.format(new_number)
        else:
            new_number = "0000001"

        new_teacher = form.save(commit=False)
        new_teacher.department_no = department_no
        new_teacher.number = new_number
        new_teacher.save()

        form.save_m2m()

        self.object = new_teacher

        uid = department_no + new_number
        from_url = "register"
        base_url = reverse(self.get_success_url(), kwargs={'kind': 'teacher'})
        return redirect(base_url + '?uid=%s&from_url=%s' % (uid, from_url))


class UpdateStudentView(UpdateView):
    model = Student
    form_class = StuUpdateForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "student"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "student"})


class UpdateTeacherView(UpdateView):
    model = Teacher
    form_class = TeaRegisterForm
    template_name = "user/update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateTeacherView, self).get_context_data(**kwargs)
        context.update(kwargs)
        context["kind"] = "teacher"
        return context

    def get_success_url(self):
        return reverse("course", kwargs={"kind": "teacher"})
