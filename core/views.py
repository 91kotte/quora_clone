from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


def register_view(request):
    if request.method == 'POST':
        data = request.POST
        email, username = data['email'], data['username']
        password, confirm_password = data['password'], data['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid username or password.")
    return render(request, 'core/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    query = request.GET.get('q', '')
    questions = Question.objects.filter(title__icontains=query).order_by('-created_at') if query else Question.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'questions': questions})

@login_required
def post_question_view(request):
    form = QuestionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data['title'].strip()
            description = form.cleaned_data['description'].strip()

            # Check if a question with same title exists
            duplicate_exists = Question.objects.filter(
                title__iexact=title
            ).exists()
            if duplicate_exists:
                messages.error(request, "A question with this title already exists. Please check before posting.")
                return redirect('home')
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    return render(request, 'core/post_question.html', {'form': form})

def post_answer_from_home_view(request, pk):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=pk)
        text = request.POST.get('text')
        if text:
            Answer.objects.create(question=question, user=request.user, text=text)
    return redirect('home')

@login_required
def question_detail_view(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question).select_related('user').prefetch_related('likes')
    form = AnswerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.user = request.user
        answer.save()
        return redirect('question_detail', pk=pk)
    return render(request, 'core/question_detail.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def like_answer_view(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.id)


@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.user:
        return redirect('home')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        question.title = title
        question.description = description
        question.save()
        return redirect('question_detail', pk=question.pk)
    return render(request, 'core/edit_question.html', {'question': question})


@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user != answer.user:
        return redirect('home')

    if request.method == 'POST':
        text = request.POST.get('text')
        answer.text = text
        answer.save()
        return redirect('question_detail', pk=answer.question.pk)
    return render(request, 'core/edit_answer.html', {'answer': answer})

