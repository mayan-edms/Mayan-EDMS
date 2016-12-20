'use strict';

var resizeFullHeight = function () {
    $('.full-height').height($(window).height() - $('.full-height').data('height-difference'));
};

var set_image_noninteractive = function (image) {
    // Remove border to indicate non interactive image
    image.removeClass('thin_border');
    var container = image.parent().parent();
    // Save img HTML
    var html = image.parent().html();
    // Remove anchor
    image.parent().remove();
    // Place again img
    container.html(html);
};

var dismissAlert = function (element) {
    element.addClass('fadeOutUp').fadeOut('slow');
};

var onImageError = function (image) {
    image.parent().parent().html('<span class="fa-stack fa-lg"><i class="fa fa-file-o fa-stack-2x"></i><i class="fa fa-times fa-stack-1x text-danger"></i></span>');
    set_image_noninteractive(image);
};

var loadImage = function (image) {
    image.error(function(event) {
        onImageError(image);
    });

    image.attr('src', image.attr('data-url'));
};


var tagSelectionTemplate = function (tag, container) {
  var $tag = $(
    '<span class="label label-tag" style="background: ' + tag.element.style.color + ';"> ' + tag.text + '</span>'
  );
  container[0].style.background = tag.element.style.color;
  return $tag;
};


var tagResultTemplate = function (tag) {
  if (!tag.element) { return ''; }
  var $tag = $(
    '<span class="label label-tag" style="background: ' + tag.element.style.color + ';"> ' + tag.text + '</span>'
  );
  return $tag;
};

jQuery(document).ready(function() {
    $('.lazy-load').on('load', function() {
        $(this).siblings('.spinner').remove();
        $(this).removeClass('lazy-load');
    });

    $('.lazy-load-carousel').on('load', function() {
        $(this).siblings('.spinner').remove();
        $(this).removeClass('lazy-load-carousel');
    });

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

   $('img.lazy-load').lazyload({
        appear: function(elements_left, settings) {
            loadImage($(this));
        },
    });

    $('img.lazy-load-carousel').lazyload({
        appear: function(elements_left, settings) {
            loadImage($(this));
        },
        container: $("#carousel-container"),
        threshold: 400
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

    $('.select2').select2({
        templateSelection: tagSelectionTemplate,
        templateResult: tagResultTemplate
    });
});
