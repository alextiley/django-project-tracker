import logging

from django.views import generic
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project
from projects.forms import ProjectForm

log = logging.getLogger(__name__)

class CreateView(generic.View):

	def get(self, request):
		return render(request, 'projects/create.html', {
			'form': ProjectForm()
		})

	def post(self, request):
		form = ProjectForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'success.project.created')
			return redirect('/projects')
		else:
			messages.error(request, 'error.form.invalid')
			return render(request, 'projects/create.html', {
				'form': form
			})


class ListView(generic.View):
	def get(self, request):
		showClosed = bool(request.GET.get('showClosed'))
		projects = Project.objects.order_by('deployment_date')

		if not showClosed:
			projects = projects.exclude(is_closed=True)

		return render(request, 'projects/list.html', {
			'projects': projects,
			'showClosed': showClosed
		})

class UpdateView(generic.View):
	def get(self, request, project_id):
		project = get_object_or_404(Project, pk = project_id)
		form = ProjectForm(instance = project)

		return render(request, 'projects/update.html', {
			'form': form,
			'project_id': project_id
		})


class DeleteView(generic.View):
	def post(self, request, project_id):
		try:
			project = Project.objects.get(id = project_id)
			project.delete()
		except ObjectDoesNotExist:
			messages.error(request, 'error.project.invalid')
			return redirect(request.META.get('HTTP_REFERER', None))
		else:
			messages.success(request, 'success.project.deleted')
			return redirect('/projects')