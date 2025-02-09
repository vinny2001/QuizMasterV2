from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as login_process
from django.contrib.auth import logout

from QuizMaster.forms import StudyForm
from QuizMaster.models import StudySet
from QuizMaster.models import Questions
from QuizMaster.forms import TermForm


# from .forms import RegisterUserForm

# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login_process(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login_process(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# login required after this point
@login_required(login_url="login")
def create_study_set(request):
    if request.method == 'POST':
        form = StudyForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
    else:
        form = StudyForm()
    return render(request, 'create_study_set.html', {'form': form})


@login_required(login_url="login")
def index(request):
    names = StudySet.objects.filter(user=request.user)
    context = {'names': names}
    return render(request, 'index.html', context)


@login_required(login_url="login")
def update_study_set(request, study_set_id):
    name = StudySet.objects.get(id=study_set_id, user=request.user)
    if request.method == 'POST':
        form = StudyForm(request.POST, request.FILES, instance=name)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('index')
    else:
        form = StudyForm(instance=name)
    return render(request, 'update_study_set.html', {'form': form})


@login_required(login_url="login")
def delete_study_set(request, study_set_id):
    task = StudySet.objects.get(id=study_set_id)
    task.delete()
    return redirect('index')


@login_required(login_url="login")
def add(request, study_set_id):
    name = StudySet.objects.get(id=study_set_id)
    form = TermForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            form.instance.study_set = name
            form.instance.user = request.user
            form.save()
            return redirect('add_term', name.id)
    terms = Questions.objects.filter(study_set=name)
    return render(request, 'term_and_definition.html', {'form': form, 'name': name, 'terms': terms})


def logout_view(request):
    logout(request)
    return redirect('home')

