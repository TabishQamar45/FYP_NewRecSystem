from .models import Category

def subject_renderer(request):
    return {'all_subjects': Category.objects.all(),}
