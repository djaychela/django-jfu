--------------------------------------------------------------------
Django-JFU - A Django Library for jQuery File Upload for Django 3.0+
--------------------------------------------------------------------

Django-JFU is designed to simplify the tasks involved in integrating jQuery
File Upload (https://github.com/blueimp/jquery-file-upload) into Django.
Django-JFU assumes very little and leaves the model/view design up to the user. 

Other Django - jQuery File Upload implementations are full-featured but
generally serve more as demonstrations than libraries for existing
applications.

If you seek a tool to ease the integration of jQuery File Upload into your
Django application while still having a great degree of freedom, you may find
this package useful.

This version is updated to work with Django 3.0, as it seems that the library has been abandoned.
This involved changes to the jfu template tag (which used functions removed before even Django 2 existed,
as well as updating the demo project so that it would work out-of-the-box with v3, while removing extraneous code.
``photo_upload_form.html`` is included in the demo project, rather than in the jfu folder.

To allow rendering of the contents of the .html and .py files in the demo project (to allow the user to see the relevant code), the ``custom_tags.py`` file includes two template tags - ``verbatim_include`` and ``verbatim_include_py`` which allow the file contents to be rendered within the template (this re-creates roughly the functionality of the pre-django 1.10 ``ssi`` template tag).


Installation
------------

1. clone the repo.
2. build the repo with ``setup.py build`` then ``setup.py install``
3. Add 'jfu' to ``INSTALLED_APPS`` in your project settings.py file.
4. Run `python manage.py collectstatic`.


Usage
-----

Django-JFU provides simple customizable template tags and override-able
templates that do the work of integrating the jQuery File Upload CSS and
JavaScipt and the HTML implementation found in the jQuery File Upload demo.

To place the jQuery File Upload widget in a template, simply insert the
following within it::
    
    {% load jfutags %}
    {% jfu %}

Then create a view that will handle the uploaded files. 
The URL for the view is expected to be named **'jfu_upload'** by default,
although this can be customized (see Customization below).

Here is an example implementation:

In your ``urls.py`` file::

    ...
    path( 'upload/', views.upload, name = 'jfu_upload' ),

    # You may optionally define a delete url as well
    path( 'delete/<int:pk>', views.upload_delete, name = 'jfu_delete' ),

In your ``views.py`` file::
    
    import os
    from django.conf import settings
    from django.core.urlresolvers import reverse
    from django.views import generic
    from django.views.decorators.http import require_POST
    from jfu.http import upload_receive, UploadResponse, JFUResponse

    from YOURAPP.models import YOURMODEL

    @require_POST
    def upload( request ):

        # The assumption here is that jQuery File Upload
        # has been configured to send files one at a time.
        # If multiple files can be uploaded simulatenously,
        # 'file' may be a list of files.
        file = upload_receive( request )

        instance = YOURMODEL( file = file )
        instance.save()

        basename = os.path.basename( instance.file.path )
        
        file_dict = {
            'name' : basename,
            'size' : file.size,

            'url': settings.MEDIA_URL + basename,
            'thumbnailUrl': settings.MEDIA_URL + basename,

            'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
            'deleteType': 'POST',
        }

        return UploadResponse( request, file_dict )

    @require_POST
    def upload_delete( request, pk ):
        success = True
        try:
            instance = YOURMODEL.objects.get( pk = pk )
            os.unlink( instance.file.path )
            instance.delete()
        except YOURMODEL.DoesNotExist:
            success = False

        return JFUResponse( request, success )

Customization
-------------

Django-JFU is designed to be very customizable.  

The Django-JFU template tag optionally takes two arguments: the name of the
template to load and the name of the URL pointing to the upload-handling
view.::

    {% load jfutags %}
    {% jfu 'your_fileuploader.html' 'your_uploader_URL_name' %}

A custom template can extend from the master Django-JFU template
`jfu/upload_form.html`.  There are several blocks which may be overriden for
the purpose of customization:

* JS_OPTS - The options supplied to the jQuery File Upload ``fileupload`` function. 
* JS_INIT - The initializing JavaScript
* FILE_INPUT - The file input for the upload form.

The blocks above are most-likely what you will want to override when seeking to
customize. For instance, one would go about adding a few options to the
fileupload function in this manner::

    # your_fileuploader.html
    {% extends 'jfu/upload_form.html' %}
    
    {% block JS_OPTS %}
    autoUpload: true,
    maxNumberOfFiles: 5,
    sequentialUploads: true,
    {% endblock %}

There are several other blocks too:


HTML Components
===============

* MODAL_GALLERY - The modal gallery
* UPLOAD_FORM   - The file upload form used as target for the file upload widget.

  * UPLOAD_FORM_LISTING - The table listing the files available for upload/download.
  * UPLOAD_FORM_LINDICATOR - The loading indicator shown during file processing.
  * UPLOAD_FORM_PROGRESS_BAR - The global progress information.
  * UPLOAD_FORM_BUTTON_BAR - The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload.

    * UPLOAD_FORM_BUTTON_BAR_CONTROL - Contains buttons to start/cancel the upload or delete files. 
    * UPLOAD_FORM_BUTTON_BAR_ADD     - Contains the file input used to add files.
        * FILE_INPUT or UPLOAD_FORM_BUTTON_BAR_ADD_FILE_INPUT - Contains the file input.
        * UPLOAD_FORM_BUTTON_BAR_ADD_EXTRA - An empty block allowing the addition of extra inputs.
    * UPLOAD_FORM_BUTTON_BAR_EXTRA  - An empty block allowing the addition of extra components.

  * UPLOAD_FORM_EXTRA - An empty block allowing the addition of extra components.

CSS Components
==============

* CSS

  * CSS_BOOTSTRAP 
  * CSS_BLUEIMP_GALLERY 
  * CSS_JQUERY_FILE_UPLOAD
  * CSS_JQUERY_FILE_UPLOAD_UI
  * CSS_HTML5_SHIM 
  * CSS_EXTRA 

JS Components
=============

* JS_TEMPLATES 

  * JS_DOWNLOAD_TEMPLATE 

    * JS_DOWNLOAD_TEMPLATE_DELETE 
    * JS_DOWNLOAD_TEMPLATE_DOWNLOAD  
    * JS_DOWNLOAD_TEMPLATE_PREVIEW 
    * JS_DOWNLOAD_TEMPLATE_ERROR 
    * JS_DOWNLOAD_TEMPLATE_FSIZE 

  * JS_UPLOAD_TEMPLATE 
    * JS_UPLOAD_TEMPLATE_PREVIEW
    * JS_UPLOAD_TEMPLATE_UPLOAD
    * JS_UPLOAD_TEMPLATE_CONTROLS
        * JS_UPLOAD_TEMPLATE_START
        * JS_UPLOAD_TEMPLATE_CANCEL
    * JS_UPLOAD_TEMPLATE_PROGRESSBAR

* JS_SCRIPTS    

  * JS_JQUERY 
  * JS_JQUERY_UI_WIDGET
  * JS_TEMPLATES_PLUGIN
  * JS_LOAD_IMAGE
  * JS_CANVAS_TO_BLOB 
  * JS_BOOTSTRAP 
  * JS_BLUEIMP_GALLERY 
  * JS_BOOTSTRAP_IFRAME_TRANSPORT
  * JS_JQUERY_FILE_UPLOAD
  * JS_JQUERY_FILE_UPLOAD_FP
  * JS_JQUERY_FILE_UPLOAD_IMAGE
  * JS_JQUERY_FILE_UPLOAD_AUDIO
  * JS_JQUERY_FILE_UPLOAD_VIDEO
  * JS_JQUERY_FILE_UPLOAD_VALIDATE
  * JS_JQUERY_FILEUPLOAD_UI 
  * JS_XDR_TRANSPORT 
  * JS_EXTRA

The included JavaScript and CSS can be updated or suppressed by overriding
these blocks ::

    # your_fileuploader.html
    {% extends 'jfu/upload_form.html' %}

    {% block JS_JQUERY %}
        <script src={{STATIC_URL}}/js/my.newer.jquery.js />
    {% endblock %}

    {% block CSS_BOOTSTRAP %}
        {% comment %}
        This is already included.
        {% endcomment %}
    {% endblock %}

or by replacing the static files themselves.

Demo
----
If you have downloaded from the repository, a simple demo application has been
included in the 'demo' directory. 
To test it out, enter the 'demo' directory and run ::

        ./setup && ./run

Note that virtualenv is required for the demo to function.

Contribution
------------           
Django-JFU is wholly open source and welcomes contributions of any kind. Feel
free to either extend it, report bugs, or provide suggestions for improvements.
The author of Django-JFU can be contacted at alem@cidola.com.
