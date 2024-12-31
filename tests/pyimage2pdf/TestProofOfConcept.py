
from datetime import datetime

from os import pathsep as osPathSep

from pathlib import Path
from typing import Optional
from typing import cast

from PIL.Image import Image
from PIL.Image import open as pilOpen
from PIL.ImageFile import ImageFile

from pypdf import DocumentInformation
from pypdf import PageObject
from pypdf import PdfReader
from pypdf import PdfWriter

from pypdf.annotations import FreeText
from pypdf.constants import AnnotationFlag
from pypdf.generic import RectangleObject

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.ResourceManager import ResourceManager
from codeallybasic.UnitTestBase import UnitTestBase

IMAGE_FILE_NAME:    str  = 'CompactImageDump.png'
PDF_FILE_NAME:      str  = 'CompactImageDump.pdf'
PDF_FILE_NAME_PATH: Path = Path(PDF_FILE_NAME)

UPDATED_META_DATA_PDF: Path = Path('CompactImageDumpUpdateMeta.pdf')
SCALED_PAGE_PATH:      Path = Path('CompactImageDumpScaled.pdf')

MST_OFFSET: str = "-05'00'"


class TestProofOfConcept(UnitTestBase):
    # noinspection SpellCheckingInspection
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 26 December 2024

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=`.png`)
    """

    IMAGES_RESOURCE_PATH: str = f'resources{osPathSep}images'
    IMAGES_PACKAGE_NAME:  str = f'{UnitTestBase.RESOURCES_PACKAGE_NAME}.images'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testBasic(self):
        basicPath: Path = ResourceManager.computeResourcePath(resourcePath=TestProofOfConcept.IMAGES_RESOURCE_PATH,
                                                              packageName=TestProofOfConcept.IMAGES_PACKAGE_NAME)

        fqPath:         Path      = basicPath / IMAGE_FILE_NAME
        imageToConvert: ImageFile = pilOpen(fqPath)
        convertedImage: Image     = imageToConvert.convert('RGB')

        # The output format is deduced from the file extension
        # https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html
        convertedImage.save(PDF_FILE_NAME_PATH,
                            author='Humberto A. Sanchez II',
                            producer='Pyut Plugin',
                            title='Pyut Diagram Dump',
                            subject='Developer Diagram',
                            keywords='UML',
                            )

        self._readPDFMetaData(PDF_FILE_NAME_PATH, title='Meta Data from PDF Conversion')

        # self._updateMetaData(PDF_FILE_NAME_PATH)

        # self._readPDFMetaData(UPDATED_META_DATA_PDF, title='After meta data update')

        self._scalePages(PDF_FILE_NAME_PATH)

    def _readPDFMetaData(self, filePath: Path, title: str):

        reader: PdfReader = PdfReader(filePath)

        docInfo: Optional[DocumentInformation] = reader.metadata

        self.logger.info('---------------------')
        self.logger.info(f'{title}')
        self.logger.info('---------------------')
        documentationInformation: DocumentInformation = cast(DocumentInformation, docInfo)

        self.logger.info(f'{documentationInformation.title=}')
        self.logger.info(f'{documentationInformation.author=}')
        self.logger.info(f'{documentationInformation.subject=}')
        self.logger.info(f'{documentationInformation['/Keywords']=}')
        self.logger.info(f'{documentationInformation.title=}')
        self.logger.info(f'{documentationInformation.producer=}')
        self.logger.info(f'{documentationInformation.creation_date=}')
        self.logger.info(f'{documentationInformation.modification_date=}')

    def _updateMetaData(self, filePath: Path):

        pdfReader: PdfReader = PdfReader(filePath)
        pdfWriter: PdfWriter = PdfWriter()

        # Add all pages to the writer
        for page in pdfReader.pages:
            pdfWriter.add_page(page)

        # Format the current date and time for the metadata
        utcTime: str = MST_OFFSET   # UTC time optional
        time = datetime.now().strftime(f"D\072%Y%m%d%H%M%S{utcTime}")

        # Add the new metadata
        pdfWriter.add_metadata(
            {
                "/Author": "Humberto A. Sanchez II",
                "/Producer": "Pyut Plugin",
                "/Title": "Pyut Diagram Dump",
                "/Subject": "Developer",
                "/Keywords": "UML",
                "/CreationDate": time,
                "/ModDate": time,
                "/Creator": "Pyut",
                "/Nickname": "El Gato Malo",
            }
        )

        # Save the new PDF to a file
        with open(UPDATED_META_DATA_PDF, "wb") as f:
            pdfWriter.write(f)

    def _scalePages(self, filePath: Path, factor: float = 0.1):

        pdfReader: PdfReader = PdfReader(filePath)
        pdfWriter: PdfWriter = PdfWriter()

        singlePage: PageObject = pdfReader.pages[0]

        mediaBox: RectangleObject = singlePage.mediabox

        self.logger.info(f'{mediaBox.width=} {mediaBox.height}')

        additionalHeight: float = mediaBox.height * factor
        newWidth:         float = mediaBox.width
        newHeight:        float = mediaBox.height + additionalHeight

        newPage: PageObject = PageObject.create_blank_page(width=newWidth, height=newHeight)
        newPage.merge_page(singlePage)

        pdfWriter.add_page(newPage)

        left: float   = 20
        top    = newHeight - 10
        right  = 300
        bottom = 650
        annotation: FreeText = FreeText(
            text="Created by Pyut 9.6.0",
            rect=(left, bottom, right, top),
            font="Arial",
            bold=True,
            italic=False,
            font_size="32pt",
            font_color="000000",
            # border_color="0000ff",
            # background_color="ffffff",
        )

        annotation.flags = AnnotationFlag.PRINT
        pdfWriter.add_annotation(page_number=0, annotation=annotation)

        pdfWriter.add_metadata(pdfReader.metadata)      # type: ignore
        pdfWriter.write(SCALED_PAGE_PATH)


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestProofOfConcept))

    return testSuite


if __name__ == '__main__':
    unitTestMain()