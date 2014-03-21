from celery import shared_task
from event_sourcing import event_stored_fail, event_stored


@shared_task
def store_event(event_name,payload):
    print "Async: %s" % event_name
    print "EndOf: %s" % event_name
    try:
        event_stored.send("store_event",command=event_name,payload=payload)
    except Exception:
        event_stored_fail.send("store_event",command=event_name,payload=payload)
