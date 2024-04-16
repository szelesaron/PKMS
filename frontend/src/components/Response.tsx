import "../App.css";

export function Message({ message }: { message: string }) {
    return message && <div className="response">{message}</div>;
}  