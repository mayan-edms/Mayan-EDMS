===========
Smart links
===========


To configure: |Setup tab| |Right arrow| |Smart links button|

To use: |Document icon| |Right arrow| |Smart links link|

Smart links are usefull for navigation between documents.  They are rule
based but don't create any organizational structure, just show the documents
that match the rules as evaluated against the metadata of the currently
displayed document.  

.. figure:: /_static/screenshots/smart_links_screenshot.png
   :alt: Smart links screenshot
   :scale: 75%

   Screenshot of smart links in action.  The documents being shown are from the same
   permit file number as the current document being viewed by the user.
   Notice how the current document is also highlighted with a black border.
   
**Details**

To create a Smart Link, a user with adequate permissions first clicks on the 
"Settings" tab in the top menu, then click on the "Smart Links" button. The screen
for creating a new (or editing an existing) Smart Link requires you to name the 
Link and to ensure it is enabled if you wish to user it. Optionally, "Dynamic title"
may be created. The Dynamic title is entended to contain references to attributes 
of a document or it's metadata. Let's cover some simpler cases and come back to 
dynamic references below. 

*Static Links* 

Smart links don't actually have to be overly smart. As a gentle introduction, lets
create a simple "static" link which will show all the documents added in the year
2014. We'll use the title "Added in 2014", leave the dynamic title empty, and ensure
that "Enabled" is checked. 

To have the link actually do something, we have to add one or more "condition". 
Conditions are translated by the system into clauses in a query (search) of the 
document database. There is a "Create condition" link in the right-bar of the Smart
Link screen. For our simple case, the value of the "Inclusion" drop down does not 
matter; we can leave it at the default "AND". For "Foreign document data" we will 
enter:

  document.date_added

For "Operator" we will select "contains". 

For "Expression" we will enter:

  2014

Underneath this field, "negated" should be unchecked and "enabled" should be checked. 
Save the condition then go to the documents tab. Click on the filename of any file 
listed there. Click on the "Smart link" tab under the submenu. A list of all 
documents entered in 2014 (if any) should be shown. 

There are a number of other document attributes which can be used in searches, with
some important caveats: 

* date_added: (discussed above)

* comments: this is next to useless at present, since instead of searching through 
  text of all comments you can instead search for the "id" of comments. 

* description: enclose the text you want to search for in 'single' or "double" quotes.

* document_type: can be used if Document Types have been defined and assigned to docs
  as they have been uploaded. The search is performed against the "id" of the document_type 
  and not against the textual description of the Document Type. This limitation,
  however, is hidden if used in a dynamic link as demonstrated below. 
  
* documentcheckout: a meaningful query clause can be consructed by choosing this 
  documnet attribute and testing if it "is equal to" 1 (for "true" or "is checked out")
  or 0 (for "false" or "is not checked out")
  
* documentrenamecount: this attribute is reported by the system as available for 
  searching but it's utility is not clear
  
* folderdocument: This attribute searches agains the "id" of the folder to which 
  a document may have been added, not against the textual name of a folder and thus 
  is useful primarily in dynamicly defined links (see below). 
  
* id: each document has a unique numeric id which can be used in searches

* indexinstancenode: ??

* metadata: ?? (see below) 

* queuedocument: ??

* recentdocument: this attibute appears to hold an integer (simple number like 1,2,3)
  indicating the relative order in which documents were added to the system. This 
  may be of some use for finding documents which were added before or after a given
  document. 
  
* tagged_items: using this attribute by entering in an integer value appears to 
  perform a search equivalent to "if document has at least one tag and this id number"
  
* tags: the "id" value of the corresponding tags are used. A tag will be matched if it
  is alone or among several tags assigned to a document. 
  
* uuid: of little value, since these are by definition unique.

* versions: ??


You can also define Smart Links based on Metadata types and values which you have 
defined. For this to work, it appears to be necessary to give the metadata type "Name" 
(also known as "Internal name") which is all lowercase. The "Title" can be uppercase.

For instance, if a metadata type is defined with these values:
  Name: priority
  Title: Priority
  Default: 5
  Lookup: (1,2,3,4,5,6,7,8,9,10)
Then I can assign various documents different priorities and create a "Smart Link" 
to find the high priority links by defining the condition as 
  Inclusion: and 
  Foreign document data: is greater or equal to
  Expression: 5

*Dynamic Smart Links*

Links which are truly Smart are created by referencing the current value of the 
document you are viewing and not a static value in at least one of the conditions.

For instance, the last example above can be modified so that the Smart Link is:
  Inclusion: and 
  Foreign document data: is greater or equal to
  Expression: metadata.priority
  
By including "metadata.priority" as the Expression instead of a static value, we 
now have a Smart Link which will find all other documents with a Priority metadata
value greater than or equal to the one we are viewing. 

Here's an example by Mathias from the forums 
(<https://groups.google.com/forum/#!topic/mayan-edms/nO5DFB1udhc>) which 
demonstrates how to find other documents in the same project, if "project" has 
been defined as a Metadata type. This example shows how to use the Dynamic Title 
feature also.

Title: Same project 
Dynamic title: u'All documents of: %s' % getattr(metadata, 'project', 'None') 

Condition: 
Inclusion: and 
Foreign document data: metadata.project 
Operator: equal 
Expression: metadata.project 

The document attributes listed above which use the "id" value to do matching are
more useful for dynamic than static conditions. For instance we can set both the
foreign and current document Expressiong to "document.document_type" to get a 
Smart Link to all other documents of the same Document Type as the current one. 

*Combining Conditions*

In theory we should be able to add multiple conditions and choose "and" or "or" 
to define how they interact with the previous condition. There does not appear 
to be a mechanism for defining parenthises to group conditions, but such subtleties
are far beyond the current state of this funcitonality as even the simplest cases
appear not to work. Defining to conditions, each of which yeild a set with 
documents in common, and then combining them with "and" yeilds no documents at all.
Switching to "or" returns the same documents multiple times. 

*Tricky Smart Links*

Advanced users can explore ways to use regular expressions in Smart Links. For 
example, one might want easy access to documentation for software features not
yet in production by using:

Foreign document data: document.description
Operator: is in regular expression (case insensitive)
Expression: r'test|experimental|development'



.. |Setup tab| image:: /_static/setup_tab.png
 :alt: Setup tab
 :align: middle

.. |Right arrow| image:: /_static/arrow_right.png
 :alt: Right arrow
 :align: middle

.. |Smart links button| image:: /_static/smart_links_button.png
 :alt: Smart links button
 :align: middle

.. |Document icon| image:: /_static/page.png
 :alt: Document icon
 :align: middle

.. |Smart links link| image:: /_static/smart_links_link.png
 :alt: Smart links link
 :align: middle

