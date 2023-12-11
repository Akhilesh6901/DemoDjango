from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import TodoForm
from .models import Task

from django.views.generic import ListView, DeleteView
from django.views.generic import DetailView
from django.views.generic import UpdateView


class Tasklistview(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'


class TaskDetailview(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'tasks'

class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'edit.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'task'
    fields=()



# Create your views here.
def index(request):
    tasks = Task.objects.all()

    if request.method == 'POST':
        name = request.POST.get('task', )
        priority = request.POST.get('priority', )
        date = request.POST.get('date', )
        task = Task(name=name, priority=priority, date=date)
        task.save()

    return render(request, 'index.html', {'tasks': tasks})


# def details(request):
#     return render(request,'details.html',{'task':task})

def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'delete.html')


def update(request, taskid):
    task = Task.objects.get(id=taskid)
    form = TodoForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'update.html', {'form': form, 'task': task})

