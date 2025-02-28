
from unittest import TestSuite
from unittest import main as unitTestMain

from os import linesep as osLineSep

from click.testing import CliRunner
from click.testing import Result

from codeallybasic.UnitTestBase import UnitTestBase

from pyimage2pdf.CommandClass import commandHandler

from pyimage2pdf import __version__ as pyImage2PdfVersion


class TestCommandClass(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 09 January 2025
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testHelp(self):
        runner: CliRunner = CliRunner()
        result: Result    = runner.invoke(commandHandler, ['--help'])

        self.assertEqual(0, result.exit_code, 'Oops, help stopped working')

    def testVersion(self):

        runner: CliRunner = CliRunner()
        result: Result    = runner.invoke(commandHandler, ['--version'])

        self.assertEqual(f'{pyImage2PdfVersion}{osLineSep}', result.output, 'Version mismatch')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestCommandClass))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
