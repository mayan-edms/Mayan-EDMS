from django.core.urlresolvers import reverse

from rest_framework import serializers

from documents.models import Document


class DocumentResourceSimple(serializers.HyperlinkedModelSerializer):
    def versions(self, instance):
        return [
            {
                'version': version.get_formated_version(),
                'major': version.major,
                'minor': version.minor,
                'micro': version.micro,
                'release_level': version.release_level,
                'serial': version.serial,
                'timestamp': version.timestamp,
                'comment': version.comment,
                'mimetype': version.mimetype,
                'encoding': version.encoding,
                'filename': version.filename,
                'checksum': version.checksum,
                'download': reverse('document_version_download', args=[version.pk]),
                'stored_filename': version.file.name,
                # TODO: Add transformations
                'pages': [
                    {
                        'content': page.content,
                        'page_label': page.page_label,
                        'page_number': page.page_number,
                    }
                    for page in version.pages.all()
                ]

            }
            for version in instance.versions.all()
        ]

    class Meta:
        model = Document
        fields = ('url', 'uuid', 'date_added', 'description')
