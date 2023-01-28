from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        authenticated_user = authenticate(username=form.cleaned_data['username'],
                                          password=form.cleaned_data['password1'])
        login(self.request, authenticated_user)
        return redirect(self.get_success_url())
