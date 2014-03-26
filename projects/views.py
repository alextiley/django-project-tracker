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
		
		try:
			request.session['show_all']

		# By default we only wish to display open projects
		except KeyError:
			request.session['show_all'] = False

		# If the user has a session, check request params to 
		# determine whether they want to view all projects
		else:
			if request.GET.get('show_all') == 'true':
				request.session['show_all'] = True
			elif request.GET.get('show_all') == 'false':
				request.session['show_all'] = False

		projects = Project.objects.order_by('deployment_date')
		open_projects = projects.exclude(is_complete = True)
		closed_project_count = projects.exclude(is_complete = False).count()

		if request.session['show_all'] == True:
			closed_projects = projects.exclude(is_complete = False)
		else:	
			closed_projects = list()

		return render(request, 'projects/list.html', {
			'open_projects': open_projects,
			'closed_projects': closed_projects,
			'closed_project_count': closed_project_count,
			'show_all': request.session['show_all']
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

