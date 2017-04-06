from django.test import TestCase

import datetime

from django.utils import timezone

from .models import Question

from django.urls import reverse

# First test
class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

# Second test        
def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
    
def create_choice(created_question, choice_text):
    """
    Creates a choice for created question.
    """
    return created_question.choice_set.create(choice_text=choice_text, votes=0)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        new_question = create_question(question_text="Past question.", days=-30)
        create_choice(created_question=new_question, choice_text='Past choice.')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        new_question = create_question(question_text="Future question.", days=30)
        create_choice(created_question=new_question, choice_text='Future choice.')
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        new_question_1 = create_question(question_text="Past question.", days=-30)
        create_choice(created_question=new_question_1, choice_text='Past choice.')
        new_question_2 = create_question(question_text="Future question.", days=30)
        create_choice(created_question=new_question_2, choice_text='Future choice.')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        new_question_1 = create_question(question_text="Past question 1.", days=-30)
        create_choice(created_question=new_question_1, choice_text='Past choice 1.')
        new_question_2 = create_question(question_text="Past question 2.", days=-5)
        create_choice(created_question=new_question_2, choice_text='Past choice 2.')
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        
    def test_index_view_with_a_question_without_choice(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        new_question = create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], []) 


# Third test       
class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_future_questions(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=30)
        create_choice(created_question=future_question, choice_text='Future choice.')
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_detail_view_with_past_questions(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text="Past question.", days=-5)
        create_choice(created_question=past_question, choice_text='Past choice.')
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    def test_detail_view_with_a_question_without_a_choice(self):
        """
        The detail view of a question without a choice future should
        return a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        
