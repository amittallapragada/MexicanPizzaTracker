import MapView from "../components/MapView";
import MapInput from "../components/MapInput";
import Hero from "../components/Hero";
import Nav from "../components/Nav";
import { useState } from "react";
function Home(props) {
  const [markers, setMarkers] = useState([]);

  return (
    <div class="grid grid-cols-5">
      <div class="col-span-5">
        <Nav />
      </div>

      <div class="col-start-2 col-end-5">
        <Hero />
      </div>

      <div class="col-start-1 col-span-5 pl-4 pr-4 z-10">
        <MapInput setMarkers={setMarkers} />
      </div>

      <div class="col-span-5 z-0">
        <MapView markers={markers.markers} />
      </div>
    </div>
  );
}
export default Home;
