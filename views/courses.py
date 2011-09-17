from django.shortcuts import render_to_response, get_object_or_404
from wiki.models.courses import Course
from utils import page_types as types
from django.http import Http404
#from wiki.forms.pages import PageForm

def index(request):
	return render_to_response('courses/index.html')

def all(request):
	courses = Course.objects.all().order_by('department', 'number')
	data = {
		'courses': courses,
	}
	return render_to_response('courses/all.html', data)

def overview(request, department, number):
	course = get_object_or_404(Course, department=department, number=int(number))

	# We can't use it directly in the template file, it just won't work
	page_types = []
	for name, obj in types.iteritems():
		page_types.append({'name': name, 'url': obj.get_create_url(course), 'icon': obj.get_icon(), 'long_name': obj.long_name, 'desc': obj.description})

	data = {
		'course': course,
		'page_types': page_types,
	}
	return render_to_response('courses/overview.html', data)

def create(request, department, number, page_type):
	course = get_object_or_404(Course, department=department, number=int(number))

	if page_type not in types:
		raise Http404
	else:
		obj = types[page_type]
		data = {
			'course': course,
			'page_type': obj,
			'form_template': obj.get_form_template(),
			'help_template': obj.get_help_template(),
			'num_sections': range(1, 11), # for people without javascript DON'T DELETE THIS UNLESS YOU HAVE ANOTHER SOLUTION FOR A FALLBACK
		}
		return render_to_response("pages/create.html", data)
