
from typing import cast
from typing import List
from typing import NewType
from typing import Optional
from typing import IO

from logging import Logger
from logging import getLogger

from dataclasses import dataclass
from dataclasses import field

from tempfile import NamedTemporaryFile

from pathlib import Path

from PIL.ImageFile import ImageFile
from PIL.Image import Image
from PIL.Image import open as pilOpen

from pypdf import DocumentInformation
from pypdf import PageObject
from pypdf import PdfReader
from pypdf import PdfWriter
from pypdf.annotations import FreeText
from pypdf.annotations import MarkupAnnotation
from pypdf.constants import AnnotationFlag
from pypdf.generic import FloatObject
from pypdf.generic import RectangleObject

from pyimage2pdf.Preferences import Preferences


OUTPUT_SUFFIX: str = 'pdf'


@dataclass
class Dimensions:
    width:  float = 0.9
    height: float = 0.0


KeyWordList = NewType('KeyWordList', List[str])


def keyWordsFactory() -> KeyWordList:
    return KeyWordList([])


@dataclass
class PdfMetaData:
    author:         str = ''
    producer:       str = ''
    title:          str = ''
    subject:        str = ''
    keywords:       KeyWordList = field(default_factory=keyWordsFactory)


def pdfMetaDataFactory() -> PdfMetaData:
    return PdfMetaData()


@dataclass
class PdfOptions:
    annotationText:         str   = ''
    annotationLeft:         float = 0.0
    annotationWidth:        float = 0.0
    annotationTopOffset:    float = 0.0
    annotationHeight:       float = 0.0
    pdfMetaData: PdfMetaData      = field(default_factory=pdfMetaDataFactory)


