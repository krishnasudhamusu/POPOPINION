from django.shortcuts import render, Http404, get_object_or_404, HttpResponseRedirect, redirect
from .models import Question, Choice, Comment, Likee
from profiles.models import Profile
from django.urls import reverse
from django.http import JsonResponse
from .forms import *
from django.utils import timezone
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

@login_required
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question Does Not Exist')
    return render(request, 'polls/delete.html', {'question': question})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    new_results = question.get_results_dict()
    return render(request, 'polls/results.html', {'question': question, 'new_results': new_results})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choicer'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/index.html',
                      {'question': question, 'error_message': 'You Didnt Select a Choice', })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text: i.votes})

    return JsonResponse(votedata, safe=False)

@login_required
def addpoll(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    userr = Profile.objects.get(user=request.user)
    p_form = PollForm()
    comment_form = CommentModelForm()
    poll_added = False
    if 'submit_p_form' in request.POST:
        p_form = PollForm(request.POST)
        if p_form.is_valid():
            new_poll = p_form.save(commit=False)
            new_poll.pub_date = timezone.now()
            new_poll.author = userr
            new_poll.save()
            new_choice1 = Choice(question_text=new_poll, choice_text=p_form.cleaned_data['choice1']).save()
            new_choice2 = Choice(question_text=new_poll, choice_text=p_form.cleaned_data['choice2']).save()
            new_choice3 = Choice(question_text=new_poll, choice_text=p_form.cleaned_data['choice3']).save()
            poll_added = True
            p_form = PollForm()

    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = userr
            new_comment.question_text = Question.objects.get(id=request.POST.get('poll_id'))
            new_comment.save()
            comment_form = CommentModelForm()

    context = {'latest_question_list': latest_question_list, 'userr': userr, 'p_form': p_form,
               'comment_form': comment_form, 'poll_added': poll_added}
    return render(request, 'polls/index.html', context)

@login_required
def vote_poll(request):
    user = request.user
    if request.method == 'POST':
        ques = get_object_or_404(Question, id=request.POST.get('poll_id'))
        userr = Profile.objects.get(user=user)
        if userr not in ques.voted_users.all():
            try:
                selected_choice = ques.choice_set.get(pk=request.POST['choicer'])
            except (KeyError, Choice.DoesNotExist):
                return render(request, 'polls/index.html',
                              {'ques': ques, 'error_message': 'You Didnt Select a Choice', })
            else:
                selected_choice.votes += 1
                selected_choice.save()
                ques.value = True
                ques.voted_users.add(userr)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('polls:index')

@login_required
def like_unlike_poll(request):
    user = request.user
    if request.method == 'POST':
        poll_id = request.POST.get('poll_id')
        poll_question = Question.objects.get(id=poll_id)
        userr = Profile.objects.get(user=user)

        if userr in poll_question.liked.all():
            poll_question.liked.remove(userr)
        else:
            poll_question.liked.add(userr)

        like, created = Likee.objects.get_or_create(user=userr, question_text_id=poll_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        else:
            like.value = 'Like'

            poll_question.save()
            like.save()

        data = {
            'value': like.value,
            'likes': poll_question.liked.all().count()
        }
        return JsonResponse(data, safe=False)

    return redirect('polls:index')


class PollDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'polls/delete.html'
    success_url = reverse_lazy('polls:index')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Question.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You are not author of the post, You cant delete')

        return obj


class PollUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = PollForm
    template_name = 'polls/update.html'
    success_url = reverse_lazy('polls:index')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not author of the post, You cant update')
            return super().form_invalid(form)
