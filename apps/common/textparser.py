import codecs
import logging

from pygments import highlight
from pygments.lexers import TextLexer, guess_lexer, get_lexer_for_filename, ClassNotFound, get_lexer_for_mimetype
from pygments.formatters import ImageFormatter

DEFAULT_PAGE_WIDTH = 70
DEFAULT_PAGE_HEIGHT = 57
DEFAULT_LINE_NUMBER_PAD = 19
CHUNKSIZE = 1024
NEWLINE = u'\n'
SPACE = u' '

TEXT_PARSER_MIMETYPES = ['text/plain' ,'text/x-python', 'text/html', 'text/x-shellscript']

logger = logging.getLogger(__name__)


class TextParser(object):
    def render_to_viewport(self, filename, page_width=DEFAULT_PAGE_WIDTH, page_height=DEFAULT_PAGE_HEIGHT, fill_last_page=False):
        """
        Render an input text file into an imaginary squared view port (terminal window),
        returning a list of pages which are themselves a list of lines
        """
        pages = []
        with codecs.open(filename, 'rU', 'utf-8') as descriptor:
            width = 0
            height = 0
            line = []
            page = []
            bytes_read = descriptor.read(CHUNKSIZE)
            while bytes_read:
                for letter in bytes_read:
                    if letter != NEWLINE:
                        line.append(letter)
                        
                    width = width + 1
                    if width >= page_width or letter == NEWLINE:
                        page.append(u''.join(line))
                        line = []
                        width = 0
                        height = height + 1
                        if height >= page_height:
                            pages.append(page)
                            page = []
                            height = 0
                        
                bytes_read = descriptor.read(CHUNKSIZE)

            # Fill any final partial page with empty lines
            if fill_last_page:
                for filler in range(DEFAULT_PAGE_HEIGHT - len(page)):
                    page.append(SPACE)

            # Append any final partial page when chunk ends
            pages.append(page)
            

        return pages
        
    def render_to_image(self, filename, mimetype=None, actual_filename=None, page_width=DEFAULT_PAGE_WIDTH, page_height=DEFAULT_PAGE_HEIGHT, page_number=None, lexer=None, line_numbers=True, line_number_pad=DEFAULT_LINE_NUMBER_PAD):
        """
        Turn a list of pages and lines and product and image representation,
        selecting the best parser possible based on the filename and contents
        """
        pages = self.render_to_viewport(filename, page_width, page_height, fill_last_page=True)
        
        if not lexer:
            if mimetype:
                try:
                    lexer = get_lexer_for_mimetype(mimetype)
                except ClassNotFound:
                    pass
                else:
                    logger.debug('get_lexer_for_mimetype: %s' % lexer)
            else:
                # Read entire file to guess the lexer
                with codecs.open(filename, 'r', 'utf-8') as descriptor:                
                    logger.debug('guessing lexer for file: %s' % filename)

                    file_data = descriptor.read()
                    if not lexer:
                        try:
                            if actual_filename:
                                lexer = get_lexer_for_filename(actual_filename, file_data)
                            else:
                                lexer = get_lexer_for_filename(filename, file_data)
                        except ClassNotFound, err:
                            logger.debug('get_lexer_for_filename error: %s', err)
                            try:
                                lexer = guess_lexer(file_data)
                            except ClassNotFound:
                                lexer = TextLexer()
                                logger.debug('unable to guess lexer')
                            else:
                                logger.debug('guess_lexer returned: %s' % lexer)
                        else:
                            logger.debug('get_lexer_for_filename returned: %s' % lexer)
       
        logger.debug('lexer: %s' % lexer)

        if page_number:
            # Render a single page into image
            return highlight(u'\n'.join(pages[page_number - 1]), lexer, ImageFormatter(line_number_start=(page_number - 1) * page_height + 1, line_numbers=line_numbers, line_number_pad=line_number_pad))
        else:
            # Render all pages into image
            output = []
        
            for page, page_number in zip(pages, xrange(len(pages))):
                output.append(highlight(u'\n'.join(page), lexer, ImageFormatter(line_number_start=page_number * page_height + 1, line_numbers=line_numbers, line_number_pad=line_number_pad)))
                
            return output
