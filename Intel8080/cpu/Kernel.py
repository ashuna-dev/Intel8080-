import logging
from cpu import CPU

class IntelKernel(object):
    logger = logging.getLogger('Intel Kernel')

    def __init__(self, filename):
        self._CPU = CPU()

        if not filename:
            return

        try:
            with open(filename, 'rb') as f:
                self._CPU.load(f.read())
        except FileNotFoundError as e:
            IntelKernel.logger.error(e)
            exit()

    def boot(self):
        self._CPU.start()
        IntelKernel.logger.info('Booted system')

    def _get_test_suite(self):
        from unittest import TestSuite, defaultTestLoader
        import tests as tests1

        suite = TestSuite()

        for t in (tests1, ):
            suite.addTests(defaultTestLoader.loadTestsFromModule(t))

        return suite

    def run_tests(self):
        from unittest import TextTestRunner

        IntelKernel.logger.info('Running test suite')
        suite = self._get_test_suite()
        TextTestRunner().run(suite)

        IntelKernel.logger.info('Test suite finished')
