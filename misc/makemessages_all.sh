#!/bin/sh
MAKEMESSAGES="django-admin makemessages"
PWD=`pwd`
BASE=$PWD

cd $BASE/apps/common
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/converter
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/documents
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/document_comments
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/document_indexing
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/dynamic_search
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/folders
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/history
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/linking
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/main
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/metadata
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/navigation
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/ocr
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/permissions
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/project_setup
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/project_tools
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/smart_settings
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/sources
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/tags
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/user_management
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es

cd $BASE/apps/web_theme
$MAKEMESSAGES -l en
$MAKEMESSAGES -l pt
$MAKEMESSAGES -l ru
$MAKEMESSAGES -l es
