from unittest import result
from django.views.generic import TemplateView

from .models import Book, Tag, Section, Problem
from accounts.models import User
from .forms import BookCreateForm, SectionCreateForm, ProblemCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin


from django.http import JsonResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render, redirect

# from django.forms.models import model_to_dict

import json


def get_book_list(request):
    user = request.user
    books = Book.objects.filter(user=user).all()
    results = []
    for book in books:
        tags = book.tag.all()

        results.append(
            {
                "title": book.title,
                "description": book.description,
                "user": str(book.user),
                "cover": str(book.cover),
                "tags": [tag.name for tag in tags],
                "finish_count": book.finish_count,
                "postData": book.postData,
                "pk": int(book.pk)
            }
        )
    return JsonResponse(results, safe=False)


def get_detail_book(request, pk):
    book = Book.objects.get(id=pk)

    results = []
    tags = book.tag.all()

    bookSection = Book.objects.filter(id=pk).prefetch_related('section')
    sections = bookSection[0].section.all().order_by('orderNum')

    results.append(
        {
            "title": book.title,
            "description": book.description,
            "user": str(book.user),
            "cover": str(book.cover),
            "tags": [tag.name for tag in tags],
            "finish_count": book.finish_count,
            "postData": book.postData,
            "pk": int(book.pk),
            "sectionPk": [section.pk for section in sections],
            "sectionTitle": [section.title for section in sections],
            "sectionOrder": [section.orderNum for section in sections]
        }
    )
    return JsonResponse(results, safe=False, status=200)


def get_detail_section(request, pk):
    section = Section.objects.get(id=pk)
    results = []

    sectionProblem = Section.objects.filter(
        id=pk).prefetch_related('problem')
    problems = sectionProblem[0].problem.all().order_by('orderNum')

    results.append(
        {
            'title': section.title,
            'book': section.book.pk,
            'bookCover': str(section.book.cover),
            'orderNum': section.orderNum,
            "problemPk": [problem.pk for problem in problems],
            "problemQuestion": [problem.question for problem in problems],
            "problemAnswer": [problem.answer for problem in problems],
            "problemExplanation": [problem.explanation for problem in problems],
            "problemOrder": [problem.orderNum for problem in problems],
        }
    )

    return JsonResponse(results, safe=False, status=200)


class BookCreateView(LoginRequiredMixin, TemplateView):
    template_name: str = 'repercisebook/create.html'

    def post(self, request):
        if request.method == 'POST':
            form = BookCreateForm(request.POST, request.FILES)

            if form.is_valid():
                book = form.save(commit=False)
                book.user = self.request.user
                book.save()
                tag_list = request.POST.get('tag').split(",")
                if tag_list:
                    for tag in tag_list:
                        book.tag.add(
                            Tag.objects.get_or_create(name=tag)[0])

                form.save_m2m()
                return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()


class BookDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'repercisebook/detail.html'

    def post(self, request, pk):
        if request.method == 'POST':
            form = BookCreateForm(request.POST, request.FILES)

            sections = json.loads(request.POST.get('sections'))
            upd_sections = []

            # section更新
            for i, section in enumerate(sections):
                if section.get('title') == '':
                    return HttpResponseServerError()

                sectionObj = Section.objects.get(id=section.get('pk'))
                sectionObj.title = section.get('title')
                sectionObj.orderNum = 1000 * (i + 1)

                upd_sections.append(sectionObj)

            if form.is_valid():
                book = Book.objects.get(id=pk)
                book.title = request.POST.get('title')
                book.description = request.POST.get('description')
                if request.FILES:
                    book.cover = request.FILES.get('cover')

                tag_list = request.POST.get('tags').split(",")
                book.tag.clear()
                if tag_list:
                    for tag in tag_list:
                        book.tag.add(
                            Tag.objects.get_or_create(name=tag)[0])

                book.save()

                # 一括更新
                Section.objects.bulk_update(upd_sections, fields=[
                                            'title', 'orderNum'])
                return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()


class BookDeleteView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        if request.method == 'POST':
            book = Book.objects.get(id=pk)
            book.delete()

            return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()


class SectionCreateView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        if request.method == 'POST':
            form = SectionCreateForm(request.POST)
            if form.is_valid():
                section = form.save(commit=False)
                book = Book.objects.filter(id=pk).prefetch_related('section')
                sectionList = list(book[0].section.all().values())

                section.title = request.POST.get('title')
                section.book_id = pk

                if sectionList == []:
                    section.orderNum = 1000
                else:
                    section.orderNum = sectionList[-1].get('orderNum') + 1000

                section.save()
                return JsonResponse({"status": 'Success'})
            else:
                return HttpResponseServerError()


class SectionDetailView(LoginRequiredMixin, TemplateView):
    template_name: str = 'repercisebook/sectionDetail.html'

    def post(self, request, pk):
        if request.method == 'POST':
            form = SectionCreateForm(request.POST)

            problems = json.loads(request.POST.get('problems'))
            upd_problems = []

            # 問題更新
            for i, problem in enumerate(problems):
                if problem.get('question') == '' or problem.get('answer') == '':
                    return HttpResponseServerError()

                problemObj = Problem.objects.get(id=problem.get('pk'))
                problemObj.question = problem.get('question')
                problemObj.answer = problem.get('answer')
                problemObj.explanation = problem.get('explanation')
                problemObj.orderNum = 1000 * (i + 1)

                upd_problems.append(problemObj)

            if form.is_valid():
                section = Section.objects.get(id=pk)
                section.title = request.POST.get('title')

                section.save()

                # 一括更新
                Problem.objects.bulk_update(upd_problems, fields=[
                                            'question', 'answer', 'explanation', 'orderNum'])
                return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()


class SectionDeleteView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        if request.method == 'POST':
            section = Section.objects.get(id=pk)
            section.delete()

            return JsonResponse({"status": 'Success'})
        else:
            return HttpResponseServerError()


class ProblemCreateView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        if request.method == 'POST':
            form = ProblemCreateForm(request.POST)
            if form.is_valid():
                problem = form.save(commit=False)
                section = Section.objects.filter(
                    id=pk).prefetch_related('problem')
                problemList = list(section[0].problem.all().values())

                problem.question = request.POST.get('question')
                problem.answer = request.POST.get('answer')
                problem.explanation = request.POST.get('explanation')
                problem.section_id = pk

                if problemList == []:
                    section.orderNum = 1000
                else:
                    section.orderNum = problemList[-1].get('orderNum') + 1000

                problem.save()
                return JsonResponse({"status": 'Success'})
            else:
                return HttpResponseServerError()


class ProblemUpdateView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        if request.method == 'POST':
            form = ProblemCreateForm(request.POST)
            if form.is_valid():
                problem = Problem.objects.get(id=pk)

                problem.save()
                return JsonResponse({"status": 'Success'})
            else:
                return HttpResponseServerError()


class ProblemDeleteView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        if request.method == 'POST':
            problem = Problem.objects.get(id=pk)
            problem.delete()

            return JsonResponse({"status": "Success"})
        else:
            return HttpResponseServerError()
