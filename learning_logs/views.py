from django.shortcuts import render, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


from .models import Topic, Entry, TopicForm, EntryForm


# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')

@login_required()
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required()
def entries(request, pk):
    topic = Topic.objects.get(pk=pk)
    if topic.owner!=request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'entries': entries, 'topic': topic}
    return render(request, 'learning_logs/entries.html', context)

@login_required()
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, pk):
    topic = Topic.objects.get(pk=pk)
    if topic.owner!=request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:entries', args=[topic.id]))
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, topic_pk, entry_pk):
    topic = Topic.objects.get(pk = topic_pk)
    entry = Entry.objects.get(pk = entry_pk)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:entries', args=[topic.pk]))
    return render(request, 'learning_logs/edit_entry.html', {'form': form, 'entry': entry, 'topic': topic})