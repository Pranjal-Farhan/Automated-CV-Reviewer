export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer__container">
        <p>
          &copy; {new Date().getFullYear()} CV Reviewer. Built with FastAPI,
          MongoDB &amp; Google Gemini.
        </p>
      </div>
    </footer>
  );
}
