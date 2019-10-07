# ashokkumar.ta@gmail.com / 11-Jul-2019

from dampy import AEM

class Test_Dampy:

    def test_connect(self):
        aem = AEM("http://localhost:5502")
        assert aem is not None

    def test_list(self):
        aem = AEM("http://localhost:5502")
        list = aem.dam.list('/content/dam/we-retail/en/products/apparel/shorts')
        assert list is not None