class PyImage2Pdf:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._preferences: Preferences = Preferences()

    def convert(self, imagePath: Path, pdfPath: Optional[Path] = None, pdfOptions: Optional[PdfOptions] = None):
        """

        Args:
            imagePath:  the image path
            pdfPath:    Where to put the output pdf.  If not set use the preferences version
            pdfOptions: Override the internal options
        """
        actualOptions: PdfOptions = PdfOptions()
        if pdfOptions is None:
            actualOptions = self._retrievePreferences()
        else:
            actualOptions.pdfMetaData = pdfOptions.pdfMetaData

            actualOptions.annotationText       = pdfOptions.annotationText
            actualOptions.annotationLeft       = pdfOptions.annotationLeft
            actualOptions.annotationWidth      = pdfOptions.annotationWidth
            actualOptions.annotationTopOffset  = pdfOptions.annotationTopOffset
            actualOptions.annotationHeight     = pdfOptions.annotationHeight

        tmpPdfFileNamePath: Path       = self._createInitialPdf(imagePath, metadata=actualOptions.pdfMetaData)
        pdfReader:          PdfReader  = PdfReader(tmpPdfFileNamePath)
        singlePdfPage:      PageObject = pdfReader.pages[0]

        self.logger.debug(f'{tmpPdfFileNamePath=}')
        newDimensions: Dimensions = self._computeEnlargedPdfSize(singlePdfPage=singlePdfPage, factor=self._preferences.pdfEnlargeFactor)
        self.logger.debug(f'{newDimensions=}')

        if pdfPath is None:
            outputPath: Path = self._generateTheFinalOutputPath(originalImageFilePath=imagePath)
        else:
            outputPath = pdfPath

        self._createEnlargedPdfDocument(pageDimensions=newDimensions,
                                        metadata=cast(DocumentInformation, pdfReader.metadata),
                                        pdfOptions=actualOptions,
                                        singlePdfPage=singlePdfPage, outputPath=outputPath)

    def _createInitialPdf(self, imagePath: Path, metadata: PdfMetaData) -> Path:
        """
        Create a temporary PDF file
        Args:
            imagePath:   The path to the image

        Returns:  The the path to the pdf file
        """

        imageToConvert:  ImageFile   = pilOpen(imagePath)
        convertedImage:  Image       = imageToConvert.convert('RGB')
        tempPdfFile:     IO          = NamedTemporaryFile(delete=False, suffix='.pdf')
        pdfFileNamePath: Path        = Path(tempPdfFile.name)

        """
        The output format is deduced from the file extension
        https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html
        """
        convertedImage.save(pdfFileNamePath,
                            author=metadata.author,
                            producer=metadata.producer,
                            title=metadata.title,
                            subject=metadata.subject,
                            keywords=','.join(metadata.keywords)
                            )

        return pdfFileNamePath

    def _computeEnlargedPdfSize(self, singlePdfPage: PageObject, factor: float) -> Dimensions:
        """
        Compute the new pageDimensions
        Args:
            singlePdfPage:
            factor:

        Returns:  The new pageDimensions

        """
        mediaBox: RectangleObject = singlePdfPage.mediabox

        self.logger.info(f'{mediaBox.width=} {mediaBox.height}')

        additionalHeight: float = mediaBox.height * factor
        newWidth:         float = mediaBox.width
        newHeight:        float = mediaBox.height + additionalHeight

        return Dimensions(width=newWidth, height=newHeight)

    def _createEnlargedPdfDocument(self,
                                   pageDimensions: Dimensions,
                                   metadata:       DocumentInformation,
                                   pdfOptions:     PdfOptions,
                                   singlePdfPage:  PageObject,
                                   outputPath:     Path):
        """
        Will be enlarged and we will add a custom annotation
        Args:
            pageDimensions:
            singlePdfPage:
            outputPath:

        Returns:

        """
        newPage: PageObject = PageObject.create_blank_page(width=pageDimensions.width, height=pageDimensions.height)
        newPage.merge_page(singlePdfPage)

        pdfWriter: PdfWriter = PdfWriter()

        pdfWriter.add_page(newPage)

        pdfWriter.metadata = metadata
        annotation: MarkupAnnotation = self._generateCustomAnnotation(pageDimensions, pdfOptions=pdfOptions)
        pdfWriter.add_annotation(page_number=0, annotation=annotation)

        pdfWriter.write(outputPath)

    def _generateCustomAnnotation(self, pageDimensions: Dimensions, pdfOptions: PdfOptions) -> MarkupAnnotation:

        rect: RectangleObject = RectangleObject((0, 0, 0, 0))
        rect.left   = FloatObject(pdfOptions.annotationLeft)
        rect.right  = FloatObject(pdfOptions.annotationLeft + pdfOptions.annotationWidth)
        rect.top    = FloatObject(pageDimensions.height - pdfOptions.annotationTopOffset)
        rect.bottom = FloatObject(rect.top - pdfOptions.annotationHeight)

        annotation:   FreeText = FreeText(
            text=f'{pdfOptions.annotationText}',
            rect=rect,
            font="PT Mono",
            bold=True,
            italic=False,
            font_size="32pt",
            font_color="00ff00",
            # border_color="0000ff",
            background_color="ffffff",
        )

        annotation.flags = AnnotationFlag.PRINT

        return annotation

    def _generateTheFinalOutputPath(self, originalImageFilePath: Path):
        """

        Args:
            originalImageFilePath:

        Returns:  The combination of the original file name with the pdf suffix
        and using the preferences output path

        """

        bareName: str = originalImageFilePath.stem

        fullPath: Path = self._preferences.outputPath / f'{bareName}.{OUTPUT_SUFFIX}'

        return fullPath

    def _retrievePreferences(self) -> PdfOptions:

        actualOptions: PdfOptions = PdfOptions()

        metadata: PdfMetaData = PdfMetaData(author=self._preferences.author,
                                            producer=self._preferences.producer,
                                            title=self._preferences.title,
                                            subject=self._preferences.subject,
                                            keywords=self._preferences.keywords)
        actualOptions.pdfMetaData = metadata
        from time import strftime

        creationDate: str = strftime(self._preferences.dateFormat)
        annotationText: str = f'{self._preferences.title} - {creationDate}'

        actualOptions.annotationText         = annotationText
        actualOptions.annotationLeft         = self._preferences.annotationLeft
        actualOptions.annotationWidth        = self._preferences.annotationWidth
        actualOptions.annotationTopOffset    = self._preferences.annotationTopOffset
        actualOptions.annotationHeight       = self._preferences.annotationHeight

        return actualOptions
