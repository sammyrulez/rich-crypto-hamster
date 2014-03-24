from celery import shared_task
from django.conf import settings
from event_sourcing import event_stored_fail, event_stored


@shared_task
def store_event(event_name,payload):
    print "Async: %s" % event_name
    try:
        if not settings.EVENT_SOURCING_STORAGE:
            raise Exception("EVENT_SOURCING_STORAGE setting missing")

        settings.EVENT_SOURCING_STORAGE.store_event(payload)
        event_stored.send("store_event",command=event_name,payload=payload)
    except Exception:
        event_stored_fail.send("store_event",command=event_name,payload=payload)

    print "EndOf: %s" % event_name
