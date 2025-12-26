from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Student, Patron
from examrecords.models import ExamRecord
from django.urls import reverse_lazy
from .forms import StudentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from subjects.models import Subject
from .forms import SubjectSelectionForm
from customaccounts.mixins import GroupRequiredMixin  # Import the mixin
from django.contrib.auth.mixins import LoginRequiredMixin
import plotly.express as px
import logging
import pandas as pd
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import redirect


# Create your views here.
# class StudentListView(LoginRequiredMixin, GroupRequiredMixin, ListView):
#     model = Student
#     template_name = 'student_list.html'
#     context_object_name = 'students'
#     paginate_by = 10
#     group_required = 'operator'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)  # Ensure this line is present
#         # Add additional context if needed

#         # since in CBV we need to load the all the object to provide the drop down capability to filter students
#         context['all_students'] = Student.objects.all()  # All students for the dropdown
        
#         return context

#     def get_queryset(self):
#         queryset = super().get_queryset()

#         student_id = self.request.GET.get('student')
#         if student_id:
#             queryset = queryset.filter(id=student_id)


#         return queryset.order_by('id')
    
#     def paginate_queryset(self, queryset, page_size):
#         """
#         Override the paginate_queryset method to handle EmptyPage and redirect to the last valid page.
#         """
#         paginator = self.get_paginator(queryset, page_size)
#         page = self.request.GET.get('page')

#         try:
#             students = paginator.page(page)
#         except PageNotAnInteger:
#             # If page is not an integer, deliver the first page.
#             students = paginator.page(1)
#         except EmptyPage:
#             # If the page is empty or out of range, deliver the last page.
#             students = paginator.page(paginator.num_pages)

#         return (paginator, students, students.object_list, students.has_other_pages())

#     def get(self, request, *args, **kwargs):
#         """
#         If the page contains no results after deletion, catch the EmptyPage exception
#         and redirect to the last valid page.
#         """
#         try:
#             return super().get(request, *args, **kwargs)
#         except Http404:
#             # Handle invalid page by redirecting to the last valid page
#             page_number = self.request.GET.get('page', 1)
#             paginator = self.get_paginator(self.get_queryset(), self.paginate_by)
#             last_page = paginator.num_pages

#             # If the current page is out of range, redirect to the last valid page
#             if int(page_number) > last_page:
#                 return redirect(f"{reverse_lazy('student-list')}?page={last_page}")

#             raise
from .forms import StudentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SubjectSelectionForm
from customaccounts.mixins import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
import plotly.express as px
import pandas as pd
from django.http import JsonResponse, Http404

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    paginate_by = 10
    group_required = 'operator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        # Check if the user belongs to the 'operator' group
        # This boolean will be used in the template to show/hide buttons
        is_operator = False
        if self.request.user.is_authenticated:
            is_operator = self.request.user.groups.filter(name='operator').exists()
        
        # Dropdown data for the filter form
        context['is_operator'] = is_operator
        context['all_students'] = Student.objects.all().order_by('first_name')
        context['all_patrons'] = Patron.objects.all().order_by('first_name')
        context['academic_levels'] = range(1, 14)
        return context

    def get_queryset(self):
        # Start with the base queryset
        queryset = super().get_queryset()

        # Capture GET parameters
        student_id = self.request.GET.get('student')
        academic_level = self.request.GET.get('level')
        patron_id = self.request.GET.get('patron')
        is_scholarship = self.request.GET.get('scholarship')
        is_aid = self.request.GET.get('aid')

        # 1. Filter by Specific Student
        if student_id:
            queryset = queryset.filter(id=student_id)

        # 2. Filter by Academic Level
        if academic_level:
            queryset = queryset.filter(current_academic_level=academic_level)

        # 3. Filter by Patron (ManyToMany Relationship)
        if patron_id:
            queryset = queryset.filter(patrons__id=patron_id)

        # 4. Filter by Scholarship Recipient Status
        if is_scholarship == 'on':
            queryset = queryset.filter(is_scholarship_recipient=True)

        # 5. Filter by Financial Aid Recipient Status
        if is_aid == 'on':
            queryset = queryset.filter(is_financial_aid_recipient=True)

        # Use .distinct() to prevent duplicate rows when filtering across ManyToMany (Patrons)
        return queryset.distinct().order_by('id')
    
    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(queryset, page_size)
        page = self.request.GET.get('page')

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        return (paginator, students, students.object_list, students.has_other_pages())

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            page_number = self.request.GET.get('page', 1)
            paginator = self.get_paginator(self.get_queryset(), self.paginate_by)
            last_page = paginator.num_pages

            if int(page_number) > last_page:
                return redirect(f"{reverse_lazy('student-list')}?page={last_page}")
            raise   

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'
    context_object_name = 'student'
    # group_required = 'operator'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['is_operator'] = user.groups.filter(name='operator').exists() or user.is_superuser

        # Fetch all marks for the student
        marks_list = ExamRecord.objects.filter(student=self.object)
        # Setup pagination, display 10 marks per page
        paginator = Paginator(marks_list, 5)

        page = self.request.GET.get('page')
        try:
            marks = paginator.page(page)
        except PageNotAnInteger:
            marks = paginator.page(1)
        except EmptyPage:
            marks = paginator.page(paginator.num_pages)

        context['marks'] = marks
        return context


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['marks'] = ExamRecord.objects.filter(student=self.object)
    #     return context
        

