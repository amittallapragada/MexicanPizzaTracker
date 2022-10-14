import L, { icon } from 'leaflet';


function createIcon(icon_url) {
    const current_icon = new L.Icon({
        iconUrl: icon_url,
        iconSize:     [40, 40],
        shadowSize:   [50, 64],
        iconAnchor:   [22, 94],
        shadowAnchor: [4, 62],
        popupAnchor:  [-3, -76],
        // iconSize: new L.Point(30, 30),
        className: 'leaflet-div-icon'
    });
    return current_icon;
}

    




export default createIcon;