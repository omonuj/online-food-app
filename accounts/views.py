from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from accounts.forms import UserForm
from accounts.models import User


# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists')

            if form.errors:
                return render(request, 'accounts/registerUser.html', {'form': form})

            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()


            try:
                with transaction.atomic():
                    user.save()
                messages.success(request, 'Account created successfully! You can now login. ')
                return redirect('registerUser')
            except IntegrityError:
                form.add_error('username', 'Username already exists')
                return render(request, 'accounts/registerUser.html', {'form': form})
        else:
            print('invalid form submission')
            print(form.errors)
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/registerUser.html', context)
