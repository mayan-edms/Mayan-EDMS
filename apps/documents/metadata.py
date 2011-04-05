from urllib import unquote_plus

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


from models import DocumentMetadata, MetadataType

def decode_metadata_from_url(url_dict):
    metadata_dict = {
        'id':{},
        'value':{}
    }
    metadata_list = []
    #Match out of order metadata_type ids with metadata values from request
    for key, value in url_dict.items():
        if 'metadata' in key:
            index, element = key[8:].split('_')
            metadata_dict[element][index] = value
        
    #Convert the nested dictionary into a list of id+values dictionaries
    for order, id in metadata_dict['id'].items():
        if order in metadata_dict['value'].keys():
            metadata_list.append({'id':id, 'value':metadata_dict['value'][order]})

    return metadata_list
    
    
def save_metadata_list(metadata_list, document):
    for item in metadata_list:
        if item['value']:
            save_metadata(item, document)
        else:
            #If there is no metadata value, delete the metadata entry 
            #completely from the document
            try:
                metadata_type = MetadataType.objects.get(id=item['id'])
                document_metadata = DocumentMetadata.objects.get(document=document,
                    metadata_type=metadata_type)
                document_metadata.delete()
            except ObjectDoesNotExist:
                pass
                        
        
def save_metadata(metadata_dict, document):
    #Use matched metadata now to create document metadata
    document_metadata, created = DocumentMetadata.objects.get_or_create(
        document=document,
        metadata_type=get_object_or_404(MetadataType, pk=metadata_dict['id']),
    )
    #Handle 'plus sign as space' in the url
    
    #unquote_plus handles utf-8?!?
    #http://stackoverflow.com/questions/4382875/handling-iri-in-django
    document_metadata.value = unquote_plus(metadata_dict['value'])#.decode('utf-8')
    document_metadata.save()


def metadata_repr(metadata_list):
    return ', '.join(metadata_repr_as_list(metadata_list))
   
    
def metadata_repr_as_list(metadata_list):
    output = []
    for metadata_dict in metadata_list:
        try:
            output.append('%s - %s' % (MetadataType.objects.get(pk=metadata_dict['id']), metadata_dict.get('value', '')))
        except:
            pass
        
    return output
    
    
    
