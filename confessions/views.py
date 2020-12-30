from django.shortcuts import render, redirect
from .models import Confession, Like
from profiles.models import Profile
from .forms import ConfessionModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
@login_required
def confession_comment_create_list_view(request):
    qs = Confession.objects.all()
    profile = Profile.objects.get(user=request.user)

    c_form = ConfessionModelForm()
    comment_form = CommentModelForm()
    confession_added = False

    if 'submit_c_form' in request.POST:
        c_form = ConfessionModelForm(request.POST, request.FILES)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.author = profile
            instance.save()
            c_form = ConfessionModelForm()
            confession_added = True

    if 'submit_comment_form' in request.POST:
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.user = profile
            instance.confession = Confession.objects.get(id=request.POST.get('confession_id'))
            instance.save()
            comment_form = CommentModelForm()

    context = {
        'qs': qs,
        'profile': profile,
        'c_form': c_form,
        'comment_form': comment_form,
        'confession_added': confession_added,
    }
    return render(request, 'confessions/main.html', context)

@login_required
def like_unlike_confession(request):
    user = request.user
    if request.method == 'POST':
        confession_id = request.POST.get('confession_id')
        confession_obj = Confession.objects.get(id=confession_id)
        profile = Profile.objects.get(user=user)

        if profile in confession_obj.liked.all():
            confession_obj.liked.remove(profile)
        else:
            confession_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, confession_id=confession_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        else:
            like.value = 'Like'

            confession_obj.save()
            like.save()

        data = {
            'value': like.value,
            'likes': confession_obj.liked.all().count()
        }
        return JsonResponse(data, safe=False)

    return redirect('confessions:main-confession-view')


class ConfessionDeleteView(LoginRequiredMixin,DeleteView):
    model = Confession
    template_name = 'confessions/confirm_delete.html'
    success_url = reverse_lazy('confessions:main-confession-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Confession.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You are not author of the post, You cant delete')

        return obj


class ConfessionUpdateView(LoginRequiredMixin,UpdateView):
    model = Confession
    form_class = ConfessionModelForm
    template_name = 'confessions/confession_update.html'
    success_url = reverse_lazy('confessions:main-confession-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You are not author of the post, You cant update')
            return super().form_invalid(form)
