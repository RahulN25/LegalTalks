from .forms import QuestionForm
def question_post_form(request):
    question_form = QuestionForm()
    return {'question_form': question_form}