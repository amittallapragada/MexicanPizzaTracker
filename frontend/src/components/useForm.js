import {useState } from 'react';

export const useForm = (initialForm) => {
    const [form, setForm] = useState({...initialForm});

    const change = (e, type="value") => {
        console.log(e, "IM HEREE")
        if(e instanceof Map){
            console.log("has label......")
        }
        if(type === "value"){
            console.log("VALUEEE", e.target.value)
            setForm({
                ...form,
                [e.target.name]: e.target.value,
            });
        }

    }

    const resetForm = () => setForm({...initialForm});

    return [form, change, resetForm];
}

export default useForm;