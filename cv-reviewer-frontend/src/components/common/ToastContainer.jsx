import { useToast } from "../../hooks/useToast";
import { CheckCircle, XCircle, Info, X } from "lucide-react";

export default function ToastContainer() {
  const { toasts, removeToast } = useToast();

  const getIcon = (type) => {
    switch (type) {
      case "success":
        return <CheckCircle size={18} />;
      case "error":
        return <XCircle size={18} />;
      default:
        return <Info size={18} />;
    }
  };

  return (
    <div className="toast-container">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast--${toast.type}`}>
          <span className="toast__icon">{getIcon(toast.type)}</span>
          <span className="toast__message">{toast.message}</span>
          <button
            className="toast__close"
            onClick={() => removeToast(toast.id)}
          >
            <X size={14} />
          </button>
        </div>
      ))}
    </div>
  );
}
