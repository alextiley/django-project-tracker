import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from projects.models import Project, ProjectForm

log = logging.getLogger(__name__)

class CreateView(generic.View):

	def get(self, request):
		return render(request, 'projects/create.html')

	def post(self, request):

		form = ProjectForm(request.POST)

		if form.is_valid():
			form.save()
			redirect('projects/list.html')

		return render(request, 'projects/create.html', {
			'project': form
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

		return render(request, 'projects/update.html', {
			'project': project
		})


class DeleteView(generic.View):

	def get(self, request, project_id):
		return render(request, 'projects/delete.html')
