from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import MarkForm
from .models import ExamRecord 
from students.models import Student
from exams.models import Exam
from subjects.models import Subject
# from .filters import ExamRecordFilter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from customaccounts.mixins import GroupRequiredMixin  # Import the mixin
from django.contrib.auth.mixins import LoginRequiredMixin
from customaccounts.decorators import group_required 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

POSTS_PER_PAGE = 4


# class ExamRecordListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
#     model = ExamRecord
#     template_name = 'mark_list.html'
#     context_object_name = 'marks'
#     group_required = 'operator'

# Mark Views
class ExamRecordCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = ExamRecord
    form_class = MarkForm
    template_name = 'mark_form.html'
    success_url = reverse_lazy('marks-filter-list-view')  # Redirect after successful creation
    success_message = 'record for stu  {}  added.'.format(model.student)
    group_required = 'operator'


    def form_invalid(self, form):
        print(form.errors)  # or log the errors
        return self.render_to_response(self.get_context_data(form=form))
        # return super().form_invalid(form)

class ExamRecordUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = ExamRecord
    form_class = MarkForm
    template_name = 'mark_form.html'
    success_url = reverse_lazy('marks-filter-list-view')  # Redirect after successful update
    group_required = 'operator'

    def form_invalid(self, form):
        print(form.errors)  # or log the errors
        return super().form_invalid(form)


# def search(request):
#     exam_record_list = ExamRecord.objects.all()
#     exam_record_filter = ExamRecordFilter(request.GET, queryset=exam_record_list)
#     return render(request, 'search/mark-search-list.html', {'filter': exam_record_filter})

@login_required
@group_required('operator')
def filter_list_view(request):
    students = Student.objects.all()
    exams = Exam.objects.all()
    subjects = Subject.objects.all()

    exam_records = ExamRecord.objects.all()

    # Filtering based on the selected student, exam, and subject
    if request.GET.get('student'):
        exam_records = exam_records.filter(student_id=request.GET['student'])
    if request.GET.get('exam'):
        exam_records = exam_records.filter(exam_id=request.GET['exam'])
    if request.GET.get('subject'):
        exam_records = exam_records.filter(subject_id=request.GET['subject'])

    # Pagination
    paginator = Paginator(exam_records, 10)  # Show 10 exam records per page
    page = request.GET.get('page')
    
    try:
        exam_records = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exam_records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        exam_records = paginator.page(paginator.num_pages)

    context = {
        'students': students,
        'exams': exams,
        'subjects': subjects,
        'exam_records': exam_records,  # Paginated exam records
    }
    return render(request, 'mark_filter_list.html', context)


class ExamRecordDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = ExamRecord
    group_required = 'operator'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if the request is AJAX
            try:
                self.object = self.get_object()
                self.object.delete()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        else:
            return super().post(request, *args, **kwargs)
