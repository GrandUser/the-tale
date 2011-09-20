
if (!window.pgf) {
    pgf = {};
}

if (!pgf.base) {
    pgf.base = {};
}

pgf.base.RenderTemplateList = function(selector, data, newElementCallback, params) {
    
    var container = jQuery(selector);
    var template = jQuery('.pgf-template', container).eq(0);
    var emptyTemplate = jQuery('.pgf-empty-template', container).eq(0);

    container.children().not('.pgf-template').not('.pgf-empty-template').remove();

    for (var i in data) {
        var elementData = data[i];

        var newElement = template
            .clone()
            .appendTo(container)
            .removeClass('pgf-template');

        newElement.addClass(i % 2 ? 'even' : 'odd');

        if (newElementCallback) {
            newElementCallback(i, elementData, newElement);
        }
    }

};

pgf.base.UpdateStatsBar = function(selector) {
    
    var widget = jQuery(selector);
    var width = widget.width();

    var base = arguments[1];

    for (var i=1; i<arguments.length; ++i)
    {
        var bar = jQuery('.pgf-layer-'+(i-1), widget);
        bar.width( Math.ceil( Math.min(arguments[i], base) / (base + 0.0) * width) );
    }
};


jQuery('.pgf-link-load-on-success').live('click', function(e){
    e.preventDefault();

    var el = jQuery(this);
    var href = el.attr('href');
    var dest = el.data('dest');

    pgf.forms.Post({action: href,
                    OnSuccess: function(data){
                        location.href = dest;
                    },
                    OnError: function(data){
                        alert(data.error);
                    }
                   });
});