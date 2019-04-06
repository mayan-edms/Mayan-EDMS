from __future__ import unicode_literals

TEST_TAG_LABEL = 'test-tag'
TEST_TAG_LABEL_EDITED = 'test-tag-edited'
TEST_TAG_COLOR = '#001122'
TEST_TAG_COLOR_EDITED = '#221100'

TEST_TAG_LABEL_2 = 'test-tag-2'

TEST_TAG_INDEX_HAS_TAG = 'HAS_TAG'
TEST_TAG_INDEX_NO_TAG = 'NO_TAG'
TEST_TAG_INDEX_NODE_TEMPLATE = '''
{{% for tag in document.tags.all %}}
{{% if tag.label == "{}" %}}
{}
{{% else %}}
NO_TAG
{{% endif %}}
{{% empty %}}
NO_TAG
{{% endfor %}}
'''.format(
    TEST_TAG_LABEL, TEST_TAG_INDEX_HAS_TAG, TEST_TAG_INDEX_NO_TAG,
    TEST_TAG_INDEX_NO_TAG
).replace('\n', '')
