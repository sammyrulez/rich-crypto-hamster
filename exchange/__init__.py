from bson import Code
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from pymongo import MongoClient
from event_sourcing import event_stored
from event_sourcing.mongodb_event_storage import SOURCED_EVENTS


client = MongoClient(settings.EVENT_SOURCING_MONGODB_URL)
db = client[settings.EVENT_SOURCING_MONGODB_DBNAME]

balance_mapper_code = Code("""
               function () {
                    signed = this.payload.amount;
                    if(this.event == 'withdraw'){
                        signed = signed * -1;
                    }
                    emit(this.payload.user,signed);
               }
         """)
balance_reduce_code = Code("""
                function (key, values) {
                  var balance = 0;
                  for (var i = 0; i < values.length; i++) {
                    balance += values[i];
                  }
                  return balance;
                }
         """)

exchange_ratio_mapper_code = Code("""
               function () {
                    signed = 0;
                    if(this.event == 'deposit'){
                        signed = this.payload.amount * -1;
                    }
                    if(this.event == 'withdraw'){
                        signed = this.payload.amount;
                    }
                    emit(z,signed);
               }
         """)
exchange_reduce_code = Code("""
                function (key, values) {
                  var ratio = 1;
                  for (var i = 0; i < values.length; i++) {
                    balance += values[i];
                  }
                  return balance;
                }
         """)#TODO

@receiver(event_stored)
def update_balance_on_event_stored(sender, **kwargs):
    print "storing from ", settings.EVENT_SOURCING_MONGODB_DBNAME, " ", SOURCED_EVENTS
    collection = db[SOURCED_EVENTS]
    result = collection.map_reduce(balance_mapper_code, balance_reduce_code, "balance_results")
    from exchange import models
    for k in result.find():
            print k
            if k['_id']:
                try:
                    user_data = User.objects.get(username = k['_id'] )
                    balance, created = models.Balance.objects.get_or_create(owner= user_data, defaults ={'current_value':k['value'] })
                    balance.current_value = k['value']
                    print balance
                    balance.save()
                except Exception as e:
                    print 'Error' , e