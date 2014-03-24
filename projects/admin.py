from django.contrib import admin
from projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name']}),
		('Release Information', {'fields': ['deployment_date', 'is_complete']}),
	]
	list_display = ('id', 'name', 'deployment_date', 'is_complete')
	list_filter = ['is_complete']
	search_fields = ['name']

admin.site.register(Project, ProjectAdmin)