'use strict';

function resizeFullHeight() {
    $('.full-height').height($(window).height() - $('.full-height').data('height-difference'));
}

function set_image_noninteractive(image) {
    // Remove border to indicate non interactive image
    image.removeClass('thin_border');
    container = image.parent().parent();
    // Save img HTML
    html = image.parent().html();
    // Remove anchor
    image.parent().remove();
    // Place again img
    container.html(html);
}

function load_document_image(image) {
    $.get( image.attr('data-src'), function(result) {
        image.attr('src', result.data);
        image.addClass(image.attr('data-post-load-class'));
    })
    .fail(function() {
        image.parent().parent().html('<span class="fa-stack fa-lg"><i class="fa fa-file-o fa-stack-2x"></i><i class="fa fa-times fa-stack-1x text-danger"></i></span>');
        set_image_noninteractive(image);
    })
}

function dismissAlert(element) {
    element.addClass('fadeOutUp').fadeOut('slow');
}

jQuery(document).ready(function() {
    resizeFullHeight();

    $(window).resize(function() {
        resizeFullHeight();
    });

    $('.scrollable').scrollview();

    $('a.fancybox').fancybox({
        beforeShow : function(){
            this.title =  $(this.element).data('caption');
        },
        openEffect  : 'elastic',
        closeEffect : 'elastic',
        prevEffect  : 'none',
        nextEffect  : 'none',
        titleShow   : true,
        type        : 'image',
        autoResize  : true,
    });

    $('a.fancybox-staging').click(function(e) {
        var $this = $(this);

            $.get($this.attr('href'), function( result ) {
                if (result.status == 'success') {
                    $.fancybox.open([
                        {
                            href : result.data,
                            title : $this.attr('title'),
                            openEffect  : 'elastic',
                            closeEffect : 'elastic',
                            prevEffect  : 'none',
                            nextEffect  : 'none',
                            titleShow   : true,
                            type        : 'image',
                            autoResize  : true,
                        },
                    ]);
                }
            })
        e.preventDefault();
    })

   $('img.lazy-load').lazyload({
        appear: function(elements_left, settings) {
            load_document_image($(this));
        },
    });

    $('img.lazy-load-carousel').lazyload({
        threshold : 400,
        container: $("#carousel-container"),
        appear: function(elements_left, settings) {
            var $this = $(this);
            $this.removeClass('lazy-load-carousel');
            load_document_image($this);
        },
    });

    $('th input:checkbox').click(function(e) {
        var table = $(e.target).closest('table');
        var checked = $(e.target).prop('checked');
        $('td input:checkbox', table).prop('checked', checked);
    });

    $('a.new_window').click(function(event) {
        event.preventDefault();
        var newWindow = window.open($(this).attr('href'), '_blank');
        newWindow.focus();
    });

    $('.alert button.close').click(function() {
        dismissAlert($(this).parent());
    });

    setTimeout(function() {
        $('.alert-success').each(function() {
            dismissAlert($(this));
        });

    }, 3000);
});
