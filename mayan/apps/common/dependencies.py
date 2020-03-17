from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.classes import (
    environment_build, environment_development, environment_documentation,
    environment_testing, BinaryDependency, PythonDependency
)

from .literals import DEFAULT_FIREFOX_GECKODRIVER_PATH

PythonDependency(
    copyright_text='''
        Copyright (c) Django Software Foundation and individual contributors.
        All rights reserved.

        Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.

        3. Neither the name of Django nor the names of its contributors may be used
        to endorse or promote products derived from this software without
        specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
        ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ''', module=__name__, name='django', version_string='==1.11.29'
)
PythonDependency(
    copyright_text='''
        Copyright (c) 2006 Kirill Simonov

        Permission is hereby granted, free of charge, to any person obtaining a copy of
        this software and associated documentation files (the "Software"), to deal in
        the Software without restriction, including without limitation the rights to
        use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
        of the Software, and to permit persons to whom the Software is furnished to do
        so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
    ''', module=__name__, name='PyYAML', version_string='==5.1.2'
)
PythonDependency(
    module=__name__, name='django-formtools', version_string='==2.1'
)
PythonDependency(
    copyright_text='''
        Copyright (c) James Pacileo and contributors.
        All rights reserved.

        Redistribution and use in source and binary forms, with or without modification,
        are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.

        3. Neither the name of Django nor the names of its contributors may be used
        to endorse or promote products derived from this software without
        specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
        ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
        ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ''', module=__name__, name='django-pure-pagination', version_string='==0.3.0'
)
PythonDependency(
    module=__name__, name='django-mathfilters', version_string='==0.4.0'
)
PythonDependency(
    copyright_text='''
        Copyright (c) 2009-2015, Carl Meyer and contributors
        All rights reserved.

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are
        met:

        * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above
        copyright notice, this list of conditions and the following
        disclaimer in the documentation and/or other materials provided
        with the distribution.
        * Neither the name of the author nor the names of other
        contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
        A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
        OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
        SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
        LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
        DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
        THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
        OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ''', module=__name__, name='django-model-utils', version_string='==3.1.2'
)
PythonDependency(
    copyright_text='''
        Django MPTT
        -----------

        Copyright (c) 2007, Jonathan Buchanan

        Permission is hereby granted, free of charge, to any person obtaining a copy of
        this software and associated documentation files (the "Software"), to deal in
        the Software without restriction, including without limitation the rights to
        use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
        the Software, and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
        FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
        COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
        IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
        CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    ''', module=__name__, name='django-mptt', version_string='==0.9.1'
)
PythonDependency(
    copyright_text='''
        Copyright (c) 2010, Matt Croydon, Mikhail Korobov
        All rights reserved.

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
        * Neither the name of the tastypie nor the
        names of its contributors may be used to endorse or promote products
        derived from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
        ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
        WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
        DISCLAIMED. IN NO EVENT SHALL MATT CROYDON BE LIABLE FOR ANY
        DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
        (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
        ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
        (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
        SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    ''', module=__name__, name='django-qsstats-magic', version_string='==1.0.0'
)
PythonDependency(
    module=__name__, name='django-stronghold', version_string='==0.3.0'
)
PythonDependency(
    copyright_text='''
        Copyright (c) 2011-2015 Mikhail Korobov

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        THE SOFTWARE.
    ''', module=__name__, name='django-widget-tweaks', version_string='==1.4.5'
)
PythonDependency(
    module=__name__, name='furl', version_string='==2.0.0'
)
PythonDependency(
    module=__name__, name='gevent', version_string='==1.4.0'
)
PythonDependency(
    module=__name__, name='gunicorn', version_string='==19.9.0'
)
PythonDependency(
    module=__name__, name='mock', version_string='==2.0.0'
)
PythonDependency(
    module=__name__, name='pathlib2', version_string='==2.3.5'
)
PythonDependency(
    copyright_text='''
        Author: Christian Theune
        License: LGPL 2.1
    ''', module=__name__, name='pycountry', version_string='==18.12.8'
)
PythonDependency(
    copyright_text='''
        Copyright (c) 2003-2005 Stuart Bishop <stuart@stuartbishop.net>

        Permission is hereby granted, free of charge, to any person obtaining a
        copy of this software and associated documentation files (the "Software"),
        to deal in the Software without restriction, including without limitation
        the rights to use, copy, modify, merge, publish, distribute, sublicense,
        and/or sell copies of the Software, and to permit persons to whom the
        Software is furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
        THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
        FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
        DEALINGS IN THE SOFTWARE.
    ''', module=__name__, name='pytz', version_string='==2019.1'
)
PythonDependency(
    module=__name__, name='requests', version_string='==2.21.0'
)
PythonDependency(
    copyright_text='''
        Copyright (C) 2011-2012 by Andrew Moffat

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        THE SOFTWARE.
    ''', module=__name__, name='sh', version_string='==1.12.14'
)
PythonDependency(
    module=__name__, name='whitenoise', version_string='==4.1.4'
)

