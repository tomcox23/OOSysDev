from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class IndexView(generic.ListView):
	template_name = 'Trivia/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):

	#Return the last five published questions (not including those set to be
	#published in the future).
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
		

class DetailView(generic.DetailView):
	model = Question
	template_name = 'Trivia/detail.html'
	
	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())

	
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'Trivia/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
		return render(request, 'Trivia/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('Trivia:results', args=(question.id,)))

		
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
	
class MakeTournament(generic.TemplateView):
    template_name = 'makeTournament.html'

    def get(self, request):
        form = TournamentForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = TournamentForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            tour_name = form.cleaned_data['tour_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            form = TournamentForm()

            response_token = requests.get('https://opentdb.com/api_token.php?command=request')
            geodata_token = response_token.json()
            token = geodata_token['token']
            request_url = str('https://opentdb.com/api.php?amount=10&type=multiple&token=' + token)
            response_questions = requests.get(request_url)
            geodata_questions = response_questions.json()
            
            # clean
            for q in geodata_questions['results']:
                question = 	q['question'].replace(
        "&#039;", "'").replace(
        "&quot;", '"').replace(
        "&eacute;", 'e').replace(
        "&uuml;rer", 'u').replace(
        '&pi;', 'pi')

                question_instance = Question.objects.create(tournament=post, question_text=question)
                choice = Choice.objects.create(question=question_instance, choice_text=q['correct_answer'], correct_answer=True)
                for c in q['incorrect_answers']:
                    choice = Choice.objects.create(question=question_instance, choice_text=c, correct_answer=False)
            # redirect to tournaments once questions and choices have been saved.
            return redirect('Trivia:tournaments')

        args = {'form': form, 'tour_name': tour_name, 'start_date': start_date, 'end_date': end_date}
        return render(request, self.template_name, args)