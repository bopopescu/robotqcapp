import logging

from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.complex import Iterable
from spyne.model.primitive import Integer
from spyne.model.primitive import Unicode

from spyne.util.simple import wsgi_soap_application


class SomeObject(ComplexModel):
    __namespace__ = 'spyne.examples.hello.soap'

    i = Integer
    s = Unicode


class HelloWorldService(ServiceBase):
    __out_header__ = SomeObject
    @srpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(name, times):
        '''
        Docstrings for service methods appear as documentation in the wsdl
        <b>what fun</b>
        @param name the name to say hello to
        @param the number of times to say hello
        @return the completed array
        '''

        for i in range(times):
            yield u'Hello, %s' % name


if __name__=='__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:7789")
    logging.info("wsdl is at: http://localhost:7789/?wsdl")

    wsgi_app = wsgi_soap_application([HelloWorldService], 'spyne.examples.hello.soap')
    server = make_server('127.0.0.1', 7789, wsgi_app)
    server.serve_forever()