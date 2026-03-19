import { useState, useRef, useCallback } from "react";
import { Upload, File, X } from "lucide-react";
import { formatFileSize } from "../../utils/helpers";

const ALLOWED_TYPES = ["application/pdf", "text/plain"];
const ALLOWED_EXTENSIONS = [".pdf", ".txt"];
const MAX_SIZE = 10 * 1024 * 1024;

export default function Dropzone({ onUpload, uploading }) {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  const validateFile = useCallback((f) => {
    const ext = f.name.toLowerCase().slice(f.name.lastIndexOf("."));
    if (!ALLOWED_EXTENSIONS.includes(ext) && !ALLOWED_TYPES.includes(f.type)) {
      return "Only PDF and TXT files are allowed.";
    }
    if (f.size > MAX_SIZE) {
      return "File size exceeds 10 MB limit.";
    }
    if (f.size === 0) {
      return "File is empty.";
    }
    return null;
  }, []);

  const handleFile = useCallback(
    (f) => {
      const err = validateFile(f);
      if (err) {
        setError(err);
        setFile(null);
        return;
      }
      setError("");
      setFile(f);
    },
    [validateFile]
  );

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const f = e.dataTransfer.files?.[0];
    if (f) handleFile(f);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragActive(true);
  };

  const handleDragLeave = () => setDragActive(false);

  const handleInputChange = (e) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
    e.target.value = "";
  };

  const removeFile = () => {
    setFile(null);
    setError("");
  };

  const handleUploadClick = () => {
    if (file && onUpload) onUpload(file);
  };

  return (
    <div className="upload__card">
      {!file ? (
        <div
          className={`dropzone ${dragActive ? "dropzone--active" : ""}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => inputRef.current?.click()}
        >
          <div className="dropzone__icon">
            <Upload size={48} />
          </div>
          <p className="dropzone__text">
            Drag &amp; drop your file here, or{" "}
            <span className="dropzone__browse">browse</span>
          </p>
          <p className="dropzone__hint">PDF or TXT only — Max 10 MB</p>
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.txt,application/pdf,text/plain"
            onChange={handleInputChange}
            hidden
          />
        </div>
      ) : (
        <>
          <div className="file-preview">
            <div className="file-preview__info">
              <div className="file-preview__icon">
                <File size={24} />
              </div>
              <div className="file-preview__details">
                <span className="file-preview__name">{file.name}</span>
                <span className="file-preview__size">
                  {formatFileSize(file.size)}
                </span>
              </div>
            </div>
            <button
              className="file-preview__remove"
              onClick={removeFile}
              disabled={uploading}
            >
              <X size={18} />
            </button>
          </div>

          <button
            className="btn btn--primary btn--upload"
            onClick={handleUploadClick}
            disabled={uploading}
          >
            {uploading ? (
              <>
                <div className="btn-spinner" />
                Uploading...
              </>
            ) : (
              <>
                <Upload size={20} />
                Analyze My CV
              </>
            )}
          </button>
        </>
      )}

      {error && (
        <div className="message message--error" style={{ marginTop: "16px" }}>
          <X size={18} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
