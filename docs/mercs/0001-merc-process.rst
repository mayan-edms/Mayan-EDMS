==============================
MERC 1: Purpose and Guidelines
==============================

:MERC: 1
:Author: Michael Price
:Status: Accepted
:Type: Process
:Created: 2018-02-17
:Last-Modified: 2018-02-17

.. contents:: Table of Contents
   :depth: 3
   :local:

What is a MERC?
===============

A Mayan EDMS Request For Comment document or MERC document is a design
document providing information to the Mayan EDMS community, or
describing a new feature or process for Mayan EDMS. MERCs provide
concise technical specifications of features, along with rationales.

MERC Types
==========

There are three kinds of MERCs:

1. A **Feature** MERC describes a new feature or implementation
for Mayan EDMS. Most MERCs will be Feature MERCs.

2. An **Informational** MERC describes a Mayan EDMS design issue, or
provides general guidelines or information to the Mayan EDMS community,
but does not propose a new feature. Informational MERCs do not
necessarily represent a community consensus or
recommendation, so users and implementers are free to ignore
Informational MERCs or follow their advice.

3. A **Process** MERC describes a process surrounding Mayan EDMS, or
proposes a change to (or an event in) a process.  Process MERCs are
like Feature MERCs but apply to areas other than the Mayan EDMS
framework itself.  They may propose an implementation, but not to
Mayan EDMS's codebase; they often require community consensus; unlike
Informational MERCs, they are more than recommendations, and users
are typically not free to ignore them.  Examples include
procedures, guidelines, changes to the decision-making process, and
changes to the tools or environment used in Mayan EDMS development.
Any meta-MERC is also considered a Process MERC. (So this document
is a Process MERC).

MERC submission workflow
========================

Pre-proposal
------------

The MERC process begins with a new idea for Mayan EDMS. It is highly recommended
that a single MERC contain a single key proposal or new idea. Small enhancements
or patches usually don't need a MERC and follow Mayan EDMS's normal contribution
process.

MERCs should be focused on a single topic. If in doubt, split your MERC
into several well-focused ones.

Once the idea's been vetted, a draft MERC should be presented to the
Mayan EDMS mailing list. This gives the author a chance to flesh out the
draft MERC to make sure it's properly formatted, of high quality, and to address
initial concerns about the proposal.

The Core Developers will be responsible for accepting or rejecting the MERC proposal.


Submitting the draft
--------------------

Following the discussion on Mayan EDMS mailing list, the proposal
should be sent as a merge request to the Mayan EDMS repository. The draft must
be written in MERC style; if it isn't the merge request may be rejected until proper
formatting rules are followed.


Implementation
--------------

Finally, once a MERC has been accepted, the implementation must be completed. In
many cases some (or all) implementation will actually happen during the MERC
process: Feature MERCs will often have fairly complete implementations before
being reviewed. When the implementation is complete and incorporated
into the main source code repository, the status will be changed to
"Final".

MERC format
===========

MERCs need to follow a common format and outline; this section describes
that format.

MERCs must be written in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_
(the same format as Mayan EDMS's documentation).

Each MERC should have the following parts:

#. A short descriptive title (e.g. "User document filters"), which is also reflected
   in the MERC's filename (e.g. ``0002-user-document-filters.rst``).

#. A preamble -- a rST `field list <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists>`_
   containing metadata about the MERC, including the MERC number and so forth. See
   `MERC Metadata`_ below for specific details.

#. Abstract -- a short (~200 word) description of the technical issue
   being addressed.

#. Specification -- The technical specification should describe the syntax and
   semantics of any new feature.  The specification should be detailed enough to
   allow implementation -- that is, developers other than the author should
   (given the right experience) be able to independently implement the feature,
   given only the MERC.

#. Motivation -- The motivation is critical for MERCs that want to add
   substantial new features or materially refactor existing ones. It should
   clearly explain why the existing solutions are inadequate to address the
   problem that the MERC solves. MERC submissions without sufficient motivation
   may be rejected outright.

#. Rationale -- The rationale fleshes out the specification by describing what
   motivated the design and why particular design decisions were made. It
   should describe alternate designs that were considered and related work.

   The rationale should provide evidence of consensus within the community and
   discuss important objections or concerns raised during discussion.

#. Backwards Compatibility -- All MERCs that introduce backwards
   incompatibilities must include a section describing these incompatibilities
   and their severity.  The MERC must explain how the author proposes to deal
   with these incompatibilities. MERC submissions without a sufficient backwards
   compatibility treatise may be rejected outright.

#. Reference Implementation -- The reference implementation must be completed
   before any MERC is given status "Final", but it need not be completed before
   the MERC is accepted. While there is merit to the approach of reaching
   consensus on the specification and rationale before writing code, the
   principle of "rough consensus and running code" is still useful when it comes
   to resolving many discussions of API details.

   The final implementation must include tests and documentation, per Mayan EDMS
   development guide.


MERC Metadata
-------------

Each MERC must begin with some metadata given as an rST
`field list <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists>`_.
The headers must contain the following fields:

``MERC``
    The MERC number. In an initial merge request, this can be left out or given
    as ``XXXX``; the reviewer who merges the pull request will assign the MERC
    number.
``Type``
    ``Feature``, ``Informational``, or ``Process``
``Status``
    ``Draft``, ``Accepted``, ``Rejected``, ``Withdrawn``, ``Final``, or ``Superseded``
``Created``
    Original creation date of the MERC (in ``yyyy-mm-dd`` format)
``Last-Modified``
    Date the MERC was last modified (in ``yyyy-mm-dd`` format)
``Author``
    The MERC's author(s).
``Implementation-Team``
    The person/people who have committed to implementing this MERC
``Requires``
    If this MERC depends on another MERC being implemented first,
    this should be a link to the required MERC.
``Mayan EDMS-Version`` (optional)
    For Feature MERCs, the version of Mayan EDMS (e.g. ``2.7.3``) that this
    feature will be released in.
``Replaces`` and ``Superseded-By`` (optional)
    These fields indicate that a MERC has been rendered obsolete. The newer MERC
    must have a ``Replaces`` header containing the number of the MERC that it
    rendered obsolete; the older MERC has a ``Superseded-By`` header pointing to
    the newer MERC.
``Resolution`` (optional)
    For MERCs that have been decided upon, this can be a link to the final
    rationale for acceptance/rejection. It's also reasonable to simply update
    the MERC with a "Resolution" section, in which case this header can be left
    out.

Auxiliary Files
---------------

MERCs may include auxiliary files such as diagrams.  Such files must be named
``XXXX-descriptive-title.ext``, where "XXXX" is the MERC number,
"descriptive-title" is a short slug indicating what the file contains, and
"ext" is replaced by the actual file extension (e.g. "png").

Reporting MERC Bugs, or Submitting MERC Updates
===============================================

How you report a bug, or submit a MERC update depends on several factors, such as
the maturity of the MERC, the preferences of the MERC author, and the nature of
your comments. For the early draft stages of the MERC, it's probably best to
send your comments and changes directly to the MERC author. For more mature, or
finished MERCs you can submit corrections as repository issues or merge requests
against the git repository.

When in doubt about where to send your changes, please check first with the MERC
author and/or a core developer.

MERC authors with git push privileges for the MERC repository can update the MERCs
themselves.
