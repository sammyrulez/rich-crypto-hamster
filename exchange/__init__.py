from bson import Code
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from pymongo import MongoClient
from event_sourcing import event_stored
from event_sourcing.mongodb_event_storage import SOURCED_EVENTS


client = MongoClient(settings.EVENT_SOURCING_MONGODB_URL)
db = client[settings.EVENT_SOURCING_MONGODB_DBNAME]

balance_user_mapper_code = Code("""
               function () {
                    signed = this.payload.amount;
                    if(this.event == 'withdraw'){
                        signed = signed * -1;
                    }
                    emit(this.payload.user,signed);
               }
         """)
balance_exchange_mapper_code = Code("""
               function () {
                    signed = this.payload.amount;
                    if(this.event == 'withdraw'){
                        signed = signed * -1;
                    }
                    emit(1,signed);
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
                        signed = this.payload.amount * 0.5;
                    }
                    if(this.event == 'withdraw'){
                        signed = this.payload.amount * -0.5;
                    }
                    emit(1,signed);
               }
         """)
exchange_reduce_code = Code("""
                function (key, values) {
                  var volume = 0;
                  for (var i = values.length; i >=0 && i>  values.length - 10 ; i--) {
                    if(values[i]){
                        volume = volume + values[i];
                    }
                  }
                  return volume;
                }
         """)

@receiver(event_stored)
def update_balance_on_event_stored(sender, **kwargs):
    collection = db[SOURCED_EVENTS]
    result = collection.map_reduce(balance_user_mapper_code, balance_reduce_code, "balance_results")
    from exchange import models
    for k in result.find():
            #print k
            if k['_id']:
                try:
                    user_data = User.objects.get(username = k['_id'] )
                    balance, created = models.Balance.objects.get_or_create(owner= user_data, defaults ={'current_value':k['value'] })
                    balance.current_value = k['value']
                    print balance
                    balance.save()
                except Exception as e:
                    print 'Error', e

@receiver(event_stored)
def update_exchange_ratio_on_event_stored(sender, **kwargs):
    collection = db[SOURCED_EVENTS]
    result = collection.map_reduce(exchange_ratio_mapper_code, exchange_reduce_code, "volume_results")
    total = collection.map_reduce(balance_exchange_mapper_code, balance_reduce_code, "total_results")
    t = total.find_one()['value']
    print 'total ', t
    from exchange import models
    k = result.find_one()['value']
    ratio = (100 * k ** 1.19) / t
    print 'update_exchange_ratio_on_event_stored ', ratio
