from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Question, UserProfile
from .forms import LoginForm, QuestionForm, CustomUserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('quiz:dashboard')
    else:
        form = LoginForm()
    return render(request, 'quiz/login.html', {'form': form})

@login_required
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    total_tests = 10
    correct_answers = user_profile.liked_questions.count()
    incorrect_answers = total_tests - correct_answers
    perfect_tests = user_profile.liked_questions.filter(likes=total_tests).count()

    success_rate = (correct_answers / total_tests) * 100 if total_tests > 0 else 0

    return render(request, 'quiz/dashboard.html', {
        'user_profile': user_profile,
        'total_tests': total_tests,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'perfect_tests': perfect_tests,
        'success_rate': success_rate
    })
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('quiz/dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'quiz/change_password.html', {'form': form})

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save()
            return redirect('quiz:dashboard')
    else:
        form = QuestionForm()
    return render(request, 'quiz/add_question.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

@login_required
def take_quiz(request):
    questions = Question.objects.order_by('?')[:10]
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        score = 0
        for question in questions:
            selected_answer = request.POST.get(f'question_{question.id}')
            if question.is_correct(selected_answer):
                score += 1
                user_profile.liked_questions.add(question)

        if not request.user.is_authenticated:
            request.session['quiz_score'] = score
        return redirect('quiz:quiz_results')
    return render(request, 'quiz/take_quiz.html', {'questions': questions})

@login_required
def quiz_results(request):
    if not request.user.is_authenticated:
        score = request.session.get('quiz_score', 0)
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        score = user_profile.liked_questions.count()
    return render(request, 'quiz/quiz_results.html', {'score': score})

@login_required
def like_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question not in request.user.userprofile.liked_questions.all():
        question.likes += 1
        question.save()
        request.user.userprofile.liked_questions.add(question)
    return redirect('quiz:take_quiz')

@login_required
def logout_view(request):
    logout(request)
    return redirect('quiz:login')