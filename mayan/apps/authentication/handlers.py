from .events import event_user_logged_in, event_user_logged_out


def handler_user_logged_in(sender, **kwargs):
    event_user_logged_in.commit(
        actor=kwargs['user'], target=kwargs['user']
    )


def handler_user_logged_out(sender, **kwargs):
    event_user_logged_out.commit(
        actor=kwargs['user'], target=kwargs['user']
    )
