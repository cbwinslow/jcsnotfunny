import SocialLinks from './SocialLinks';

const Footer = () => {
  return (
    <footer>
      <div className="footer-content">
        <div className="footer-section">
          <h3>Jared's Not Funny</h3>
          <p>A comedy podcast exploring technology, culture, and everything in between.</p>
        </div>
        
        <div className="footer-section">
          <SocialLinks />
        </div>
        
        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
            <li><a href="/episodes">Episodes</a></li>
            <li><a href="/tour">Tour Dates</a></li>
            <li><a href="/contact">Contact</a></li>
          </ul>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} Jared's Not Funny. All rights reserved.</p>
        <div className="footer-legal">
          <a href="/privacy">Privacy Policy</a>
          <a href="/terms">Terms of Service</a>
        </div>
      </div>

      <style jsx>{`
        footer {
          background: #f8f8f8;
          padding: 3rem 1rem 1rem;
          margin-top: 2rem;
        }

        .footer-content {
          max-width: 1200px;
          margin: 0 auto;
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 2rem;
          margin-bottom: 2rem;
        }

        .footer-section h3 {
          font-size: 1.25rem;
          margin-bottom: 1rem;
        }

        .footer-section p {
          color: #666;
          margin-bottom: 1rem;
        }

        .footer-section ul {
          list-style: none;
          padding: 0;
        }

        .footer-section li {
          margin-bottom: 0.5rem;
        }

        .footer-section a {
          color: #333;
          text-decoration: none;
          transition: color 0.2s ease;
        }

        .footer-section a:hover {
          color: #000;
        }

        .footer-bottom {
          border-top: 1px solid #ddd;
          padding-top: 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .footer-bottom p {
          margin: 0;
          color: #666;
          font-size: 0.875rem;
        }

        .footer-legal {
          display: flex;
          gap: 1rem;
        }

        .footer-legal a {
          color: #666;
          font-size: 0.875rem;
          text-decoration: none;
        }

        .footer-legal a:hover {
          color: #000;
        }

        @media (max-width: 768px) {
          .footer-bottom {
            flex-direction: column;
            text-align: center;
          }
        }
      `}</style>
    </footer>
  );
};

export default Footer;
