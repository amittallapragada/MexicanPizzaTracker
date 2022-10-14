import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Row } from "react-bootstrap";
import { Col } from "react-bootstrap";
import Alert from "react-bootstrap/Alert";
import { Container } from "react-bootstrap";
import { Spinner } from "react-bootstrap";
import { useGeolocation } from "rooks";
import { getRestaurants } from "../network_calls";
import { useEffect } from "react";
import { useState } from "react";
import axios from "axios";
import useForm from "./useForm";
import MapView from "./MapView";
import "react-select/dist/react-select.css";
import "react-virtualized/styles.css";
import "react-virtualized-select/styles.css";
// Then import the virtualized Select HOC
import VirtualizedSelect from "react-virtualized-select";

axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  // dev code
  axios.defaults.baseURL = "http://0.0.0.0:8080";
} else {
  // production code
  axios.defaults.baseURL = "http://54.187.184.201:8080";
}

function DropDownList(data) {
  const dropDownList = data.map((rest) => (
    <option value={rest.value}>{rest.name}</option>
  ));
  return dropDownList;
}

function DropDownSelect(data) {
  let outputs = [];
  const dropDownList = data.map((rest) =>
    outputs.push({ label: rest.name, value: rest.value })
  );
  return outputs;
}

function GenButton(isLoading) {
  if (isLoading) {
    return (
      <button
        type="submit"
        class="drop-shadow-4xl inline-flex w-100 justify-content-center items-center px-4 py-2 font-bold leading-6 text-sm shadow rounded-md text-white bg-indigo-500 hover:bg-indigo-700 transition ease-in-out duration-150 cursor-not-allowed sm:w-2"
        disabled={true}
      >
        <svg
          class="animate-spin -ml-1 mr-3 h-5 w-5 text-green-400"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        Searching...
      </button>
    );
  } else {
    return (
      <button
        type="submit"
        class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-2 w-100 rounded sm:w-2"
        disabled={false}
      >
        Go!
      </button>
    );
  }
}

function ShowAlert(isAlert) {
  if (isAlert) {
    return (
      <div class="alert">
        <Alert variant={"danger"}>
          {" "}
          Something is wrong! Please ensure your location is valid or try again
          later.
        </Alert>
      </div>
    );
  } else {
    return <></>;
  }
}

function MapInput({ setMarkers }) {
  const [restaurants, setRestaurants] = useState([]);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState(false);
  let geoObj = useGeolocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(window.location.search);
    const restaurant = searchParams.get("restaurant");
    const item = searchParams.get("item");

    if (restaurant && item && restaurants) {
      setLoading(true);

      let valid_restaurant = false;
      let valid_item = false;
      restaurants.forEach(function (restItem) {
        if (restItem.value === restaurant) {
          valid_restaurant = true;
        }
      });
      if (valid_restaurant) {
        setLoading(true);
        axios
          .get("/get-items", { params: { restaurant: restaurant } })
          .then((response) => {
            setItems(response.data);
            console.log(response.data);
            response.data.forEach(function (foodItem) {
              if (foodItem.id === item) {
                console.log("TRUE", foodItem.name);
                valid_item = true;
              }
            });
          })
          .catch((err) => {
            console.log(err);
            setItems([]);
            valid_item = false;
          });
      }

      if (
        geoObj &&
        geoObj.isError === true &&
        !valid_item &&
        !valid_restaurant
      ) {
        setLoading(false);
      }
      if (geoObj && geoObj.isError === false) {
        queryForm.restaurant = restaurant;
        queryForm.item = item;
        queryForm.zip_code = "📍 Current Location";
        localStorage.setItem("USER_LAT", geoObj.lat.toString());
        localStorage.setItem("USER_LNG", geoObj.lng.toString());
        axios
          .get("/geojson-features", {
            params: {
              store: restaurant,
              item: item,
              lat: geoObj.lat.toString(),
              lon: geoObj.lng.toString(),
            },
          })
          .then((response) => {
            if (response.data.status === "success") {
              setMarkers(response.data);
            }
            setLoading(false);
          })
          .catch((err) => {
            console.log(err);
            setMarkers([]);
            setLoading(false);
          });
      }
    }
  }, [geoObj, restaurants]);

  useEffect(() => {
    axios
      .get("/get-restaurants")
      .then((response) => {
        setRestaurants(response.data);
      })
      .catch((err) => {
        console.log(err);
        setRestaurants([]);
      });
  }, []);

  const onRestaurantChange = (e) => {
    change(e);
    setLoading(true);
    axios
      .get("/get-items", { params: { restaurant: e.target.value } })
      .then((response) => {
        console.log(response.data);
        setItems(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log(err);
        setItems([]);
        setLoading(false);
      });
  };

  const initQueryForm = {
    restaurant: null,
    item: "",
    zip_code: null,
  };
  let [queryForm, change, resetQueryForm] = useForm(initQueryForm);

  function onSubmit(event) {
    event.preventDefault();
    setLoading(true);
    if (queryForm.item && queryForm.restaurant && queryForm.zip_code) {
      let urlParams = {
        store: queryForm.restaurant,
        item: queryForm.item,
      };
      if (
        queryForm.zip_code !== "📍 Current Location" &&
        queryForm.zip_code !== ""
      ) {
        urlParams.zip_code = queryForm.zip_code;
      } else if (localStorage.getItem("USER_LAT")) {
        urlParams.lat = localStorage.getItem("USER_LAT");
        urlParams.lon = localStorage.getItem("USER_LNG");
      }

      axios
        .get("/geojson-features", { params: urlParams })
        .then((response) => {
          console.log(response.data);
          if (response.data.status === "success") {
            setMarkers(response.data);
          }
          setLoading(false);
          setAlert(false);
        })
        .catch((err) => {
          console.log(err);
          setMarkers([]);
          setLoading(false);
          setAlert(true);
        });
    } else {
      setAlert(true);
      setLoading(false);
    }
  }

  function dropDownSelectChange(e) {
    change({ target: { name: "item", value: e.value } });
  }
  if (restaurants) {
    return (
      <div class="map-input">
        <div>
          <Form onSubmit={onSubmit}>
            <Container>
              <div class="grid grid-cols-1 justify-content-center sm:grid-cols-4 gap-4">
                <div class="col-span-1">
                  <Form.Group controlId="form.Name">
                    <Form.Select
                      aria-label="Restaurant Name"
                      name="restaurant"
                      value={queryForm.restaurant}
                      onChange={onRestaurantChange}
                    >
                      <option>Select a Restaurant</option>
                      {DropDownList(restaurants)}
                    </Form.Select>
                  </Form.Group>
                </div>
                <div class="col-span-1">
                  <Form.Group controlId="form.Name">
                    <VirtualizedSelect
                      disabled={queryForm.restaurant === null && items}
                      options={DropDownSelect(items)}
                      onChange={dropDownSelectChange}
                      value={queryForm.item}
                    />
                  </Form.Group>
                </div>
                <div class="col-span-1">
                  <Form.Group controlId="form.Name">
                    <Form.Control
                      type="text"
                      name="zip_code"
                      value={queryForm.zip_code}
                      onChange={change}
                      placeholder="Enter Zip Code"
                    />
                  </Form.Group>
                </div>
                <div class="col-span-1">{GenButton(loading)}</div>
              </div>
              <Row className="justify-content-md-center">
                {ShowAlert(alert)}
              </Row>
            </Container>
          </Form>
        </div>
        <div className="spacer"></div>
      </div>
    );
  } else {
    return <div></div>;
  }
}
export default MapInput;