# Development

PythonDependency(
    module=__name__, environment=environment_development, name='Werkzeug',
    version_string='==0.15.4'
)
PythonDependency(
    module=__name__, environment=environment_development, name='devpi-server',
    version_string='==5.3.1'
)
PythonDependency(
    environment=environment_development, module=__name__,
    name='django-debug-toolbar', version_string='==1.11'
)
PythonDependency(
    environment=environment_development, module=__name__,
    name='django-extensions', version_string='==2.1.9'
)
PythonDependency(
    environment=environment_development, help_text=_(
        'Used to allow offline translation of the code text strings.'
    ), module=__name__, name='django-rosetta', version_string='==0.9.3'
)
PythonDependency(
    environment=environment_development, help_text=_(
        'Provides style checking.'
    ), module=__name__, name='flake8', version_string='==3.7.9'
)
PythonDependency(
    environment=environment_development, help_text=_(
        'Command line environment with autocompletion.'
    ), module=__name__, name='ipython', version_string='==5.8.0'
)
PythonDependency(
    environment=environment_development, help_text=_(
        'Checks proper formatting of the README file.'
    ), module=__name__, name='readme', version_string='==0.7.1'
)
PythonDependency(
    environment=environment_development,
    module=__name__, name='safety', version_string='==1.8.5'
)
PythonDependency(
    environment=environment_development,
    module=__name__, name='transifex-client', version_string='==0.13.6'
)

# Testing

BinaryDependency(
    environment=environment_testing, label='firefox-geckodriver',
    module=__name__, name='geckodriver',
    path=DEFAULT_FIREFOX_GECKODRIVER_PATH
)
PythonDependency(
    environment=environment_testing, module=__name__, name='codecov',
    version_string='==2.0.15'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='coverage',
    version_string='==4.4.1'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='coveralls',
    version_string='==1.3.0'
)
PythonDependency(
    environment=environment_testing, module=__name__,
    name='django-test-migrations', version_string='==0.1.0'
)
PythonDependency(
    environment=environment_testing,
    module=__name__, name='django-test-without-migrations',
    version_string='==0.6'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='selenium',
    version_string='==3.141.0'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='tox',
    version_string='==3.8.6'
)
PythonDependency(
    environment=environment_testing, module=__name__, name='psutil',
    version_string='==5.7.0'
)

# Build

PythonDependency(
    environment=environment_build, module=__name__, name='twine',
    version_string='==1.9.1'
)
PythonDependency(
    environment=environment_build, module=__name__, name='wheel',
    version_string='==0.30.0'
)

# Documentation

PythonDependency(
    environment=environment_documentation, module=__name__, name='Sphinx',
    version_string='==1.8.5'
)
PythonDependency(
    environment=environment_documentation, module=__name__,
    name='sphinx-autobuild',
    version_string='==0.7.1'
)
PythonDependency(
    environment=environment_documentation, module=__name__,
    name='sphinx-sitemap',
    version_string='==1.0.2'
)
PythonDependency(
    environment=environment_documentation, module=__name__,
    name='sphinx_rtd_theme',
    version_string='==0.4.3'
)
PythonDependency(
    environment=environment_documentation, module=__name__,
    name='sphinxcontrib-blockdiag',
    version_string='==1.5.5'
)
PythonDependency(
    environment=environment_documentation, module=__name__,
    name='sphinxcontrib-spelling',
    version_string='==4.2.1'
)
# sphinx-autobuild has a dependency on Tornado,
# but Tornado 6.0 dropped support for Python 2.7
PythonDependency(
    environment=environment_documentation, module=__name__, name='tornado',
    version_string='<6.0'
)
