TEST_TAG_LABEL = 'test-tag'
TEST_TAG_LABEL_EDITED = 'test-tag-edited'
TEST_TAG_COLOR = '#001122'
TEST_TAG_COLOR_EDITED = '#221100'

TEST_TAG_INDEX_HAS_TAG = 'HAS_TAG'
TEST_TAG_INDEX_NO_TAG = 'NO_TAG'
TEST_TAG_INDEX_NODE_TEMPLATE = '''
{{% for tag in document.tags.all %}}
{{% if tag.label == "{tag_label}" %}}
{has_tag}
{{% else %}}
{no_tag}
{{% endif %}}
{{% empty %}}
{no_tag}
{{% endfor %}}
'''.format(
    tag_label='{}_0'.format(TEST_TAG_LABEL), has_tag=TEST_TAG_INDEX_HAS_TAG,
    no_tag=TEST_TAG_INDEX_NO_TAG
).replace('\n', '')
