// Response.tsx
import "../App.css";

export function Response({ response }: { response: string }) {
    return response && <div className="response"><pre>{response}</pre></div>;
}