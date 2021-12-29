'use strict';

class MayanImage {
    constructor (options) {
        this.element = options.element;
        this.load();
    }

    static async setup (options) {
        this.options = options || {};
        this.options.templateInvalidImage = this.options.templateInvalidImage || '<span>Error loading image</span>';

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
            idleTime: false,
            infobar: true,
            selector: 'a.fancybox',
        });
    }

    static async intialize () {
        $('img.lazy-load').lazyload({
            appear: async function(elements_left, settings) {
                new MayanImage({element: $(this)});
            },
            threshold: 400,
        });

        $('img.lazy-load-carousel').lazyload({
            appear: async function(elements_left, settings) {
                new MayanImage({element: $(this)});
            },
            container: $('#carousel-container'),
            threshold: 2000,
        });

        $('.lazy-load').on('load', function() {
            const $this = $(this);

            $this.siblings('.spinner-container').remove();
            $this.removeClass('lazy-load pull-left');
            clearTimeout(MayanImage.timer);
            MayanImage.timer = setTimeout(MayanImage.timerFunction, 250);
        });

        $('.lazy-load-carousel').on('load', function() {
            const $this = $(this);

            $this.siblings('.spinner-container').remove();
            $this.removeClass('lazy-load-carousel pull-left');
        });
    }

    static timerFunction () {
        $.fn.matchHeight._update();
    }

    async load () {
        const self = this;
        const container = this.element.parent().parent().parent();
        const dataURL = this.element.attr('data-url');

        if (dataURL === '') {
            container.html(MayanImage.options.templateInvalidImage);
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
                            MayanImage.options.templateInvalidImage
                        );
                    }
                });
            }, 1);
        }
    };
}

MayanImage.timer = setTimeout(null);

$.fn.matchHeight._maintainScroll = true;
