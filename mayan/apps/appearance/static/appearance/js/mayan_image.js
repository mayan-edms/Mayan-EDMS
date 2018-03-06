'use strict';

var MayanImage = function (options) {
    this.element = options.element;
    this.load();
}

MayanImage.intialize = function () {
    $('a.fancybox').fancybox({
        beforeShow : function(){
            this.title = $(this.element).data('caption');
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
            new MayanImage({element: $(this)});
        },
        threshold: 400,
    });

    $('img.lazy-load-carousel').lazyload({
        appear: function(elements_left, settings) {
            new MayanImage({element: $(this)});
        },
        container: $('#carousel-container'),
        threshold: 2000
    });

    $('.lazy-load').on('load', function() {
        $(this).hide();
        $(this).fadeIn();
        $(this).siblings('.spinner-container').remove();
        $(this).removeClass('lazy-load pull-left');
    });

    $('.lazy-load-carousel').on('load', function() {
        $(this).hide();
        $(this).fadeIn();
        $(this).siblings('.spinner-container').remove();
        $(this).removeClass('lazy-load-carousel pull-left');
    });
}

MayanImage.prototype.onImageError = function () {
    this.element.parent().parent().html('\
        <div class="fa-3x">\
            <span class="fa-layers fa-fw">\
                <i class="far fa-file"></i>\
                <i class="fa-inverse fas fa-times text-danger" data-fa-transform="shrink-6"></i>\
            </span>\
        </div>\
    ')

    // Remove border to indicate non interactive image
    this.element.removeClass('thin_border');

    var container = this.element.parent().parent();
    // Save img HTML
    var html = this.element.parent().html();
    // Remove anchor
    this.element.parent().remove();
    // Place again img
    container.html(html);
};

MayanImage.prototype.load = function () {
    var self = this;

    this.element.error(function(event) {
        self.onImageError();
    });

    this.element.attr('src', this.element.attr('data-url'));
    $.fn.matchHeight._update();
    $.fn.matchHeight._maintainScroll = true;
};
