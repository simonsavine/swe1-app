import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def create_question(question_text, days):
    """A question published `days` from now (negative for the past)."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        self.assertIs(Question(pub_date=time).was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        self.assertIs(Question(pub_date=time).was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        self.assertIs(Question(pub_date=time).was_published_recently(), True)

    def test_str_returns_the_text(self):
        question = create_question("What's new?", days=-1)
        choice = Choice.objects.create(question=question, choice_text="Not much")
        self.assertEqual(str(question), "What's new?")
        self.assertEqual(str(choice), "Not much")


class IndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_lists_the_latest_five_newest_first(self):
        questions = [create_question(f"Question {n}", days=-n) for n in range(1, 7)]
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"], questions[:5]
        )


class DetailAndResultsViewTests(TestCase):
    def test_detail_shows_the_question(self):
        question = create_question("Past question.", days=-5)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertContains(response, question.question_text)

    def test_detail_of_missing_question_is_404(self):
        response = self.client.get(reverse("polls:detail", args=(999,)))
        self.assertEqual(response.status_code, 404)

    def test_results_show_the_votes(self):
        question = create_question("Results?", days=-1)
        Choice.objects.create(question=question, choice_text="Yes", votes=2)
        response = self.client.get(reverse("polls:results", args=(question.id,)))
        self.assertContains(response, "Yes -- 2 votes")


class VoteViewTests(TestCase):
    def setUp(self):
        self.question = create_question("Vote?", days=-1)
        self.choice = Choice.objects.create(question=self.question, choice_text="A")

    def test_vote_counts_and_redirects_to_results(self):
        url = reverse("polls:vote", args=(self.question.id,))
        response = self.client.post(url, {"choice": self.choice.id})
        self.assertRedirects(
            response, reverse("polls:results", args=(self.question.id,))
        )
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_vote_without_a_choice_shows_an_error(self):
        url = reverse("polls:vote", args=(self.question.id,))
        response = self.client.post(url, {})
        self.assertContains(response, "You didn&#x27;t select a choice.")
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)
