"""Utilities for exams"""


from typing import Any
from api.models import UserQuestionResult


def get_exam_stats(uqr: UserQuestionResult) -> dict[str, list[dict[str, Any]]]:
    """Return a dictionary of exam statistics."""

    exam_stats = {}
    for el in uqr:
        if el.exam_id not in exam_stats:
            exam_stats[el.exam_id] = {
                'name': el.exam.name,
                'answers': 0,
                'correct_answers': 0}
        exam_stats[el.exam_id]['answers'] += 1
        exam_stats[el.exam_id]['correct_answers'] += el.is_correct_int

    exam_stats_by_accuracy = dict(sorted(
        exam_stats.items(),
        key=lambda item:
            item[1]['correct_answers'] / item[1]['answers']))

    exam_stats_by_popularity = dict(sorted(
        exam_stats.items(),
        key=lambda item:
            item[1]['answers'],
        reverse=True))

    exam_stats_by_accuracy_readable = [
        {'number': i + 1,
            'id': id,
            'name': el['name'],
            'accuracy': round(el['correct_answers'] / el['answers'], 3) * 100}
        for i, (id, el) in enumerate(exam_stats_by_accuracy.items())]

    exam_stats_by_popularity_readable = [
        {'number': i + 1,
            'id': id,
            'name': el['name'],
            'answers': el['answers']}
        for i, (id, el) in enumerate(exam_stats_by_popularity.items())]

    return {
        'accuracy': exam_stats_by_accuracy_readable,
        'popularity': exam_stats_by_popularity_readable,
    }
