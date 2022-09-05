# Balance - In CRUD views add the handling for DoesNotExist
from django.shortcuts import render, redirect
from .models import Question, Answer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
)
from .forms import QuestionForm, AnswerForm
from operator import itemgetter
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def home(request):
    try:
        if request.session['category'] and request.user.is_authenticated:
            pending_question = Question(
                question_title=request.session['question_title'],
                question_body=request.session['question_body'],
                is_anonymous=request.session['as_anonymous'],
                category=request.session['category'],
                author=request.user
            )
            new_question = pending_question.save()
            request.session.pop('as_anonymous', None)
            request.session.pop('category', None)
            request.session.pop('question_title', None)
            request.session.pop('question_body', None)
            request.session.modified = True
            messages.success(request, f'Your Query has been posted {new_question.author.first_name}!')
            return redirect(new_question.get_absolute_url())
    except KeyError:
        questions = []
        for q in Question.objects.all():
            answer_count = len(q.answer_set.all())
            votes = q.votes()
            question_category = q.get_category_display()
            questions.append((q, answer_count, votes, question_category))
        context = {
            'questions': questions,
        }
        return render(request, 'forum/home.html', context)

def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                new_question = form.save(request.user)
                messages.success(request, f'Your Query has been posted {new_question.author.first_name}!')
                return redirect(new_question.get_absolute_url())
            request.session['as_anonymous'] = form.cleaned_data.get('is_anonymous')
            request.session['category'] = form.cleaned_data.get('category')
            request.session['question_title'] = form.cleaned_data.get('question_title')
            request.session['question_body'] = form.cleaned_data.get('question_body')
            return redirect('account:login')
    return redirect('home')


@login_required
def edit_question(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_id)
        edit_question_form = QuestionForm(request.POST, instance=question)
        if edit_question_form.is_valid():
            edit_question_form.save()
            messages.success(request, 'Your Question was updated Successfully!')
            return redirect(question.get_absolute_url())
        messages.error(request, 'Failed to save edits to your Question')
        return redirect(question.get_absolute_url())
    return redirect('home')

def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_form.save(usr=request.user, ques=question)
            messages.success(request, 'Your Answer was successfully added to this Question!')
            return redirect(question.get_absolute_url())
        messages.error(request, 'An error occured while adding your answer to this question.')
        return redirect(question.get_absolute_url())
    question_edit_form = QuestionForm(instance=question)
    votes = question.votes()
    answer_count = len(question.answer_set.all())
    answer_form = AnswerForm()
    context = {
        'question': question,
        'question_edit_form': question_edit_form,
        'votes': votes,
        'answer_count': answer_count,
        'answer_form': answer_form,
    }
    return render(request, 'forum/question.html', context)

def question_delete(request, question_id):
    if request.method == 'POST':
        Question.objects.get(pk=question_id).delete()
        messages.success(request, 'Your Question Was Deleted Successfully!')
        return redirect('home')
    return redirect('home')

""" class HomeQuestionListView(ListView):
    model = Question
    template_name = 'forum/home.html'
    context_object_name = 'question'
    ordering = ['-date_asked'] """

def edit_answer(request, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_id)
        anonymity = request.POST.get('answer_anonymity', False)
        if anonymity == 'on':
            anonymity = True
        else:
            anonymity = False
        answer.is_anonymous = anonymity
        answer.answer_body = request.POST['edit_question_body']
        answer.save()
        messages.success(request, 'Your Answer Has Been Edited Successfully')
        question = answer.answer_for
        return redirect(question.get_absolute_url())
    return redirect('home')

def delete_answer(request, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_id)
        question = answer.answer_for
        answer.delete()
        messages.success(request, 'Your Answer Has Been Deleted Successfully')
        return redirect(question.get_absolute_url())
    else:
        redirect('home')

@login_required
def your_content(request):
    user = request.user
    your_content = []
    if user.is_advocate:
        for q in user.questions.all():
            question = q, q.date_asked, "q"
            your_content.append(question)
        for a in user.answers.all():
            answer = a, a.date_answered, "a"
            your_content.append(answer)
        your_content.sort(key=itemgetter(1), reverse=True)
    else:
        for q in user.questions.all():
            question = q, q.date_asked, "q"
            your_content.append(question)
        your_content.sort(key=itemgetter(1), reverse=True)
    return render(request, 'forum/yourContent.html', {'your_content': your_content})


def search(request):
    keywords = request.GET.get("search", False)
    if keywords:
        keywords = keywords.split()
        results = []
        # Tests whether the search returned at least one result
        found = False
        for question in Question.objects.all():
            question_text = question.question_title + question.question_body
            question_text =  question_text.casefold()
            # Tests whether at least one keyword matches
            # And used to determine whether to include the current question
            matched = False
            degree = 0
            for keyword in keywords:
                if keyword.casefold() in question_text:
                    if not matched:
                        matched = True
                        found = True
                    degree += 1
            if matched:
                results.append((question, degree))
        if not found:
            results = False
        else:
            results.sort(key=itemgetter(1), reverse=True)
        context = {
            'results': results,
            'keywords': keywords,
        }
        return render(request, 'forum/search.html', context)
    else:
        return render(request, 'forum/search.html', {})

def anonymous(request):
    return render(request, 'forum/anonymous.html', {})

@csrf_exempt
def vote(request):
    if request.method == 'POST' and request.user.is_authenticated:
        act = {}
        act[0] = request.POST.get("0")
        act[1] = request.POST.get("1")
        forum_obj = request.POST.get("forum_obj")
        # Check whether it is the question or answer which is being interacted
        if forum_obj == "q":
            q_id = int(request.POST.get("question"))
            obj = Question.objects.get(id=q_id)
        else:
            obj = Answer.objects.get(id=int(forum_obj))
        print(act)
        print(obj)
        # Check which button was pressed
        if act[0] == "up":
            if act[1] == "add_upvote":
                if request.user in obj.downvotes.all():
                    obj.downvotes.remove(request.user)
                obj.upvotes.add(request.user)
            else:
                obj.upvotes.remove(request.user)
            obj.save()
        else:
            if act[1] == "add_downvote":
                if request.user in obj.upvotes.all():
                    obj.upvotes.remove(request.user)
                obj.downvotes.add(request.user)
            else:
                obj.downvotes.remove(request.user)
            obj.save()
        obj.refresh_from_db()
        return JsonResponse({"votes": obj.votes()})
    return JsonResponse({"login": "/account/login/"})
    # return JsonResponse({"success": "Succeeded Successfully!"})