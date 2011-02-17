#Some code from http://wiki.github.com/hoffstaetter/python-tesseract

import os
from multiprocessing import Process, Queue
from Queue import Empty

import subprocess
import tempfile

from django.utils.translation import ugettext as _
from django.contrib import messages

from common.conf.settings import TEMPORARY_DIRECTORY

from documents.models import Document

from converter.api import convert_document_for_ocr

from ocr.conf.settings import TESSERACT_PATH

from literals import QUEUEDOCUMENT_STATE_PROCESSING, \
    QUEUEDOCUMENT_STATE_ERROR, QUEUEDOCUMENT_STATE_PENDING

from models import DocumentQueue

queue_dict = {}

def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass

class TesseractError(Exception):
    pass
#    def __init__(self, status, message):
#        self.status = status
#        self.message = message

def get_errors(error_string):
    '''
    returns all lines in the error_string that start with the string "error"

    '''
    lines = error_string.splitlines()
    return lines[1]
    #error_lines = (line for line in lines if line.find('error') >= 0)
    #return '\n'.join(error_lines)

def run_tesseract(input_filename, output_filename_base, lang=None):
    command = [TESSERACT_PATH, input_filename, output_filename_base]
    if lang is not None:
        command += ['-l', lang]

    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())


#def do_document_ocr(document):

def do_document_ocr(document):
    for page_index, document_page in enumerate(document.documentpage_set.all()):    
        imagefile = convert_document_for_ocr(document, page=page_index)
        desc, filepath = tempfile.mkstemp()
        try:
            status, error_string = run_tesseract(imagefile, filepath)
            if status:
                errors = get_errors(error_string)
                raise TesseractError(errors)
        finally:
            ocr_output = os.extsep.join([filepath, 'txt'])

        f = file(ocr_output)
        try:
            #document_page, created = DocumentPage.objects.get_or_create(document=document,
            #    page_number=page_index+1)
            document_page = document.documentpage_set.get(page_number=page_index+1)
            document_page.content = f.read().strip()
            document_page.page_label = _(u'Text from OCR')
            document_page.save()
        finally:
            f.close()
            cleanup(filepath)
            cleanup(ocr_output)
            cleanup(imagefile)


def do_queue_document(queue_document):
    print 'do_queue_document'
    queue_document.state = QUEUEDOCUMENT_STATE_PROCESSING
    queue_document.save()

    try:
        do_document_ocr(queue_document.document)
        queue_document.delete()
        print 'ocr ended ok'

    except Exception, e:
        print 'error', e
        queue_document.state = QUEUEDOCUMENT_STATE_ERROR
        queue_document.result = e
        queue_document.save()
        


def process_queue_document(queue_document):
    #print 'process_queued_document'
    #print 'test' ,queue_document.document.documentpage_set.all()    
    #print 'after'
    d=Document.objects.get(id=42)
    print d
    print d.documentpage_set.all()
    print 'after'
    
    p = Process(target=do_queue_document, args=(queue_document,))
    p.start()
    

def start_queue_watcher(queue_name):

    if queue_name in queue_dict:
        print 'already started'
    else:
        queue_dict[queue_name] = Queue()
        print 'start', queue_name
    #    if queue_name in queue_dict:
        document_queue = DocumentQueue.objects.get(name=queue_name)
        watcher = Process(target=queue_watcher, args=(document_queue,))
        watcher.start()
    #    else:
    #        raise Exception('No such queue: %s' % queue_name)

import time
import sys
def queue_watcher(document_queue):
    while True:
        time.sleep(5)
        try:
            oldest_queued_document = document_queue.queuedocument_set.filter(
                state=QUEUEDOCUMENT_STATE_PENDING).order_by('datetime_submitted')[0]
            process_queue_document(oldest_queued_document)
            print 'queue.get', oldest_queued_document
            sys.stdout.flush()
        except:
            pass
