import axios from 'axios';
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    // dev code
    axios.defaults.baseURL = 'http://0.0.0.0:8080';

} else {
    // production code
    axios.defaults.baseURL = 'http://54.187.184.201:8080';

}

export function getRestaurants(){

    return axios.get("/get-restaurants")
    .then((response) => {
        console.log(response.data)
        return response.data;
    })
    .catch((err) => {
        console.log(err)
        return null;
    })
    
}