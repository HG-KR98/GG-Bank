from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    opts = instance._meta
    data = DotDict()
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data


class DotDict(dict):
    # obj.key
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return self.key

    def __setattr__(self, key, value):
        self[key] = value
