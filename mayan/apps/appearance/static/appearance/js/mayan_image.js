'use strict';

var MayanImage = function (options) {
    this.element = options.element;
    this.load();
}

MayanImage.intialize = function () {
    var app = this;

    this.fancybox = $().fancybox({
        animationDuration : 400,
        buttons : [
            'fullScreen',
            'close',
        ],
        selector: 'a.fancybox',
        afterShow: function (instance, current) {
            $('a.a-caption').on('click', function(event) {
                instance.close(true);
            });
        },
        infobar: true,

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
        threshold: 2000,
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

MayanImage.templateInvalidDocument = $('#template-invalid-document').html();


MayanImage.prototype.load = function () {
    var self = this;
    var container = this.element.parent().parent().parent();

    this.element.on('error', (function(event) {
        container.html(MayanImage.templateInvalidDocument);
    }));

    this.element.attr('src', this.element.attr('data-url'));
    $.fn.matchHeight._update();
    $.fn.matchHeight._maintainScroll = true;
};
