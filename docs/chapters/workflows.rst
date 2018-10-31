*********
Workflows
*********

Introduction
============

Workflows provide a structure method for storing a sequence of states over
which the a document will progress. Workflows keep track how a document has
been processed so far.

Workflows work by storing a series of states to help you know the "status"
of a document. To move a workflow from one state to another, transitions are
used.

Transitions connect two different states and help provide context to know
which state is possible to transition to, from a previous state. Transitions
provide and order for the sequence of possible states changes.

Transitions can be executed manually by users if they have the required access
level as configure by the system administrator.


Automation
==========

Besides being able to be executed manually by users, transitions can also be
programmed execute automatically based on system events. This is called in
Mayan EDMS transition triggering and is one of the tools available to
automate business processes.

For example:

* Move a document from a "scanned" state to a "billed" state
  when a tag is attached to the document.
* Move a document from a "uploaded" state to a "OCR ready" state
  when the OCR engine finishes processing the document.

The other tool provided for process automation is being able to execute an
action when a workflow state is reached or leaved. These are called state
events.

Some examples of state actions currently provided are:

* Attach a tag to a document
* Remove a tag from a document
* Do an HTTP POST request to an external IP address
* Edit the label or the description of a document.

Other time more state actions are being added. Some state actions like the one
that creates an HTTP POST request allow Mayan EDMS to trigger processes in
external systems based on the state of a document. One example of this is
triggering the billing process of an accounting system when an invoice is
scanned in Mayan EDMS.

Workflow state actions and transitions triggers are new features and are still
evolving.

Workflows allow translating business logic into a series of states. With the
addition of state actions and transition triggers, the workflows in Mayan EDMS
are no longer just informative but can be part of your actual business
automation process.


Implementation
==============

Internally, workflows are implemented as a finite state machines
(https://en.wikipedia.org/wiki/Finite-state_machine). And have the limitation
that only one state can be the current active state for a workflow being
executed. The other limitation of the current implementation is that every
workflow needs at least one state marked as the initial state. These limitations
are the result of a compromised in the design between flexibility and ease of
use.


Visualizations
==============

The graphical representation of a workflow (or a finite state machine style
in Mayan EDMS's case) is similar to a flowchart. The states are represented
with circles. The transitions are represented with arrows. Circle with a
double border represent the initial state of the workflow.

To view the graphical representations of workflow use **Preview** button of
the workflow in the setup view.



We are working now on workflow transition trigger filters to have
the trigger move the state of the workflow on certain conditions. For example: Attach a tag if there is a specific word found in the OCR text.
