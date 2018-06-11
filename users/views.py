import datetime
import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string, get_template
from django.template import Context
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from web3.auto import w3
from web3 import Web3, HTTPProvider
import sendgrid
from sendgrid.helpers.mail import *


from .forms import RegisterForm, UserAccountForm
from .tokens import account_activation_token
from .models import User, Subscription


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'signup.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()

        current_site = get_current_site(self.request)
        mail_subject = 'ITO registration'
        to_email = self.object.email
        ctx = {
            'user': self.object,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).decode("utf-8"),
            'token':account_activation_token.make_token(self.object),
        }

        message = get_template('confirm_email.html').render(ctx)

        email = EmailMessage(
             mail_subject, message, to=[to_email]
        )
        email.content_subtype = 'html'
        email.send()

        return HttpResponseRedirect('/thanks/')



class ThanksPageView(TemplateView):

    template_name = "thanks.html"


class CompatibleWalletsView(TemplateView):

    template_name = "compatible_wallets.html"


class HomeView(UpdateView):

    template_name = "home.html"
    form_class = UserAccountForm
    success_url = '/home'
    model = User


    def form_valid(self, form):
        if self.request.user.editable:
            self.request.user.editable = False
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(HomeView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # TODO
        # w3 = Web3(HTTPProvider('https://mainnet.infura.io/'))
        # get_balance = w3.eth.getBalance('0x0')
        # balance = Web3.fromWei(get_balance, 'ether')
        balance = 10

        launched = False
        now = datetime.datetime.now()
        deadline = datetime.datetime(2018, 6, 15, 21, 0, 0)
        if now >= deadline:
            launched = True

        context = super().get_context_data(**kwargs)
        context['launched'] = launched
        context['balance'] = balance
        return context


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account was successfully activated!")
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('Activation link is invalid!')


class SubscriptionCreate(CreateView):
    model = Subscription
    fields = ['email', ]
    template_name = 'index.html'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        current_site = get_current_site(self.request)
        mail_subject = 'newsletter subscription'
        to_email = self.object.email
        ctx = {
            'domain': current_site.domain,
            'token': self.object.activation_code,
        }

        message = get_template('confirm_subscription.html').render(ctx)

        email = EmailMessage(
             mail_subject, message, to=[to_email]
        )
        email.content_subtype = 'html'
        email.send()
        messages.success(self.request, "We've sent a confirmation email to you. Please confirm to activate your subscription. Thanks!")
        return HttpResponseRedirect('/')


def subscribe_activate(request, token):
    try:
        subscription = Subscription.objects.get(activation_code=token)
    except(TypeError, ValueError, OverflowError, Subscription.DoesNotExist):
        subscription = None
    if subscription is not None:
        subscription.active = True
        subscription.save()
        messages.success(request, "Your have successfully subscribed to newsletter!")
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')
