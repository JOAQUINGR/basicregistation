from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormView
from djangoautexample import settings
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Create your views here.


@login_required
def profile(request):
    print(request.user)
    # if isinstance(request.user, AnonymousUser):
    #     return HttpResponse("user dont exist")
    return HttpResponse(
        'welcome user {} <a href="/logout">logout</a>'.format(request.user)
    )


class Registerform(forms.Form):

    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField(min_length=0)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean_password_confirm(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise ValidationError("The passwords dont mach")


class RegisterView(FormView):
    template_name = "authn/register.html"
    form_class = Registerform
    # TODO poner esto bien
    success_url = "/thanks"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        try:
            register_new_user(form, self.request)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        except IntegrityError as e:
            print(
                "Invalid {} credentials while registering a user. Try again!".format(e)
            )
            return HttpResponseRedirect(
                "check your mail you have there the confirmation"
            )


def register_new_user(form, request):

    user_exists = User.objects.filter(email=form.cleaned_data["email"])
    print(user_exists, "ESTOY AQUI JODERRRRR")
    if user_exists.exists():
        user_exists.first().email_user(
            "?check it", "ey , someone tried to register your accounts"
        )
        return IntegrityError(
            "the email {} already exists".format(form.cleaned_data["email"])
        )
    else:
        new_user_created = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
        )
        login(request, new_user_created)
