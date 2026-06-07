from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm


# ================= Dashboard =================

@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)

    context = {
        "total_tasks": tasks.count(),
        "completed_tasks": tasks.filter(status="completed").count(),
        "in_progress_tasks": tasks.filter(status="in_progress").count(),
        "pending_tasks": tasks.filter(status="pending").count(),
    }

    return render(request, "tasks/dashboard.html", context)


# ================= Task List =================

@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


# ================= Task Detail =================

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    return render(request, "tasks/task_detail.html", {"task": task})


# ================= Create Task =================

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form})


# ================= Update Task =================

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form})


# ================= Delete Task =================

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "tasks/task_confirm_delete.html", {"task": task})


# ================= Register =================

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect("dashboard")

    return render(request, "tasks/register.html")


# ================= Login =================

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "tasks/login.html")


# ================= Logout =================

def logout_view(request):
    logout(request)
    return redirect("login")