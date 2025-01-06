
from logging import Logger
from logging import getLogger

from pathlib import Path

from PIL import UnidentifiedImageError
from click import ClickException

from click import Path as clickPath
from click import command
from click import option
from click import version_option

from click import secho as clickSEcho

from pyimage2pdf import __version__ as pyImage2PdfVersion

from pyimage2pdf.PyImage2Pdf import OUTPUT_SUFFIX
from pyimage2pdf.PyImage2Pdf import PyImage2Pdf


class CommandClass:

    def __init__(self, inputFileName: Path, outputFileName: Path):
        self.logger: Logger = getLogger(__name__)

        self._inputFileName: Path = inputFileName

        if outputFileName is None:
            clickSEcho('Using input file name as base for output file name', bold=True)
            baseName: str = inputFileName.stem
            self._outputFileName: Path = Path(f'{baseName}.{OUTPUT_SUFFIX}')
            clickSEcho(f'Output file name is: {self._outputFileName}', bold=True)
        else:
            self._outputFileName = outputFileName

    def convert(self):
        pyimage2pdf: PyImage2Pdf = PyImage2Pdf()

        try:
            pyimage2pdf.convert(imagePath=self._inputFileName, pdfPath=self._outputFileName)
        except UnidentifiedImageError:
            raise ClickException('The input file does not appear to be an image file')


@command()
@version_option(version=f'{pyImage2PdfVersion}', message='%(version)s')
@option('-i', '--input-file',  required=True,  type=clickPath(readable=True, exists=True,  path_type=Path), help='The input image file name to convert.')
@option('-o', '--output-file', required=False, type=clickPath(writable=True,               path_type=Path), help='The output pdf file name.')
def commandHandler(input_file: Path, output_file: Path):
    """
    \b
    This command converts input image files to pdf;  If
    you omit the output file name the command deduces the name
    based on the input file name
    """

    commandClass: CommandClass = CommandClass(inputFileName=input_file, outputFileName=output_file)

    commandClass.convert()


if __name__ == "__main__":

    # commandHandler(['-i', 'tests/resources/images/Tailor.jpg'])
    # commandHandler(['-i', 'tests/resources/images/Tailor.jpg', '-o', 'junk.pdf'])
    commandHandler(['-i', 'tests/resources/images/CorruptedImage.png'])
