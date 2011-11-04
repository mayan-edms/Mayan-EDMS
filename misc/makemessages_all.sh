#!/bin/sh
MAKEMESSAGES="django-admin makemessages"
PWD=`pwd`
BASE=$PWD

cd $BASE/apps/common
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/converter
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/documents
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/document_comments
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/document_indexing
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/dynamic_search
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/folders
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/history
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/grouping
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/main
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/metadata
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/navigation
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/ocr
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/permissions
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/project_setup
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/project_tools
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/smart_settings
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/sources
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/tags
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/user_management
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/web_theme
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es
