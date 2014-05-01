from django import forms
from django.forms import extras

from projects.models import Project

class ProjectForm(forms.ModelForm):

	name = forms.CharField(
		initial = '',
		widget = forms.TextInput(attrs = {
			'class': 'form-control',
			'placeholder': 'Enter a project name, e.g. MINTV_18'
		})
	)

	deployment_date = forms.DateField(
		widget = extras.SelectDateWidget(
			attrs = {
				'class': 'form-control'
			}
		)
	)

	deployment_time = forms.TimeField(
		widget = forms.TimeInput(
			format = '%H:%M',
			attrs = {
				'class': 'form-control',
				'placeholder': 'Enter a time in 24 hour format (hh:mm), e.g. 14:30 or 06:00',
				'value': '12:00'
			}
		)
	)
	
	is_complete = forms.BooleanField(
		required = False,
		initial = False,
		widget = forms.NullBooleanSelect(
			attrs = {
				'class': 'form-control'
			}
		)
	)

	class Meta:
		model = Project
		initial = {'is_complete': False}