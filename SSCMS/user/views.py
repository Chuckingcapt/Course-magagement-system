from django.shortcuts import render, redirect
from django.http.response import HttpResponse

from constants import INVALID_KIND
from user.forms import StuLoginForm, TeaLoginForm
from user.cbvs import CreateStudentView, CreateTeacherView, UpdateStudentView, UpdateTeacherView
from user.models import Student, Teacher


def home(request):
    return render(request, "user/login_home.html")


def login(request, *args, **kwargs):
    if not kwargs or kwargs.get("kind", "") not in ["student", "teacher"]:
        return HttpResponse(INVALID_KIND)

    kind = kwargs["kind"]
    context = {'kind': kind}

    if request.method == 'POST':
        if kind == "teacher":
            form = TeaLoginForm(data=request.POST)
        else:
            form = StuLoginForm(data=request.POST)

        if form.is_valid():
            uid = form.cleaned_data["uid"]
            if len(uid) != 10:
                form.add_error('uid', 'The length of the account number must be 10.')
            else:
                if kind == "student":
                    grade = uid[:4]
                    number = uid[4:]
                    object_set = Student.objects.filter(grade=grade, number=number)
                else:
                    department_no = uid[:3]
                    number = uid[3:]
                    object_set = Teacher.objects.filter(department_no=department_no, number=number)

                if object_set.count() == 0:
                    form.add_error('uid', 'The account does not exist!')
                else:
                    user = object_set[0]
                    if form.cleaned_data['password'] != user.password:
                        form.add_error('password', 'Incorrect password!')
                    else:
                        request.session['kind'] = kind
                        request.session['user'] = uid
                        request.session['id'] = user.id

                        return redirect("course", kind=kind)

            context['form'] = form
            return render(request, 'user/login_detail.html', context)
        else:
            context['form'] = form
    elif request.method == 'GET':
        if request.GET.get('uid'):
            uid = request.GET.get('uid')
            context['uid'] = uid
            data = {"uid": uid, 'password': '12345678'}
            if kind == "student":
                form = StuLoginForm(data)
            else:
                form = TeaLoginForm(data)
        else:
            if kind == "student":
                form = StuLoginForm()
            else:
                form = TeaLoginForm()

        context['form'] = form
        if request.GET.get('from_url'):
            context['from_url'] = request.GET.get('from_url')

    return render(request, 'user/login_detail.html', context)


def register(request, kind):
    func = None
    if kind == "student":
        func = CreateStudentView.as_view()
    elif kind == "teacher":
        func = CreateTeacherView.as_view()

    if func:
        context = {
            "kind": kind
        }
        return func(request, context=context)
    else:
        return HttpResponse(INVALID_KIND)


def logout(request):
    if request.session.get('kind'):
        del request.session['kind']
    if request.session.get('user'):
        del request.session['user']
    if request.session.get('id'):
        del request.session['id']

    return redirect("login")


def update(request, kind):
    func = None
    if kind == "student":
        func = UpdateStudentView.as_view()
    elif kind == "teacher":
        func = UpdateTeacherView.as_view()
    else:
        return HttpResponse(INVALID_KIND)

    pk = request.session.get("id")
    if pk:
        context = {
            "name": request.session.get("name", ""),
            "kind": request.session.get("kind", "")
        }
        return func(request, pk=pk, context=context)
    return redirect("login")

