from django.shortcuts import redirect, render, get_object_or_404
import random
from .models import *
from django.http import HttpResponse

# Home view
def home(request):
    return render(request, 'home.html')

# About view
def about(request):
    return render(request, 'about.html')

# Quiz categories view
def quiz(request):
    categories = Category.objects.all()  # Fetch all categories
    return render(request, 'quiz.html', {'categories': categories})

# Start quiz based on selected category
def start_quiz(request, category_id):
    # Ensure the category exists or return a 404 error
    category = get_object_or_404(Category, id=category_id)

    # Fetch questions for the selected category
    questions = Question.objects.filter(category=category)

    if not questions.exists():
        return render(request, 'quiz_page.html', {
            'error_message': 'No questions are available for this category.',
            'category': category,
        })

    # Randomly select up to 10 questions from the category
    selected_questions = random.sample(list(questions), min(len(questions), 10))

    return render(request, 'quiz_page.html', {
        'questions': selected_questions,
        'category': category
    })


# Handle quiz results after submission
def result(request):
    if request.method == 'POST':
        correct_answers = 0
        total_questions = 0
        answers = {}  # To store the answers submitted by the user

        # Loop through each question and check the answer
        for question_id, selected_answer in request.POST.items():
            # Skip CSRF token and other non-answer fields
            if question_id == 'csrfmiddlewaretoken':
                continue

            # The question ID is used to fetch the question object
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                continue  # Skip if question doesn't exist (just a safety check)

            total_questions += 1

            # Compare selected answer with the correct one
            if int(selected_answer) == question.answer:
                correct_answers += 1
        
        # You can also use the logged-in user to display their name
        user_name = request.user.username if request.user.is_authenticated else 'Guest'

        # Pass the results to the template
        context = {
            'user_name': user_name,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
        }
        return render(request, 'result.html', context)

    else:
        return redirect('quiz')  # If no POST data, redirect to quiz page
