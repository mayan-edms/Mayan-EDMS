from django.apps import apps


def method_check_in(self, user=None):
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )

    return DocumentCheckout.business_logic.check_in_document(
        document=self, user=user
    )


def method_get_check_out_info(self):
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )
    return DocumentCheckout.objects.get_check_out_info(document=self)


def method_get_check_out_state(self):
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )
    return DocumentCheckout.objects.get_check_out_state(document=self)


def method_is_checked_out(self):
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )
    return DocumentCheckout.objects.is_checked_out(document=self)
