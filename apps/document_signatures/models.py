from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentVersion, get_filename_from_uuid
from documents.conf.settings import STORAGE_BACKEND


class DocumentVersionSignature(models.Model):
    '''
    Model that describes a document version signature properties
    '''
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_(u'document version'), editable=False)
    signature_state = models.CharField(blank=True, null=True, max_length=16, verbose_name=_(u'signature state'), editable=False)
    signature_file = models.FileField(blank=True, null=True, upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'signature file'), editable=False)
        
    def update_signed_state(self, save=True):
        if self.exists():
            try:
                self.signature_state = gpg.verify_file(self.open()).status
                # TODO: give use choice for auto public key fetch?
                # OR maybe new config option
            except GPGVerificationError:
                self.signature_state = None
           
            if save:
                self.save()

    def add_detached_signature(self, detached_signature):
        if not self.signature_state:
            self.signature_file = detached_signature
            self.save()
        else:
            raise Exception('document already has an embedded signature')
    
    def has_detached_signature(self):
        if self.signature_file:
            return self.signature_file.storage.exists(self.signature_file.path)
        else:
            return False
    
    def detached_signature(self):
        return self.signature_file.storage.open(self.signature_file.path)
        
    def verify_signature(self):
        try:
            if self.has_detached_signature():
                logger.debug('has detached signature')
                signature = gpg.verify_w_retry(self.open(), self.detached_signature())
            else:
                signature = gpg.verify_w_retry(self.open(raw=True))
        except GPGVerificationError:
            signature = None
            
        return signature
        
    class Meta:
        verbose_name = _(u'document version signature')
        verbose_name_plural = _(u'document version signatures')        
