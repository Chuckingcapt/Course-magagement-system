from django import forms
from user.models import Student, Teacher


class StuLoginForm(forms.Form):
    uid = forms.CharField(label='Student ID', max_length=10)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)


class TeaLoginForm(forms.Form):
    uid = forms.CharField(label='Teacher ID', max_length=10)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)


class StuRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm your password', widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ('grade', 'name', 'password', 'confirm_password',
                  'gender', 'birthday', 'email', 'info')

    def clean(self):
        clean_data = super(StuRegisterForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match!')

        return clean_data


class TeaRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm your password', widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('name', 'password', 'confirm_password',
                  'gender', 'birthday', 'email', 'info')

    def clean(self):
        clean_data = super(TeaRegisterForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match!')

        return clean_data


class StuUpdateForm(StuRegisterForm):
    class Meta:
        model = Student
        fields = ('name', 'password', 'confirm_password', 'gender', 'birthday', 'email', 'info')
