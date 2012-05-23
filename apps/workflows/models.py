from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from permissions.models import StoredPermission

from .literals import OPERAND_CHOICES, OPERAND_AND
#from .literals import NODE_TYPE_TASK, NODE_TYPE_START, NODE_TYPE_END

#NODE_TYPE_CHOICES

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
    initial_node = models.ForeignKey('WorkflowNode', related_name='workflow_initial_node', blank=True, null=True, verbose_name=_(u'initial node'))
    initial_state = models.ForeignKey('WorkflowState', related_name='workflow_initial_state', blank=True, null=True, verbose_name=_(u'initial state'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    
    def __unicode__(self):
        return self.label
 
    @property
    def workflow_nodes(self):
        return self.workflownode_set
 
    def get_nodes(self):
        return [workflow_node.node for workflow_node in self.workflownode_set.all()]
        
    def add_node(self, node):
        workflow_node = WorkflowNode(
            workflow=self,
            node=node)
        workflow_node.save()
        return workflow_node
 
    def save(self, *args, **kwargs):
        is_new = not self.pk
        result = super(Workflow, self).save(*args, **kwargs)

        if is_new:
            # Instanciate a new start node
            start_node = Start()
            start_node.save()
            
            # Set the start node a
            workflow_node = self.add_node(node=start_node)
            
            self.initial_node = workflow_node
            self.save()
            
        return result
 
    class Meta:
        verbose_name = _(u'workflow')
        verbose_name_plural = _(u'workflows')


class Node(models.Model):
    """
    Must provide:
        possible_next_nodes()
            Arguments: None
            Returns:
                List of possible nodes after this one executes
            
        choices()
            Arguments: workflow
            Returns:
                {
                    'next_node': workflow.nodes.all()
                }

        execute()
            Arguments: workflow_instance
            Returns: next_node    
    """
    
    label = models.CharField(max_length=128, verbose_name=_(u'label'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _(u'state')
        verbose_name_plural = _(u'states')
        abstract = True


class Start(Node):
    """
    The node with which all workflows start
    """
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    next_node = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')
    
    def __unicode__(self):
        return ugettext(u'Start')
        
    def possible_next_nodes(self):
        return self.next_node
            
    def choices(self, workflow):
        return {
            'next_node': workflow.nodes.all()
        }

    def execute(self, workflow_instance):
        return self.next_node

    class Meta(Node.Meta):
        verbose_name = _(u'start node')
        verbose_name_plural = _(u'start nodes')
        

class End(Node):
    class Meta(Node.Meta):
        verbose_name = _(u'end node')
        verbose_name_plural = _(u'end nodes')
    

'''
class Sequence(Node):
    """
    A node that is enabled after the completion of a preceding node in the same workflow
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    next_node = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')
    #node_type = NODE_TYPE_TASK

    def execute(self):
        return self.next_node
    
    class Meta(Node.Meta):
        verbose_name = _(u'task')
        verbose_name_plural = _(u'tasks')
'''

class State(models.Model):
    label = models.CharField(max_length=128, verbose_name=_(u'label'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _(u'state')
        verbose_name_plural = _(u'states')
        ordering = ('label',)
        

class WorkflowState(models.Model):
    """
    List of possible states the object of this worflow could be in
    """
    workflow = models.ForeignKey(Workflow, verbose_name=_(u'workflow'))
    state = models.ForeignKey(State, verbose_name=_(u'state'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
        
    def __unicode__(self):
        return unicode(self.state)

    class Meta:
        unique_together = ('workflow', 'state')
        verbose_name = _(u'workflow state')
        verbose_name_plural = _(u'workflows states')

# TODO: Reduntant - remove
class WorkflowNode(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=_(u'workflow'))
    content_type = models.ForeignKey(ContentType)#, limit_choices_to={'model__in': ('model1', 'model2')})#, related_name='workflow_state_ability_object')#, blank=True, null=True)
    object_id = models.PositiveIntegerField()#blank=True, null=True)
    node = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')
    description = models.TextField(blank=True, verbose_name=_(u'description'))
        
    def __unicode__(self):
        return unicode(self.node)

    #def save(self, *args, **kwargs):
    #    if not issubclass(
    #    return super(WorkflowNode, self).save(*args, **kwargs)
        
    class Meta:
        #unique_together = ('workflow', 'state')
        verbose_name = _(u'workflow node')
        verbose_name_plural = _(u'workflows nodes')

"""
class WorkflowTaskAbilityGrant(models.Model):
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
      
"""        
class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=_(u'workflow'))
    content_type = models.ForeignKey(ContentType, verbose_name=_(u'Content type'), related_name='workflow_instance_object')#, blank=True, null=True)
    object_id = models.PositiveIntegerField()#blank=True, null=True)
    content_object = generic.GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def __unicode__(self):
        return unicode(self.content_object)
     
    @property
    def active_nodes(self):
        return self.workflowinstanceactivenode_set
        
    def set_active_state(self, state):
        active_state = self.get_active_state()
        if active_state:
            active_state.delete()
            
        # Trigger an exception if the state argument if not allowed for this workflow
        state = WorkflowState.objects.get(workflow=self.workflow, state=state).state

        self.workflowinstanceactivestate_set.create(
            workflow_instance = self,
            state = state
        )

    def get_active_state(self):
        try:
            return self.workflowinstanceactivestate_set.get().state
        except WorkflowInstanceActiveState.DoesNotExist:
            return None
            
    active_state = property(get_active_state, set_active_state)
    
    class Meta:
        verbose_name = _(u'workflow instance')
        verbose_name_plural = _(u'workflow instances')
        
    #    unique_together = ('content_type', 'object_id', 'workflow')


class WorkflowInstanceActiveNode(models.Model):
    workflow_instance = models.ForeignKey(WorkflowInstance, verbose_name=_(u'workflow instance'))
    workflow_node = models.ForeignKey(WorkflowNode, verbose_name=_(u'workflow node'))    

    class Meta:
        verbose_name = _(u'workflow instance active node')
        verbose_name_plural = _(u'workflow instances active nodes')


class WorkflowInstanceState(models.Model):
    """
    This class holds the active state for the workflow instance
    """
    workflow_instance = models.ForeignKey(WorkflowInstance, verbose_name=_(u'workflow instance'))
    state = models.ForeignKey(State, null=True, verbose_name=_(u'state'))    

    class Meta:
        unique_together = ('workflow_instance', 'state')
        verbose_name = _(u'workflow instance active state')
        verbose_name_plural = _(u'workflow instances active states')


# TODO: WorkflowInstanceActiveNodeHistory
# TODO: WorkflowInstanceActiveStateHistory