class StudentMarksView(DetailView):
    model = Student
    template_name = 'student_marks.html'
    context_object_name = 'student'
    group_required = 'operator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Get the subject_id from the URL query parameters (GET request)
        subject_id = self.request.GET.get('subject')
        
        # 2. Start with all marks for this specific student
        marks_queryset = ExamRecord.objects.filter(student=self.object)
        
        # 3. Apply filter if a subject was selected in the dropdown
        if subject_id:
            marks_queryset = marks_queryset.filter(subject_id=subject_id)
            
        # 4. Attach the filtered marks to the context
        context['marks'] = marks_queryset
        
        # 5. Attach ALL subjects to populate your filter dropdown
        context['subjects'] = Subject.objects.all().order_by('name')
        
        # 6. (Optional) Pass back the selected subject to keep the dropdown value
        context['selected_subject'] = subject_id
        # context['marks'] = ExamRecord.objects.filter(student=self.object)
        return context

# updates/inserts
class StudentCreateView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')  # Redirect after successful creation
    group_required = 'operator'

    def form_invalid(self, form):
        print(form.errors)  # This will print the form errors to the console
        return super().form_invalid(form)

class StudentUpdateView(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')  # Redirect after successful update
    group_required = 'operator'

class StudentMarksChartView(DetailView):
    model = Student
    template_name = 'student_marks_chart.html'
    context_object_name = 'student'
    group_required = 'operator'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        marks_queryset = ExamRecord.objects.filter(student=student)

        # Preparing data for Plotly
        marks_data = [
            {
                'exam_name': mark.exam.name,
                'subject_name': mark.subject.name,
                'marks_obtained': mark.marks_obtained,
                'exam_date': mark.exam.date
            }
            for mark in marks_queryset
        ]

        # Create a DataFrame (you may need pandas installed for this)
        df = pd.DataFrame(marks_data)

        # Ensure dates are sorted
        if not df.empty:
            df = df.sort_values(by='exam_date')  # Sort DataFrame by 'exam_date'

            # Plotly Line Chart (marks across exams grouped by subject)
            fig = px.line(df, x='exam_date', y='marks_obtained', color='subject_name',
                          title=f"Exam Marks for {student.first_name} {student.last_name}",
                          markers=True)

            # Convert plot to HTML for rendering in the template
            context['graph_div'] = fig.to_html(full_html=False)

        return context


#for a single subject
def student_marks_chart(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    form = SubjectSelectionForm(request.GET or None)
    graph_div = None

    if form.is_valid():
        subject = form.cleaned_data['subject']
        # Query exam records of the student for the selected subject
        exam_records = ExamRecord.objects.filter(student=student, subject=subject).order_by('exam__date')

        # Extract data for the plot
        dates = [record.exam.date for record in exam_records]
        marks = [record.marks_obtained for record in exam_records]

        # Ensure dates and marks are sorted by date
        sorted_dates_marks = sorted(zip(dates, marks))  # Sort by the date
        
        sorted_dates, sorted_marks = zip(*sorted_dates_marks)  # Unzip the sorted pairs

        # Create Plotly line chart
        fig = px.line(
            x=sorted_dates,
            y=sorted_marks,
            title=f"{student.first_name}'s Marks for {subject.name}",
            labels={'x': 'Date', 'y': 'Marks Obtained'},
            markers=True,
            symbol=subject
        )
        graph_div = fig.to_html(full_html=False)

    return render(request, 'student_marks_chart.html', {
        'student': student,
        'form': form,
        'graph_div': graph_div,
    })

class StudentDeleteView(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    model = Student
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
        

class ImpactView(TemplateView):
    template_name = 'impact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Todo: Pulling real counts from your models
        # context['book_count'] = BookDonation.objects.count()
        # context['scholar_count'] = Student.objects.filter(is_scholar=True).count()
        return context