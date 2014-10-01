this.seantis = this.seantis || {};

this.seantis.placemap = (function() {

    var self = this;
    var layers = [];

    self.create_kml_layer = function(url, title) {
        var layer = new OpenLayers.Layer.Vector(title, {
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.KML({
                    extractStyles: true,
                    extractAttributes: true
                })
            }),
            strategies: [new OpenLayers.Strategy.Fixed()],
            projection: new OpenLayers.Projection('EPSG:4326')
        });

        layer.is_placemap = true;

        return layer;
    };

    self.enable_popups = function(map) {
        for (var i=0; i<map.layers.length; i++) {
            if (map.layers[i].is_placemap === true) {
                self.enable_popups_on_layer(map, map.layers[i]);
            }
        }
    };
    self.enable_popups_on_layer = function(map, layer) {
        var select = new OpenLayers.Control.SelectFeature(layer);

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

        layer.events.on({
            "featureselected": on_feature_select,
            "featureunselected": on_feature_unselect
        });

        map.addControl(select);
        select.activate();
    };

    return self;
})();
