from celery import shared_task
from django.conf import settings
from event_sourcing import event_stored_fail, event_stored
import importlib


def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

instance = load_class(settings.EVENT_SOURCING_STORAGE)


@shared_task
def store_event(event_name, payload):
    print "Async: %s" % event_name
    try:
        instance.store_event({'event': event_name, 'payload': payload})
        event_stored.send("store_event", command=event_name, payload=payload)
    except Exception:
        event_stored_fail.send("store_event", command=event_name, payload=payload)

    print "EndOf: %s" % event_name
