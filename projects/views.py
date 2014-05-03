import logging

from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project
from projects.forms import ProjectForm

log = logging.getLogger(__name__)


def is_positive_integer(value):
	try:
		value = int(value)
	except (ValueError, TypeError):
		return False
	return value > 0


def render_create(request, form):
	return render(request, 'projects/create.html', {
		'form': form
	})


def render_update(request, form, project_id):
	return render(request, 'projects/update.html', {
		'form': form,
		'project_id': project_id
	})


def get_pagination(collection, result_count):

	if not is_positive_integer(result_count):
		result_count = 5

	return Paginator(collection, result_count)


def get_page(pagination, page_number):

	if page_number is None:
		page_number = 1

	try:
		page = pagination.page(page_number)
	except InvalidPage:
		return False

	return page


# Don't add page to the URL, this is controlled in pagination template
# Also, don't pass show_all through as this is stored in the user's session
def get_paging_params(request):

	query_string = ''

	for param, value in request.GET.iteritems():
		if param != 'page' and param != 'show_all':
			query_string = query_string + '&' + param + '=' + value

	return query_string


def get_show_all(request):
	try:
		request.session['show_all']
	except KeyError: # By default we only wish to display open projects
		return False
	# If the user has a session, check request params to determine whether they want to view all projects
	if request.GET.get('show_all') == 'true':
		return True
	elif request.GET.get('show_all') == 'false':
		return False
	else:
		return request.session['show_all']


def get_pages_to_display(pagination, page, count_per_side):

	pages = []
	start = page.number - count_per_side
	end = page.number + count_per_side

	for i in range(start, end + 1):
		if i > 0 and i <= pagination.num_pages:
			pages.append(i)

	return pages


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

		projects = Project.objects.order_by('deployment_date')

		open_project_count = projects.exclude(is_complete = True).count()
		closed_project_count = projects.exclude(is_complete = False).count()

		# Store show_all config in the session so the app remembers it's value when the user navigates away
		request.session['show_all'] = get_show_all(request)

		# If show_all has been set to false (default option), filter those records out
		if request.session['show_all'] == False:
			projects = projects.exclude(is_complete = True)

		# Now we have our project list, get pagination
		pagination = get_pagination(projects, request.GET.get('results'))
		page = get_page(pagination, request.GET.get('page'))
		page.query_string = get_paging_params(request)
		pagination.display_pages = get_pages_to_display(pagination, page, 3)

		if not page:
			items = list()
		else:
			items = page.object_list

		return render(request, 'projects/list.html', {
			'projects': items,
			'pagination': pagination,
			'page': page,
			'open_project_count': open_project_count,
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

