
from pathlib import Path

from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import StringList
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.PassThroughInterpolation import PassThroughInterpolation
from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3


KEYWORDS_PROPERTY:   StringList = StringList(['UML', 'Pyut', 'Diagram'])
DEFAULT_OUTPUT_PATH: Path       = Path('/tmp')

SECTION_GENERAL: ValueDescriptions = ValueDescriptions(
    {
        KeyName('outputPath'):       ValueDescription(defaultValue=str(DEFAULT_OUTPUT_PATH), deserializer=Path),
        KeyName('pdfEnlargeFactor'): ValueDescription(defaultValue='0.1', deserializer=SecureConversions.secureFloat),
    }
)


SECTION_METADATA: ValueDescriptions = ValueDescriptions(
    {
        KeyName('author'):   ValueDescription(defaultValue='Humberto A. Sanchez II'),
        KeyName('producer'): ValueDescription(defaultValue='Pyut Plugin'),
        KeyName('title'):    ValueDescription(defaultValue='Pyut Diagram Dump'),
        KeyName('subject'):  ValueDescription(defaultValue='Developer Diagram'),
        KeyName('keywords'): ValueDescription(defaultValue=KEYWORDS_PROPERTY, isStringList=True)
    }
)


SECTION_ANNOTATIONS: ValueDescriptions = ValueDescriptions(
    {
        KeyName('title'):  ValueDescription(defaultValue='Created by Pyut'),
        KeyName('bold'):   ValueDescription(defaultValue='True',  deserializer=SecureConversions.secureBoolean),
        KeyName('italic'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('italic'): ValueDescription(defaultValue='False', deserializer=SecureConversions.secureBoolean),
        KeyName('annotationLeft'):         ValueDescription(defaultValue='20.0',  deserializer=SecureConversions.secureFloat),
        KeyName('annotationRight'):        ValueDescription(defaultValue='200.0', deserializer=SecureConversions.secureFloat),
        KeyName('annotationTopOffset'):    ValueDescription(defaultValue='2.0',   deserializer=SecureConversions.secureFloat),
        KeyName('annotationBottomOffset'): ValueDescription(defaultValue='50.0',  deserializer=SecureConversions.secureFloat),
        KeyName('dateFormat'):             ValueDescription(defaultValue='%d %b %Y %H:%M'),
    }
)


PYIMAGE2PDF_SECTIONS: Sections = Sections(
    {
        SectionName('General'):     SECTION_GENERAL,
        SectionName('MetaData'):    SECTION_METADATA,
        SectionName('Annotations'): SECTION_ANNOTATIONS,
    }
)


class Preferences(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):

        passThroughInterpolation: PassThroughInterpolation = PassThroughInterpolation(
            ['dateFormat']
        )

        super().__init__(baseFileName='pyimage2pdf.ini', moduleName='pyimage2pdf', sections=PYIMAGE2PDF_SECTIONS, interpolation=passThroughInterpolation)

        self._configParser.optionxform = str  # type: ignore
