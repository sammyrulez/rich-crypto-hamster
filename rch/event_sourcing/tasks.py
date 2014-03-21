from celery import shared_task


@shared_task
def store_event(event_name,payload):
    print "Async: %s" % event_name
    print "EndOf: %s" % event_name
