

                            if staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                                expand = True
                            else:
                                expand = False                        
                        transformations, errors = SourceTransformation.transformations.get_for_object_as_list(staging_folder)
                        if (not expand) or (expand and not _handle_zip_file(request, staging_file.upload(), document_type=document_type, transformations=transformations)):
                            document = Document(file=staging_file.upload())
                            if document_type:
                                document.document_type = document_type
                            document.save()
                            document.apply_default_transformations(transformations)
                            _handle_save_document(request, document, form)
                            messages.success(request, _(u'Staging file: %s, uploaded successfully.') % staging_file.filename)

                        if staging_folder.delete_after_upload:
                            staging_file.delete(preview_size=staging_folder.get_preview_size(), transformations=transformations)
                            messages.success(request, _(u'Staging file: %s, deleted successfully.') % staging_file.filename)
                    except Exception, e:
                        messages.error(request, e)
