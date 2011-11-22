from converter.office_converter import OfficeConverter
from converter.exceptions import OfficeBackendError


try:
    office_converter = OfficeConverter()
except OfficeBackendError:
    office_converter = None
