__author__ = 'Administrator'
from django import template
from django.template.loader import get_template
from  Utils import parsers
class ButtonNode(template.Node):
    def __init__(self, vals):
        self.action = template.Variable(vals[1])
        self.name = template.Variable(vals[2])
    def render(self, context):
        return get_template('button_widget.html').render(template.Context({'action':self.action,'name':self.name}))
class PkNode(template.Node):
    def __init__(self, vals):
            self.pk = template.Variable(vals[1])
    def render(self, context):
        context_pk = self.pk.resolve(context)
        actual_key = context_pk.form.initial['code']
        return actual_key
register = template.Library()
def checkboxFunc():
    return {}
def checkbox_utils():
    return {}
def editButtonFunc():
    return {}
def hrefButtonFunc():
    return {}
def tableButtonFunc():
    return {}
def generic_buttonFunc(self,token):
    vals = token.split_contents()
    for i in range(0,len(vals)):
        vals[i] = parsers.clean_alphabet_string_from_garbage(['\"'],vals[i])
    return ButtonNode(vals)
def get_pk_from_form(self,token):
    vals = token.split_contents()
    return PkNode(vals)
def checkbox_button():
    return {}
def new_project_button():
    return {}
def progress_bar():
    return {}
def run_step():
    return {}
register.inclusion_tag('checkbox_utils.html')(checkbox_utils)
register.inclusion_tag('checkbox_button.html')(checkbox_button)
register.inclusion_tag('row_button.html')(tableButtonFunc)
register.inclusion_tag('new_project_button.html')(new_project_button)
register.inclusion_tag('progressBar.html')(progress_bar)
register.inclusion_tag('runStepUtils.html')(run_step)
register.tag('generic_buttonFunc')(generic_buttonFunc)
register.tag('get_pk_from_form', get_pk_from_form)
