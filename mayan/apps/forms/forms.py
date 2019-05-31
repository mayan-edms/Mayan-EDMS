from __future__ import unicode_literals

import json

from django import forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.forms import DynamicModelForm
#from mayan.apps.common.settings import setting_project_title, setting_project_url

#from .classes import MailerBackend
#from .models import UserMailer
#from .permissions import permission_user_mailer_use
#from .settings import (
#    setting_document_body_template, setting_document_subject_template,
#    setting_link_body_template, setting_link_subject_template
#)
#from .validators import validate_email_multiple

from .models import FormInstance


class FormInstanceDynamicForm(DynamicModelForm):
    class Meta:
        #fields = ('label', 'default', 'enabled', 'backend_data')
        fields = ('data',)
        model = FormInstance
        widgets = {'data': forms.widgets.HiddenInput}

    def __init__(self, *args, **kwargs):
        result = super(FormInstanceDynamicForm, self).__init__(*args, **kwargs)

        if self.instance:
            #print("!!!!!!!!!!! instace data", self.instance.get_data())
            ##print("!!!!!!!!!!! instace data", type(self.instance.get_data()))
            print("!!!!!!!!!!! instace data", self.instance.data)
            print("!!!!!!!!!!! instace data", type(self.instance.data))
            self.set_dynamic_values(values=self.instance.data)

        """

        instance_data = self.instance.get_data()

        if instance_data:
            #print("@@@@@@@@@!!!!!!!!!!!! self.instance.data", self.instance.data)
            #print("@@@@@@@@@!!!!!!!!!!!! data", data)
            #print("@@@@@@@@@!!!!!!!!!!!! type: data", type(data))
            #print("@@@@@@@@@!!!!!!!!!!!! self.fields", self.fields)
            #print("@@@@@@@@@!!!!!!!!!!!! self.fields", self.fields.keys())
            for key in self.instance.form_template.get_fields_dictionary():
                #print("@@@@@@@@@@@key", key)
                #print("@@@@@@@@@@@key", type(data))
                #print("@@@@@@@@@@@key", data[key])
                self.fields[key].initial = instance_data[key]

        return result
        """

    def clean(self):
        cleaned_data = super(FormInstanceDynamicForm, self).clean()
        cleaned_data['data'] = json.dumps(self.get_dynamic_values())
        return cleaned_data

        """

        cleaned_data = super(FormInstanceDynamicForm, self).clean()

        # Consolidate the dynamic fields into a single JSON field called
        # 'backend_data'.
        form_instance_data = {}

        for field_name, field_data in self.schema['fields'].items():
            form_instance_data[field_name] = cleaned_data.pop(
                field_name, field_data.get('default', None)
            )

        print("!!!!!!!!!!!!!!!!!! form_instance_data", form_instance_data)
        #cleaned_data['data'] = json.dumps(form_instance_data)
        cleaned_data['data'] = form_instance_data
        return cleaned_data
        """
