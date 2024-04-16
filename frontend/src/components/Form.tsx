import { SetStateAction, useState } from "react";
import "../App.css";

export function Form({ onFormSubmit }: { onFormSubmit: (data: string) => void }) {
    const [formData, setFormData] = useState('');

    const handleInputChange = (event: { target: { value: SetStateAction<string>; }; }) => {
        setFormData(event.target.value);
    };

    const handleSubmit = () => {
        onFormSubmit(formData);
    };

    return (
        <div>
            <input className="input-form" type="text" placeholder="Enter your name" onChange={handleInputChange} />
            <button className="submit" onClick={handleSubmit}>Submit</button>
        </div>
    );
}  