export function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
}

export function formatDate(dateString) {
  if (!dateString) return "—";
  const d = new Date(dateString);
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function getStatusColor(status) {
  switch (status) {
    case "completed":
      return "var(--clr-success)";
    case "processing":
      return "var(--clr-accent-amber)";
    case "failed":
      return "var(--clr-error)";
    default:
      return "var(--clr-text-dim)";
  }
}

export function getInitials(name) {
  if (!name) return "?";
  return name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

/**
 * Safely parse the AI analysis result.
 * The backend might return it as a JSON string or as an object.
 */

/**
 * Strip markdown code block wrappers from AI response.
 * Gemini often returns: ```json\n{...}\n```
 */
function stripMarkdownCodeBlock(str) {
  if (typeof str !== "string") return str;

  let cleaned = str.trim();

  // Remove ```json ... ``` or ```JSON ... ``` or ``` ... ```
  const codeBlockRegex = /^```(?:json|JSON)?\s*\n?([\s\S]*?)\n?\s*```$/;
  const match = cleaned.match(codeBlockRegex);
  if (match) {
    cleaned = match[1].trim();
  }

  // Sometimes there's text before/after the code block
  // Try to extract JSON from anywhere in the string
  if (!cleaned.startsWith("{") && !cleaned.startsWith("[")) {
    // Look for JSON object
    const jsonObjectMatch = cleaned.match(/\{[\s\S]*\}/);
    if (jsonObjectMatch) {
      cleaned = jsonObjectMatch[0];
    }
  }

  return cleaned;
}

/**
 * Safely parse the AI analysis result.
 * Handles: JSON string, markdown-wrapped JSON, plain object, or raw text.
 */
export function parseAnalysis(result) {
  if (!result) return null;

  // Already an object — return directly
  if (typeof result === "object" && !Array.isArray(result)) {
    return result;
  }

  if (typeof result === "string") {
    // Step 1: Strip markdown code blocks
    const cleaned = stripMarkdownCodeBlock(result);

    // Step 2: Try to parse as JSON
    try {
      const parsed = JSON.parse(cleaned);
      if (typeof parsed === "object") {
        return parsed;
      }
    } catch {
      // Not valid JSON
    }

    // Step 3: Try to find and extract JSON from within the text
    try {
      const jsonMatch = result.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        if (typeof parsed === "object") {
          return parsed;
        }
      }
    } catch {
      // Still not valid JSON
    }

    // Step 4: Return as raw text
    return { raw: result };
  }

  return { raw: String(result) };
}
