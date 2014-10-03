this.seantis = this.seantis || {};

this.seantis.placemap = (function() {

    var self = this;
    var layers = [];

    // http://stackoverflow.com/questions/13375039/javascript-calculate-darker-colour
    self.darken_color = function(hex, percent) {
        // strip the leading # if it's there
        hex = hex.replace(/^\s*#|\s*$/g, '');

        // convert 3 char codes --> 6, e.g. `E0F` --> `EE00FF`
        if(hex.length == 3){
            hex = hex.replace(/(.)/g, '$1$1');
        }

        var r = parseInt(hex.substr(0, 2), 16),
            g = parseInt(hex.substr(2, 2), 16),
            b = parseInt(hex.substr(4, 2), 16);

        return '#' +
           ((0|(1<<8) + r * (1 - percent / 100)).toString(16)).substr(1) +
           ((0|(1<<8) + g * (1 - percent / 100)).toString(16)).substr(1) +
           ((0|(1<<8) + b * (1 - percent / 100)).toString(16)).substr(1);
    };

    self.create_kml_layer = function(url, title, color) {

        var defaultStyle = new OpenLayers.Style({
            'pointRadius': 8,
            'fillColor': color,
            'fillOpacity': 0.4,
            'strokeColor': self.darken_color(color, 0.2),
            'strokeWidth': 1
        });

        var selectStyle = new OpenLayers.Style({
            'pointRadius': 9,
            'fillColor': '#fff',
            'fillOpacity': 0.8,
            'strokeColor': self.darken_color(color, 0.2),
            'strokeWidth': 2
        });

        var style = new OpenLayers.StyleMap({
            'default': defaultStyle,
            'select': selectStyle
        });

        var layer = new OpenLayers.Layer.Vector(title, {
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.KML({
                    extractStyles: false,
                    extractAttributes: true
                })
            }),
            strategies: [new OpenLayers.Strategy.Fixed()],
            projection: new OpenLayers.Projection('EPSG:4326'),
            styleMap: style
        });

        layer.is_popup_layer = true;

        return layer;
    };

    self.get_popup_layers = function(map) {
        var popup_layers = [];
        for (var i=0; i<map.layers.length; i++) {
            if (map.layers[i].is_popup_layer === true) {
                popup_layers.push(map.layers[i]);
            }
        }
        return popup_layers;
    };

    self.enable_popups = function(map) {

        var on_popup_close = function(event) {
            select.unselectAll();
        };

        var on_feature_select = function(event) {
            var feature = event.feature;
            var content = "<h2>" + feature.attributes.name + "</h2>" + feature.attributes.description;

            var popup = new OpenLayers.Popup.FramedCloud(
                "chicken",
                feature.geometry.getBounds().getCenterLonLat(),
                new OpenLayers.Size(100,100),
                content,
                null,
                true,
                on_popup_close
            );

            feature.popup = popup;
            map.addPopup(popup);
        };

        var on_feature_unselect = function(event) {
            var feature = event.feature;

            if (feature.popup) {
                map.removePopup(feature.popup);
                feature.popup.destroy();
                delete feature.popup;
            }
        };

        var layers = self.get_popup_layers(map);
        var select = new OpenLayers.Control.SelectFeature(layers);

        for (var i=0; i<layers.length; i++) {
            layers[i].events.on({
                "featureselected": on_feature_select,
                "featureunselected": on_feature_unselect
            });
        }

        map.addControl(select);
        select.activate();
    };

    return self;
})();
