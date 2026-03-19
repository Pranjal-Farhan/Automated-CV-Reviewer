import { useState, useRef, useCallback, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { cvAPI } from "../api/cv";
import { useToast } from "./useToast";

const POLL_INTERVAL = 2500;
const MAX_POLL_TIME = 120000;

export function useCVUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null); // pending | processing | completed | failed
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const pollRef = useRef(null);
  const startTimeRef = useRef(null);
  const navigate = useNavigate();
  const { addToast } = useToast();

  const reset = useCallback(() => {
    setFile(null);
    setUploading(false);
    setJobId(null);
    setStatus(null);
    setProgress(0);
    setResult(null);
    setError(null);
    if (pollRef.current) clearInterval(pollRef.current);
  }, []);

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  const pollResult = useCallback(
    async (id) => {
      try {
        const res = await cvAPI.getResult(id);
        const data = res.data;

        setStatus(data.status);

        if (data.status === "processing") {
          const elapsed = Date.now() - startTimeRef.current;
          const pct = Math.min(85, (elapsed / MAX_POLL_TIME) * 100);
          setProgress(pct);
        }

        if (data.status === "completed") {
          stopPolling();
          setProgress(100);
          setResult(data);
          addToast("Analysis complete!", "success");
          // Navigate to result page
          setTimeout(() => navigate(`/result/${id}`), 600);
        }

        if (data.status === "failed") {
          stopPolling();
          setError("Analysis failed. Please try again.");
          addToast("Analysis failed", "error");
        }

        // Timeout check
        if (Date.now() - startTimeRef.current > MAX_POLL_TIME) {
          stopPolling();
          setError("Analysis timed out. Please try again.");
          addToast("Analysis timed out", "error");
        }
      } catch (err) {
        console.error("Poll error:", err);
      }
    },
    [stopPolling, addToast, navigate]
  );

  const upload = useCallback(
    async (selectedFile) => {
      if (!selectedFile) return;

      setError(null);
      setUploading(true);
      setProgress(5);
      setStatus("uploading");

      try {
        const res = await cvAPI.upload(selectedFile);
        const id = res.data.job_id;
        setJobId(id);
        setStatus("pending");
        setProgress(15);
        addToast("File uploaded — analysis started", "success");

        // Start polling
        startTimeRef.current = Date.now();
        pollRef.current = setInterval(() => pollResult(id), POLL_INTERVAL);
      } catch (err) {
        const msg =
          err.response?.data?.detail || "Upload failed. Please try again.";
        setError(msg);
        addToast(msg, "error");
        setStatus(null);
        setProgress(0);
      } finally {
        setUploading(false);
      }
    },
    [pollResult, addToast]
  );

  // Cleanup on unmount
  useEffect(() => {
    return () => stopPolling();
  }, [stopPolling]);

  return {
    file,
    setFile,
    uploading,
    jobId,
    status,
    progress,
    result,
    error,
    upload,
    reset,
  };
}
