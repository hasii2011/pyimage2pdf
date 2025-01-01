
from codeallybasic.DynamicConfiguration import KeyName
from codeallybasic.DynamicConfiguration import SectionName
from codeallybasic.DynamicConfiguration import Sections
from codeallybasic.DynamicConfiguration import DynamicConfiguration
from codeallybasic.DynamicConfiguration import StringList
from codeallybasic.DynamicConfiguration import ValueDescription
from codeallybasic.DynamicConfiguration import ValueDescriptions
from codeallybasic.SecureConversions import SecureConversions

from codeallybasic.SingletonV3 import SingletonV3


KEYWORDS_PROPERTY: StringList = StringList(['UML', 'Pyut', 'Diagram'])

SECTION_METADATA: ValueDescriptions = ValueDescriptions(
    {
        KeyName('author'):   ValueDescription(defaultValue='Humberto A. Sanchez II'),
        KeyName('producer'): ValueDescription(defaultValue='Pyut Plugin'),
        KeyName('title'):    ValueDescription(defaultValue='Pyut Diagram Dump'),
        KeyName('subject'):  ValueDescription(defaultValue='Developer Diagram'),
        KeyName('keywords'): ValueDescription(defaultValue=''),
        KeyName('keywords'): ValueDescription(defaultValue=KEYWORDS_PROPERTY, isStringList=True)
    }
)

# rect.left = 20.0
# rect.right = 200.0
# rect.top = newHeight - 2.0
# rect.bottom = newHeight - 50.0

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
    }
)


PYIMAGE2PDF_SECTIONS: Sections = Sections(
    {
        SectionName('MetaData'):    SECTION_METADATA,
        SectionName('Annotations'): SECTION_ANNOTATIONS,
    }
)


class Preferences(DynamicConfiguration, metaclass=SingletonV3):

    def __init__(self):

        super().__init__(baseFileName='pyimage2pdf.ini', moduleName='pyimage2pdf', sections=PYIMAGE2PDF_SECTIONS)

        self._configParser.optionxform = str  # type: ignore
