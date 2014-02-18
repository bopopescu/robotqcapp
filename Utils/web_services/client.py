from suds.client import Client
c = Client('http://localhost:7789/?wsdl')
c.service.say_hello('punk', 5)
