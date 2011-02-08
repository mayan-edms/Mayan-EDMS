import os
import tempfile

from documents.conf.settings import TEMPORARY_DIRECTORY

#http://snippets.dzone.com/posts/show/5434
#http://snippets.dzone.com/user/jakob
def pretty_size(size):
	suffixes = [("B",2**10), ("K",2**20), ("M",2**30), ("G",2**40), ("T",2**50)]
	for suf, lim in suffixes:
		if size > lim:
			continue
		else:
			return round(size/float(lim/2**10),2).__str__()+suf
            
            
#http://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
def copyfile(source, dest, buffer_size=1024*1024):
    """
    Copy a file from source to dest. source and dest
    can either be strings or any object with a read or
    write method, like StringIO for example.
    """
    if not hasattr(source, 'read'):
        source = open(source, 'rb')
    if not hasattr(dest, 'write'):
        dest = open(dest, 'wb')

    while 1:
        copy_buffer = source.read(buffer_size)
        if copy_buffer:
            dest.write(copy_buffer)
        else:
            break

    source.close()
    dest.close()


def from_descriptor_to_tempfile(input_descriptor, filename, buffer_size=1024*1024):
    path = os.path.join(TEMPORARY_DIRECTORY, filename)
    
    output_descriptor = open(path, 'wb')
    
    while 1:
        copy_buffer = input_descriptor.read(buffer_size)
        if copy_buffer:
            output_descriptor.write(copy_buffer)
        else:
            break

    input_descriptor.close()
    output_descriptor.close()
    return path



def from_descriptor_to_new_tempfile(input_descriptor, buffer_size=1024*1024):
    output_descriptor, tmp_filename = tempfile.mkstemp()
    
    while 1:
        copy_buffer = input_descriptor.read(buffer_size)
        if copy_buffer:
            #output_descriptor.write(copy_buffer)
            os.write(output_descriptor, copy_buffer)
        else:
            break

    input_descriptor.close()
    os.close(output_descriptor)
    return tmp_filename
