import simplejson
from django.forms import Widget
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt

class JsonPairInputs(Widget):
    """
    :author: Huy Nguyen
    
    A widget that displays JSON Key Value Pairs as a list of text input box pairs
    
    Usage (in forms.py)::
    jsonfield = forms.CharField(
        label="Example JSON Key Value Field", 
        required = False,
        widget = JsonPairInputs(
            val_attrs={'size':35},
            key_attrs={'class':'large'}
        )
    )
    """
    def __init__(self, key_attrs={}, val_attrs={}, *args, **kwargs):
        """
        :param key_attrs: HTML attributes applied to the 1st input box
        :param val_attrs: HTML attributes applied to the 2nd input box
        """
        self.key_attrs = key_attrs
        self.val_attrs = val_attrs
        Widget.__init__(self, *args, **kwargs)
    
    def render(self, name, value, attrs=None):
        """
        Renders this widget into an HTML string
        
        :param name:  Name of the field
        :type name:   str
        :param value: A json string of a two-tuple list automatically passed in by django
        :type value:  str
        :param attrs: automatically passed in by django (unused in this function)
        :type attrs:  dict
        """
        if value is None or value.strip() is '': 
            value = '{}'
        twotuple = simplejson.loads(force_unicode(value))
        
        ret = []
        if value and len(value) > 0:
            for k,v in twotuple:
                ctx = {'key':k,
                       'value':v,
                       'fieldname':name,
                       'key_attrs': flatatt(self.key_attrs),
                       'val_attrs': flatatt(self.val_attrs) }
                ret.append('<input type="text" name="json_key[%(fieldname)s]" value="%(key)s" %(key_attrs)s> <input type="text" name="json_value[%(fieldname)s]" value="%(value)s" %(val_attrs)s><br />' % ctx)
        return mark_safe("".join(ret))
    
    def value_from_datadict(self, data, files, name):
        """
        Returns the simplejson representation of the key-value pairs
        sent in the POST parameters
        
        :param data:  request.POST or request.GET parameters
        :type data:   dict
        :param files: request.FILES
        :type files:  list
        :param name:  The name of the field associated with this widget
        :type name:   str
        """
        if data.has_key('json_key[%s]' % name) and data.has_key('json_value[%s]' % name):
            keys     = data.getlist("json_key[%s]" % name)
            values   = data.getlist("json_value[%s]" % name)
            twotuple = []
            for key, value in zip(keys, values):
                if len(key) > 0:
                    twotuple += [(key,value)]
            jsontext = simplejson.dumps(twotuple)
        return jsontext


class MarkItUpWidget(Widget):
