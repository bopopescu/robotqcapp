__author__ = 'Administrator'
from datable.web.columns import *
from datable.core.serializers import UnicodeSerializer

class ButtonColumn(Column):
    formatter = 'button'
    sortable = False
class IntegerColumn(Column):
    formatter = 'integer'
    sortable = True
class ButtonS3FileColumn(Column):
    formatter = 'buttonS3File'
    sortable = False
class JsonButtonColumn(Column):
    formatter = 'jsonButton'
    sortable = False
class SelectionColumn(Column):
    formatter = 'checkbox'
    sortable = False

class IntegerSerializer(UnicodeSerializer):
    """
    Serialize one of model's fields to a textBox
    """
    def __init__(self):
        # These values are created
        # when the class is instantiated.
        pass
    def serialize(self, model, output_format=None):
        return str(model.amount)
class ButtonSerializer(UnicodeSerializer):
    """
    Serialize one of model's fields to a edit button.
    """
    def __init__(self, _url,_title,_pk_name):
        # These values are created
        # when the class is instantiated.
        self.url = _url
        self.title = _title
        self.pk_name = _pk_name
    def serialize(self, model, output_format=None):
        return str(model.pk),self.url,self.title,self.pk_name
class ButtonS3FileSerializer(UnicodeSerializer):
    """
    Serialize one of model's fields to a download file  button.
    """
    def __init__(self,_title):
        # These values are created
        # when the class is instantiated.
        self.title = _title
    def serialize(self, model, output_format=None):
        return '/s3FileDownload/'+str(model.id),self.title
class JsonButtonSerializer(UnicodeSerializer):
    """
    Serialize one of model's fields to a edit button.
    """
    def __init__(self, _url,_title,_pk_name):
        # These values are created
        # when the class is instantiated.
        self.url = _url
        self.title = _title
        self.pk_name = _pk_name
    def serialize(self, model, output_format=None):
        return str(model.pk),self.url,self.title,self.pk_name
class CheckBoxSerializer(UnicodeSerializer):
    """
    Serialize one of model's fields to a edit button.
    """
    def __init__(self, _checked,):
        # These values are created
        # when the class is instantiated.
        self.checked = _checked
    def serialize(self, model, output_format=None):
        return str(model.pk),self.checked