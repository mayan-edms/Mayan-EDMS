*****************
Mailing documents
*****************

Sending emails in Mayan EDMS is controlled by two different system depending on
the type of email being sent. These are administrative emails like password
reset emails and user emails sent from the application. To configure
administrative email for things like password reset check the topic:
:doc:`../topics/administration`

Application emails
==================

To allow users to send emails or documents from within the web interface,
Mayan EDMS provides its our own email system called Mailing Profiles.
Mailing Profiles support access control per user role and can use different
email backends. Mailing Profiles are created from the
:menuselection:`System --> Setup` menu.

Once created mailing profiles allow users to send email messages from
within the user interface containing either an URL link to the document or
the actual document as an attachment.
