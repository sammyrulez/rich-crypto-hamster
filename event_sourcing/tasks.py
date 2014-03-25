from celery import shared_task
from django.conf import settings
from event_sourcing import event_stored_fail, event_stored

storage_split = settings.EVENT_SOURCING_STORAGE.split('.')
module = __import__(storage_split[0])
print storage_split[0]
for sub in storage_split[1:len(storage_split) - 1]:
    print dir(module), sub
    module = getattr(module, sub)

instance = getattr(module, storage_split[len(storage_split)-1])


@shared_task
def store_event(event_name,payload):
    print "Async: %s" % event_name
    try:
        instance.store_event(payload)
        event_stored.send("store_event", command=event_name,payload=payload)
    except Exception:
        event_stored_fail.send("store_event", command=event_name,payload=payload)

    print "EndOf: %s" % event_name
