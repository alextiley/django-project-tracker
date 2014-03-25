import logging

from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project
from projects.forms import ProjectForm

log = logging.getLogger(__name__)


def render_create(request, form):
	return render(request, 'projects/create.html', {
		'form': form
	})


def render_update(request, form, project_id):
	return render(request, 'projects/update.html', {
		'form': form,
		'project_id': project_id
	})


class CreateView(View):

	def get(self, request):
		return render_create(request, ProjectForm())

	def post(self, request):
		form = ProjectForm(request.POST)

		if form.is_valid():
			project = form.save()
			messages.success(request, 'Project \'' + project.name + '\' was successfully created.')
			return redirect('/projects')
		else:
			messages.error(request, 'Sorry, but there was a problem with the information you supplied.')
			return render_create(request, form)


class ListView(View):
	def get(self, request):
		
		show_all = bool(request.GET.get('show_all'))
		projects = Project.objects.order_by('deployment_date')
		open_projects = projects.exclude(is_complete = True)
		closed_projects = list()

		if show_all:
			closed_projects = projects.exclude(is_complete = False)

		return render(request, 'projects/list.html', {
			'open_projects': open_projects,
			'closed_projects': closed_projects,
			'show_all': show_all
		})


class UpdateView(View):
	def get(self, request, project_id):
		project = get_object_or_404(Project, pk = project_id)
		form = ProjectForm(instance = project)
		return render_update(request, form, project_id)

	def post(self, request, project_id):
		project = Project.objects.get(pk = project_id)
		form = ProjectForm(request.POST, instance = project)
		if form.is_valid():
			project = form.save()
			messages.success(request, 'Project \'' + project.name + '\' was successfully updated.')
			return redirect('/projects/update/' + project_id)
		else:
			messages.error(request, 'Sorry, but there was a problem with the information you supplied.')
			return render_update(request, form, project_id)


class DeleteView(View):
	def post(self, request, project_id):
		try:
			project = Project.objects.get(id = project_id)
			project.delete()
		except ObjectDoesNotExist:
			# Don't show an error here, there's no need to tell potential hackers that the project doesn't exist
			return redirect(request.META.get('HTTP_REFERER', None))
		else:
			messages.success(request, 'Project \'' + project.name + '\' was successfully deleted.')
			return redirect('/projects')

