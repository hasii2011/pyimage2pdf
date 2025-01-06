
from typing import IO

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from tempfile import NamedTemporaryFile

from pathlib import Path
from typing import Optional

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


class PyImage2Pdf:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._preferences: Preferences = Preferences()

    def convert(self, imagePath: Path, pdfPath: Optional[Path] = None):
        """

        Args:
            imagePath:  the image path
            pdfPath:    Where to put the output pdf.  If not set use the preferences version

        """

        tmpPdfFileNamePath: Path = self._createInitialPdf(imagePath)

        pdfReader:     PdfReader   = PdfReader(tmpPdfFileNamePath)
        singlePdfPage: PageObject = pdfReader.pages[0]

        self.logger.debug(f'{tmpPdfFileNamePath=}')
        newDimensions: Dimensions = self._computeEnlargedPdfSize(singlePdfPage=singlePdfPage, factor=self._preferences.pdfEnlargeFactor)

        self.logger.debug(f'{newDimensions=}')

        if pdfPath is None:
            outputPath: Path = self._generateTheFinalOutputPath(originalImageFilePath=imagePath)
        else:
            outputPath = pdfPath

        self._createEnlargedPdfDocument(pageDimensions=newDimensions,
                                        metadata=pdfReader.metadata,
                                        singlePdfPage=singlePdfPage, outputPath=outputPath)

    def _createInitialPdf(self, imagePath: Path) -> Path:
        """
        Create a temporary PDF file
        Args:
            imagePath:   The path to the image

        Returns:  The the path to the pdf file
        """

        preferences:     Preferences = self._preferences
        imageToConvert:  ImageFile   = pilOpen(imagePath)
        convertedImage:  Image       = imageToConvert.convert('RGB')
        tempPdfFile:     IO          = NamedTemporaryFile(delete=False, suffix='.pdf')
        pdfFileNamePath: Path        = Path(tempPdfFile.name)

        # The output format is deduced from the file extension
        # https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html
        convertedImage.save(pdfFileNamePath,
                            author=preferences.author,
                            producer=preferences.producer,
                            title=preferences.title,
                            subject=preferences.subject,
                            keywords=','.join(preferences.keywords),
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
                                   metadata:   DocumentInformation | None,
                                   singlePdfPage: PageObject,
                                   outputPath: Path):
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
        annotation: MarkupAnnotation = self._generateCustomAnnotation(pageDimensions)
        pdfWriter.add_annotation(page_number=0, annotation=annotation)

        pdfWriter.write(outputPath)

    def _generateCustomAnnotation(self, pageDimensions: Dimensions) -> MarkupAnnotation:

        from time import strftime

        creationDate: str = strftime(self._preferences.dateFormat)

        rect: RectangleObject = RectangleObject((0, 0, 0, 0))
        rect.left   = FloatObject(self._preferences.annotationLeft)
        rect.right  = FloatObject(self._preferences.annotationRight)
        rect.top    = FloatObject(pageDimensions.height - self._preferences.annotationTopOffset)
        rect.bottom = FloatObject(pageDimensions.height - self._preferences.annotationBottomOffset)

        annotation:   FreeText = FreeText(
            text=f'{self._preferences.title} - {creationDate}',
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
