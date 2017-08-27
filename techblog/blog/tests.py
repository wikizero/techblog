from django.test import TestCase

# Create your tests here.

import pdfkit


pdfkit.from_url('https://pypi.python.org/pypi/pdfkit', 'out.pdf')
