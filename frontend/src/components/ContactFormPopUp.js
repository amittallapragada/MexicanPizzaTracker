import React from "react";
import Popup from "reactjs-popup";
import { useState } from "react";
import { useForm } from "./useForm";
import Form from "react-bootstrap/Form";
import axios from "axios";
import Alert from "react-bootstrap/Alert";

axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  // dev code
  axios.defaults.baseURL = "http://0.0.0.0:8080";
} else {
  // production code
  axios.defaults.baseURL = "http://54.187.184.201:8080";
}

function ShowAlert(alert) {
  if (alert.enabled) {
    return (
      <div class="alert">
        <Alert variant={alert.type}>{alert.message}</Alert>
      </div>
    );
  } else {
    return <></>;
  }
}

function GenButton(isLoading, close) {
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
        Sending...
      </button>
    );
  } else {
    return (
      <button
        type="submit"
        class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-2 w-100 rounded sm:w-2"
        disabled={false}
      >
        Submit
      </button>
    );
  }
}

function ContactFormPopup() {
  const initContactForm = {
    from_email: "",
    subject: "",
    message: "",
  };
  let [loading, setLoading] = useState(false);
  let [alert, setAlert] = useState({
    enabled: false,
    type: null,
    message: null,
  });
  let [contactForm, change, resetContactForm] = useForm(initContactForm);
  const contentStyle = { background: "#000" };
  const overlayStyle = { background: "rgba(0,0,0,0.5)" };
  const arrowStyle = { color: "#000" }; // style for an svg element
  function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    axios
      .post("/send-email", {
        data: {
          template_name: "feature_request",
          params: {
            subject: contactForm.subject,
            from_email: contactForm.from_email,
            message: contactForm.message,
          },
        },
      })
      .then((response) => {
        setLoading(false);
        setAlert({
          enabled: true,
          type: "success",
          message:
            "We got your email! We will respond to you as soon as possible. Thank you!",
        });
      })
      .catch((err) => {
        console.log(err);
        setLoading(false);
        setAlert({
          enabled: true,
          type: "danger",
          message:
            "Our bad, something went wrong. Please try again later or email us directly at amithypeeats@gmail.com",
        });
      });
    resetContactForm();
  }
  return (
    <div>
      <Popup
        trigger={
          <button className="button bg-indigo-500 hover:bg-indigo-700 rounded px-4 py-2 text-white font-bold shadow-md">
            Suggest an Item
          </button>
        }
        {...{
          contentStyle,
          overlayStyle,
          arrowStyle,
        }}
        modal
      >
        {(close) => (
          <div class="bg-white px-4 py-4 h-70 items-center content-center">
            <div class="flex items-center justify-center">
              <div class="mx-auto w-full">
                <button
                  type="button"
                  onClick={close}
                  class="close bg-white rounded-md inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none"
                >
                  <span class="sr-only">Close menu</span>
                  <svg
                    class="h-6 w-6"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    aria-hidden="true"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
                <h1 class="popup-header">Suggest an Item</h1>
                <p>
                  Have a favorite item that keeps running out stock at a fast
                  food restaurant? Let us know! Send us the item's name and
                  restaurant and we will try our best to add it 😊
                </p>
                <Form onSubmit={onSubmit}>
                  <div class="mb-3">
                    <label
                      for="from_email"
                      class="mb-3 block text-base font-medium text-[#07074D]"
                    >
                      Email Address
                    </label>
                    <input
                      type="email"
                      name="from_email"
                      id="from_email"
                      placeholder="example@domain.com"
                      required={true}
                      value={contactForm.from_email}
                      onChange={change}
                      class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                  </div>
                  <div class="mb-3">
                    <label
                      for="subject"
                      class="mb-3 block text-base font-medium text-[#07074D]"
                    >
                      Subject
                    </label>
                    <input
                      type="text"
                      name="subject"
                      id="subject"
                      placeholder="Enter your subject"
                      required={true}
                      value={contactForm.subject}
                      onChange={change}
                      class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                  </div>
                  <div class="mb-3">
                    <label
                      for="message"
                      class="mb-3 block text-base font-medium text-[#07074D]"
                    >
                      Message
                    </label>
                    <textarea
                      rows="4"
                      name="message"
                      id="message"
                      placeholder="Type your message"
                      required={true}
                      value={contactForm.message}
                      onChange={change}
                      class="w-full resize-none rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    ></textarea>
                  </div>
                  <div>{GenButton(loading)}</div>
                  {ShowAlert(alert)}
                </Form>
              </div>
            </div>
          </div>
        )}
      </Popup>
    </div>
  );
}

export default ContactFormPopup;
