import { Code } from "lucide-react";

export default function RawResponse({ data }) {
  if (!data) return null;

  const content =
    typeof data === "string" ? data : JSON.stringify(data, null, 2);

  return (
    <details className="raw-response">
      <summary className="raw-response__toggle">
        <Code size={18} />
        View Raw AI Response
      </summary>
      <pre className="raw-response__content">{content}</pre>
    </details>
  );
}
