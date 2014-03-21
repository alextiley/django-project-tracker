from projects.models import Project
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

def create(request):
	return render(request, 'projects/create.html')



def read(request):

	showClosed = bool(request.GET.get('showClosed'))
	projects = Project.objects.order_by('deployment_date')

	if not showClosed:
		projects = projects.exclude(is_closed=True)

	return render(request, 'projects/read.html', {
		'projects': projects,
		'showClosed': showClosed
	})


def update(request, project_id):

	project = get_object_or_404(Project, pk = project_id)

	return render(request, 'projects/update.html', {
		'project': project
	})



def delete(request, project_id):
	return render(request, 'projects/delete.html')



#class ProjectListView(View):
#	def get(request):
#		pass