'use strict';

class MayanImage {
    constructor (options) {
        this.element = options.element;
        this.load();
    }

    static intialize () {
        var app = this;

        this.fancybox = $().fancybox({
            animationDuration : 300,
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

        $('.lazy-load').one('load', function() {
            $(this).hide();
            $(this).fadeIn(300);
            $(this).siblings('.spinner-container').remove();
            $(this).removeClass('lazy-load pull-left');
            clearTimeout(MayanImage.timer);
            MayanImage.timer = setTimeout(MayanImage.timerFunction, 100);
        });

        $('.lazy-load-carousel').one('load', function() {
            $(this).hide();
            $(this).fadeIn(300);
            $(this).siblings('.spinner-container').remove();
            $(this).removeClass('lazy-load-carousel pull-left');
        });
    }

    static timerFunction () {
        $.fn.matchHeight._maintainScroll = true;
        $.fn.matchHeight._update();
    }

    load () {
        var self = this;
        var container = this.element.parent().parent().parent();

        this.element.attr('src', this.element.attr('data-url'));
        this.element.on('error', function() {
            // Check the .complete property to see if it is a real error
            // or it was a cached image
            if (this.complete === false) {
                // It is a cached image, set the src attribute to trigger
                // it's display.
                this.src = this.src;
            } else {
                container.html(MayanImage.templateInvalidDocument);
            }
        });

        $.fn.matchHeight._maintainScroll = true;
    };
}

MayanImage.templateInvalidDocument = $('#template-invalid-document').html();
MayanImage.timer = setTimeout(null);
