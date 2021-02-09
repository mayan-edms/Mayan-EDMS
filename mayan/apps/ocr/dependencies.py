from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import BinaryDependency

from .backends.tesseract import Tesseract

tesseract = Tesseract(auto_initialize=False)
tesseract.read_settings()

BinaryDependency(
    copyright_text='''
        The code in this repository is licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

           http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
    ''', help_text=_('Free Open Source OCR Engine'), label='Tesseract',
    module=__name__, name='tesseract', path=tesseract.tesseract_binary_path
)
