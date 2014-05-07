import logging

from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from projects.models import Project
from projects.forms import ProjectForm

log = logging.getLogger(__name__)

'''
Convenience method to check if a given value is a positive integer
'''
def is_positive_integer(value):
	try:
		value = int(value)
	except (ValueError, TypeError):
		return False
	return value > 0

'''
Renders the create page and passes the form object to it
'''
def render_create(request, form):
	return render(request, 'projects/create.html', {
		'form': form
	})

'''
Renders the update page and passes the form object and project's ID to it
'''
def render_update(request, form, project_id):
	return render(request, 'projects/update.html', {
		'form': form,
		'project_id': project_id
	})


'''
This method takes all current query params and creates a pagination query string from them.
	It will not add 'page' to the URL - this is controlled in the pagination template
	It was also not add 'show_all' - this is stored in the user's session so no need for this to be in the URL
	Everything else should be carried through, as we want to retain all other query params (filtering, etc.)
'''
def get_paging_params(request):

	query_string = ''

	for param, value in request.GET.iteritems():
		if param != 'page' and param != 'show_all':
			query_string = query_string + '&' + param + '=' + value

	return query_string

'''
This method calculates which clickable page numbers to display in the pagination UI element.
	paginator: the Django Paginator object
	page: the current page returned from Paginator.page(x)
	pages_per_side: the number of page numbers to show either side of the current page
'''
def get_pages_to_display(paginator, page, pages_per_side):

	pages = []	
	start = page.number - pages_per_side
	end = page.number + pages_per_side

	for i in range(start, end + 1):
		if i > 0 and i <= paginator.num_pages:
			pages.append(i)

	return pages

'''
This method decides whether to show all projects, regardless of visibility (closed or not).
	If show_all is not in the session, returns false by default.
	If show_all is in the session and show_all is in the URL, return it's value of True or False, where valid.
	If show_all in in the session but show_all is not in the URL (or is but invalid), return the current session value of show_all.
'''
def get_show_all(request, closed_project_count):
	try:
		request.session['show_all']
	except KeyError: # By default we only wish to display open projects
		return False
	# If the user has a session, check request params to determine whether they want to view all projects
	if request.GET.get('show_all') == 'true' and closed_project_count > 0:
		return True
	elif request.GET.get('show_all') == 'false':
		return False
	elif closed_project_count == 0:
		return False
	else:
		return request.session['show_all']


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

'''
The view for the project listing page.
---

Request Parameters:
----
page - the pagination page to display. Defaults to 1 if page < 1, and num_pages when page > num_pages
results - the number of projects to display per page, defaults to 5.
show_all - when true, the project list will also display projects that have been closed.
---

Stuff to know...
---
open_project_count and closed_project_count are sent back to the template for useful information the user.
show_all is stored in the session so that it can easily be retrieved later on. Defaults to false.
query_string is sent back to allow the template to easily carry across all active query parameters for subsequent requests
display_pages is sent back to allow the template to determine which page numbers to show in the pagination widget
query_string and display_pages are added to the Django Paginator object (pagination), which can be used in the template
---
'''
class ListView(View):

	def get(self, request):

		page_requested = request.GET.get('page') 		# no need to validate, pagination does this for us
		results_requested = request.GET.get('results')

		if results_requested == None or not is_positive_integer(results_requested):
			results_requested = 5

		# Get all projects from the db
		project_list = Project.objects.order_by('deployment_date')
		open_project_count = project_list.exclude(is_complete = True).count()
		closed_project_count = project_list.exclude(is_complete = False).count()

		# Store show_all config in the session so the app remembers it's value when the user navigates away
		request.session['show_all'] = get_show_all(request, closed_project_count)

		# If show_all has been set to false (default option), filter those records out
		if request.session['show_all'] == False:
			project_list = project_list.exclude(is_complete = True)

		# Now we have a list of projects, get associated pagination
		pagination = Paginator(project_list, results_requested)

		try:
			projects = pagination.page(page_requested)
		except PageNotAnInteger:
			projects = pagination.page(1)
		except EmptyPage:
			projects = pagination.page(pagination.num_pages)

		pagination.query_string = get_paging_params(request)
		pagination.display_pages = get_pages_to_display(pagination, projects, 3)

		return render(request, 'projects/list.html', {
			'projects': projects,
			'pagination': pagination,
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

