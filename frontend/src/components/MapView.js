import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { useGeolocation } from "rooks";
import { useMap } from "react-leaflet";
import createIcon from "./Icon";

function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

function MapView(props) {
  let geoObj = useGeolocation();
  console.log("GEO ", JSON.stringify(geoObj));
  if (!geoObj || (geoObj && geoObj.isError === true)) {
    geoObj = {
      lat: "37.3861",
      lng: "-122.0839",
    };
  } else {
    geoObj.lat = geoObj.lat.toString();
    geoObj.lng = geoObj.lng.toString();
  }
  const OPEN_STREET_MAP_TILES_URL =
    "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png";
  const SAD_ICON = "https://cdn-icons-png.flaticon.com/512/599/599426.png";
  const UNKNOWN_ICON =
    "https://cdn-icons-png.flaticon.com/512/5978/5978029.png";
  if (props.markers) {
    const happy_icon = createIcon(props.markers.item_icon);
    const sad_icon = createIcon(SAD_ICON);
    const unknown_icon = createIcon(UNKNOWN_ICON);
    return (
      <div className="map-holder">
        <MapContainer
          className="markercluster-map"
          center={[props.markers.stores[0].lat, props.markers.stores[0].lon]}
          zoom={12}
          maxZoom={18}
        >
          <ChangeView
            center={[props.markers.stores[0].lat, props.markers.stores[0].lon]}
            zoom={12}
          />
          <TileLayer
            url={OPEN_STREET_MAP_TILES_URL}
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          />
          {props.markers.stores.map((mark) => (
            <Marker
              position={[mark.lat, mark.lon]}
              icon={
                mark.available === true
                  ? happy_icon
                  : mark.available === false
                  ? sad_icon
                  : mark.available === "Inconclusive"
                  ? unknown_icon
                  : unknown_icon
              }
            >
              {mark.available === true ? (
                <Popup>
                  {mark.address + " has the " + props.markers.item_name}
                </Popup>
              ) : mark.available === false ? (
                <Popup>
                  {mark.address +
                    " does not have the " +
                    props.markers.item_name}
                </Popup>
              ) : mark.available === "Inconclusive" ? (
                <Popup>
                  {"Unable to get information from the " +
                    mark.address +
                    " store"}
                </Popup>
              ) : (
                <Popup>{"Something is wrong"}</Popup>
              )}
            </Marker>
          ))}
        </MapContainer>
      </div>
    );
  } else {
    return (
      <MapContainer
        className="markercluster-map"
        center={[geoObj.lat, geoObj.lng]}
        zoom={12}
        maxZoom={18}
      >
        <TileLayer
          url={OPEN_STREET_MAP_TILES_URL}
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        />
      </MapContainer>
    );
  }
}

export default MapView;
