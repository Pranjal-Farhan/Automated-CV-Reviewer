import api from "./axios";

export const cvAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return api.post("/cv/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  getResult: (jobId) => api.get(`/cv/result/${jobId}`),
  getHistory: () => api.get("/cv/history"),
};
