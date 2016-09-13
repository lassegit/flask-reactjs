from app.models.database import db
import app.helper as helper

class Serializable(object):
    @property
    def serialized(self):
        blacklist = ['_sa_instance_state']
        blacklist.extend(getattr(self, '_serialize_blacklist', []))
        result = {}

        for k,v in self.__dict__.items():
            if k in blacklist:
                continue
            elif isinstance(v, list): # One to Many/Many to Many relationship, add a list of serialized child objects
                result[k] = [i.serialized for i in v]
            elif isinstance(v, db.Model): # One to One relationship, serialize the child and include it
                result[k] = v.serialized
            elif isinstance(v, decimal.Decimal):
                result[k] = str(v)
            else:
                if k in ['created_at', 'updated_at']:
                    result[k] = {
                        'date': v,
                        'timeago': helper.timeago(v)
                    }
                else:
                    result[k] = v
        
        return result
