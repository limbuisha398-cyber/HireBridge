from django.core.management.base import BaseCommand
from HireBridge.models import ScoringCriteria

CRITERIA = [
    ("Skills", 20, "Relevant and recognized skills listed"),
    ("Education", 15, "Education history completeness"),
    ("Experience", 20, "Work experience relevance and completeness"),
    ("Projects", 15, "Number and quality of listed projects"),
    ("Completeness", 15, "Overall completeness of all resume sections"),
    ("Formatting", 15, "Contact info, summary length, structure"),
]

class Command(BaseCommand):
    help = "Seed the SCORING_CRITERIA table"

    def handle(self, *args, **kwargs):
        for name, max_score, desc in CRITERIA:
            ScoringCriteria.objects.update_or_create(
                criteria_name=name,
                defaults={'maximum_score': max_score, 'description': desc}
            )
        self.stdout.write(self.style.SUCCESS("Scoring criteria seeded."))