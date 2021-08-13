import json

from django.db import models


class SourceManager(models.Manager):
    def create_backend(self, label, backend_path, backend_data=None):
        self.create(
            backend_path=backend_path,
            backend_data=json.dumps(obj=backend_data or {}),
            label=label
        )

    def interactive(self):
        interactive_sources_ids = []
        for source in self.all():
            if getattr(source.get_backend(), 'is_interactive', False):
                interactive_sources_ids.append(source.pk)

        return self.filter(id__in=interactive_sources_ids)
