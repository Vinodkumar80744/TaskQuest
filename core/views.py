# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Question, Task, Profile, TaskCompletion
# from .forms import ProfileForm

# from .models import Profile, Task, TaskCompletion

# @login_required
# def home(request):
#     profile, _ = Profile.objects.get_or_create(user=request.user)

#     all_tasks = Task.objects.all()
#     completed_tasks = TaskCompletion.objects.filter(user=request.user, completed=True).values_list('task_id', flat=True)

#     pending = all_tasks.exclude(id__in=completed_tasks)
#     completed = all_tasks.filter(id__in=completed_tasks)

#     total_tasks = all_tasks.count()
#     completed_count = completed.count()

#     progress_percent = 0
#     if total_tasks > 0:
#         progress_percent = int((completed_count / total_tasks) * 100)

#     context = {
#         'profile': profile,
#         'pending_tasks': pending,
#         'completed_tasks': completed,
#         'progress_percent': progress_percent
#     }

#     return render(request, 'core/dashboard.html', context)


# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Validation
#         if not username or not password:
#             messages.error(request, "All fields are required.")
#             return redirect('register')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already taken!")
#             return redirect('register')

#         User.objects.create_user(username=username, password=password)
#         messages.success(request, "Account created successfully! Please login.")
#         return redirect('login')

#     return render(request, 'core/register.html')


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successful!")
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid username or password.")
#             return redirect('login')

#     return render(request, 'core/login.html')


# @login_required
# def quiz_view(request, task_id):
#     task = Task.objects.get(id=task_id)
#     questions = Question.objects.filter(task=task)

#     return render(request, 'core/quiz.html', {
#         'task': task,
#         'questions': questions
#     })

# @login_required
# def quiz_view(request, task_id):
#     task = Task.objects.get(id=task_id)
#     questions = Question.objects.filter(task=task)
#     profile, _ = Profile.objects.get_or_create(user=request.user)

#     # 🔒 CHECK IF ALREADY COMPLETED
#     if TaskCompletion.objects.filter(user=request.user, task=task, completed=True).exists():
#         messages.error(request, "You have already completed this quiz.")
#         return redirect('home')

#     if request.method == 'POST':
#         correct_count = 0
#         total_questions = questions.count()

#         for q in questions:
#             selected = request.POST.get(f'q{q.id}')
#             if selected and int(selected) == q.correct_option:
#                 correct_count += 1

#         earned_points = int((correct_count / total_questions) * task.points)

#         profile.points += earned_points
#         profile.save()

#         TaskCompletion.objects.update_or_create(
#             user=request.user,
#             task=task,
#             defaults={'completed': True}
#         )

#         messages.success(
#             request,
#             f"You scored {correct_count}/{total_questions}! +{earned_points} points 🎉"
#         )
#         return redirect('home')

#     return render(request, 'core/quiz.html', {
#         'task': task,
#         'questions': questions
#     })



# @login_required
# def leaderboard_view(request):
#     top_users = Profile.objects.select_related('user').order_by('-points')[:10]

#     return render(request, 'core/leaderboard.html', {
#         'top_users': top_users
#     })




# def user_logout(request):
#     logout(request)
#     messages.success(request, "Logged out successfully.")
#     return redirect('login')
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Question, Task, Profile, TaskCompletion
from .forms import ProfileForm


# DASHBOARD
@login_required
def home(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    all_tasks = Task.objects.all()
    completed_tasks = TaskCompletion.objects.filter(
        user=request.user, completed=True
    ).values_list('task_id', flat=True)

    pending = all_tasks.exclude(id__in=completed_tasks)
    completed = all_tasks.filter(id__in=completed_tasks)

    total_tasks = all_tasks.count()
    completed_count = completed.count()

    progress_percent = 0
    if total_tasks > 0:
        progress_percent = int((completed_count / total_tasks) * 100)

    context = {
        'profile': profile,
        'pending_tasks': pending,
        'completed_tasks': completed,
        'progress_percent': progress_percent
    }

    return render(request, 'core/dashboard.html', context)


# REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'core/register.html')


#  LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'core/login.html')


#  QUIZ SYSTEM
@login_required
def quiz_view(request, task_id):
    task = Task.objects.get(id=task_id)
    questions = Question.objects.filter(task=task)
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Prevent reattempt
    if TaskCompletion.objects.filter(user=request.user, task=task, completed=True).exists():
        messages.error(request, "You have already completed this quiz.")
        return redirect('home')

    if request.method == 'POST':
        correct_count = 0
        total_questions = questions.count()

        for q in questions:
            selected = request.POST.get(f'q{q.id}')
            if selected and int(selected) == q.correct_option:
                correct_count += 1

        earned_points = int((correct_count / total_questions) * task.points)

        profile.points += earned_points
        profile.save()

        TaskCompletion.objects.update_or_create(
            user=request.user,
            task=task,
            defaults={'completed': True}
        )

        messages.success(
            request,
            f"You scored {correct_count}/{total_questions}! +{earned_points} points 🎉"
        )
        return redirect('home')

    return render(request, 'core/quiz.html', {
        'task': task,
        'questions': questions
    })


#LEADERBOARD
@login_required
def leaderboard_view(request):
    top_users = Profile.objects.select_related('user').order_by('-points')[:10]
    return render(request, 'core/leaderboard.html', {'top_users': top_users})


# PROFILE PAGE
@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    edit_mode = request.GET.get('edit')  # check if edit requested

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    else:
        form = ProfileForm(instance=profile)

    # check if profile already filled
    profile_filled = profile.date_of_birth or profile.phone or profile.institution or profile.bio

    return render(request, 'core/profile.html', {
        'form': form,
        'profile': profile,
        'profile_filled': profile_filled,
        'edit_mode': edit_mode
    })




def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')
