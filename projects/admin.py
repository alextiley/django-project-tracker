from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['project_name']}),
		('Release Information', {'fields': ['deployment_date', 'is_closed']}),
	]
	list_display = ('id', 'project_name', 'deployment_date', 'is_closed')
	list_filter = ['is_closed']
	search_fields = ['project_name']

admin.site.register(Project, ProjectAdmin)