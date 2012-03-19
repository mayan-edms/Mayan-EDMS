from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from permissions.models import StoredPermission

from .literals import OPERAND_CHOICES, OPERAND_AND


class Ability(models.Model):
    label = models.CharField(max_length=128, unique=True, verbose_name = _(u'label'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    def __unicode__(self):
        return self.label
 
    class Meta:
        verbose_name = _(u'ability')
        verbose_name_plural = _(u'abilities')
    

class Workflow(models.Model):
    label = models.CharField(max_length=128, unique=True, verbose_name = _(u'label'))
    initial_state = models.ForeignKey('WorkflowState', related_name='workflow_initial_state', blank=True, null=True, verbose_name=_(u'initial state'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    
    def __unicode__(self):
        return self.label
 
    class Meta:
        verbose_name = _(u'workflow')
        verbose_name_plural = _(u'workflows')
        
        
class State(models.Model):
    label = models.CharField(max_length=128, verbose_name=_(u'label'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    def __unicode__(self):
        #return '%s (%s)' % (self.name, self.workflow.name)
        return self.label

    class Meta:
        verbose_name = _(u'state')
        verbose_name_plural = _(u'states')
        

class Transition(models.Model):
    label = models.CharField(max_length=128, verbose_name=_(u'label'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    def __unicode__(self):
        #return '%s (%s)' % (self.name, self.workflow.name)
        return self.label

    class Meta:
        verbose_name = _(u'transition')
        verbose_name_plural = _(u'transitions')
    
    
class WorkflowState(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=_(u'workflow'))
    state = models.ForeignKey(State, verbose_name=_(u'state'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
        
    def __unicode__(self):
        return unicode(self.state)

    @property
    def transitions(self):
        return self.workflowstatetransition_set

    class Meta:
        #unique_together = ('workflow', 'state')
        verbose_name = _(u'workflow state')
        verbose_name_plural = _(u'workflows states')


class WorkflowStateAbilityGrant(models.Model):
    workflow_state = models.ForeignKey(WorkflowState, related_name='workflow_state_ability', verbose_name=_(u'workflow state'))
    content_type = models.ForeignKey(ContentType, related_name='workflow_state_ability_object')#, blank=True, null=True)
    object_id = models.PositiveIntegerField()#blank=True, null=True)
    content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def __unicode__(self):
        return unicode(self.content_object)

    class Meta:
        verbose_name = _(u'workflow state ability grant')
        verbose_name_plural = _(u'workflows states ability grant')

#TODO: WorkflowStateACLEntry
#WorkflowState
#Actor
#Object
#Permission (s)


#TODO: WorkflowStateAlarm
#label
#timedate
#interval

        
class WorkflowStateTransition(models.Model):
    workflow_state_source = models.ForeignKey(WorkflowState, verbose_name=_(u'workflow state source'))
    transition = models.ForeignKey(Transition, related_name='workflow_state_transition', verbose_name=_(u'transition'))
    workflow_state_destination = models.ForeignKey(WorkflowState, related_name='workflow_state_transition_destination', verbose_name=_(u'workflow state destination'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
        
    def __unicode__(self):
        return unicode(self.transition)

    class Meta:
        verbose_name = _(u'workflow state transition')
        verbose_name_plural = _(u'workflows states transitions')        
        

class WorkflowStateTransitionAbility(models.Model):
    attribute_comparison_operand = models.CharField(max_length=8, default=OPERAND_AND, choices=OPERAND_CHOICES, verbose_name=_(u'operand'))
    negate = models.BooleanField(verbose_name=_(u'negate'), help_text=_(u'Inverts the attribute comparison.'))
    ability = models.ForeignKey(Ability, related_name='workflow_state_transition_ability', verbose_name=_(u'ability'))

    description = models.TextField(blank=True, verbose_name=_(u'description'))

    def __unicode__(self):
        return unicode(self.ability)

    class Meta:
        verbose_name = _(u'transition')
        verbose_name_plural = _(u'transitions')
      
        
class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name = _(u'workflow'))
    content_type = models.ForeignKey(ContentType, verbose_name=_(u'Content type'), related_name='workflow_instance_object')#, blank=True, null=True)
    object_id = models.PositiveIntegerField()#blank=True, null=True)
    content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')
    workflow_state = models.ForeignKey(WorkflowState, related_name='workflow_instance_state', verbose_name=_(u'state'))

    def __unicode__(self):
        return unicode(self.content_object)
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'workflow')
