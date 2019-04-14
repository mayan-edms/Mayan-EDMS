'use strict';

class MayanImage {
    constructor (options) {
        this.element = options.element;
        this.load();
    }

    static intialize (options) {
        this.options = options || {};
        this.options.templateInvalidDocument = this.options.templateInvalidDocument || '<span>Error loading document image</span>';

        $().fancybox({
            afterShow: function (instance, current) {
                $('a.a-caption').on('click', function(event) {
                    instance.close(true);
                });
            },
            animationEffect: 'fade',
            animationDuration : 100,
            buttons : [
                'fullScreen',
                'close',
            ],
            infobar: true,
            selector: 'a.fancybox'
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
            $(this).show();
            $(this).siblings('.spinner-container').remove();
            $(this).removeClass('lazy-load pull-left');
            clearTimeout(MayanImage.timer);
            MayanImage.timer = setTimeout(MayanImage.timerFunction, 250);
        });

        $('.lazy-load-carousel').one('load', function() {
            $(this).hide();
            $(this).show();
            $(this).siblings('.spinner-container').remove();
            $(this).removeClass('lazy-load-carousel pull-left');
        });
    }

    static timerFunction () {
        $.fn.matchHeight._update();
    }

    load () {
        var self = this;
        var container = this.element.parent().parent().parent();
        var dataURL = this.element.attr('data-url');

        if (dataURL === '') {
            container.html(MayanImage.options.templateInvalidDocument);
        } else {
            this.element.attr('src', dataURL);
            setTimeout(function () {
                self.element.on('error', function () {
                    // Check the .complete property to see if it is a real
                    // error or it was a cached image
                    if (this.complete === false) {
                        // It is a cached image, set the src attribute to
                        // trigger its display.
                        this.src = dataURL;
                    } else {
                        container.html(
                            MayanImage.options.templateInvalidDocument
                        );
                    }
                });
            }, 1);
        }
    };
}

MayanImage.timer = setTimeout(null);

$.fn.matchHeight._maintainScroll = true;

