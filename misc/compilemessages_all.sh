#!/bin/sh
COMPILEMESSAGES="django-admin compilemessages"
PWD=`pwd`
BASE=$PWD

cd $BASE/apps/common
$COMPILEMESSAGES -l pt

cd $BASE/apps/converter
$COMPILEMESSAGES -l pt

cd $BASE/apps/documents
$COMPILEMESSAGES -l pt

cd $BASE/apps/document_comments
$COMPILEMESSAGES -l pt

cd $BASE/apps/document_indexing
$COMPILEMESSAGES -l pt

cd $BASE/apps/dynamic_search
$COMPILEMESSAGES -l pt

cd $BASE/apps/folders
$COMPILEMESSAGES -l pt

cd $BASE/apps/history
$COMPILEMESSAGES -l pt

cd $BASE/apps/grouping
$COMPILEMESSAGES -l pt

cd $BASE/apps/main
$COMPILEMESSAGES -l pt

cd $BASE/apps/metadata
$COMPILEMESSAGES -l pt

cd $BASE/apps/navigation
$COMPILEMESSAGES -l pt

cd $BASE/apps/ocr
$COMPILEMESSAGES -l pt

cd $BASE/apps/permissions
$COMPILEMESSAGES -l pt

cd $BASE/apps/project_setup
$COMPILEMESSAGES -l pt

cd $BASE/apps/project_tools
$COMPILEMESSAGES -l pt

cd $BASE/apps/smart_settings
$COMPILEMESSAGES -l pt

cd $BASE/apps/sources
$COMPILEMESSAGES -l pt

cd $BASE/apps/tags
$COMPILEMESSAGES -l pt

cd $BASE/apps/user_management
$COMPILEMESSAGES -l pt

cd $BASE/apps/web_theme
$COMPILEMESSAGES -l pt
