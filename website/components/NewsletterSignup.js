import { useState } from 'react';

const NewsletterSignup = () => {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('idle'); // 'idle', 'loading', 'success', 'error'
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email || !email.includes('@')) {
      setStatus('error');
      setMessage('Please enter a valid email address');
      return;
    }

    setStatus('loading');
    
    try {
      // This would typically call an API endpoint
      // For now, we'll simulate a successful submission
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setStatus('success');
      setMessage('Thank you for subscribing! Check your email for confirmation.');
      setEmail('');
      
      // Reset after 5 seconds
      setTimeout(() => {
        setStatus('idle');
        setMessage('');
      }, 5000);
    } catch (error) {
      setStatus('error');
      setMessage('Subscription failed. Please try again later.');
      console.error('Newsletter signup error:', error);
    }
  };

  return (
    <section className="newsletter-signup">
      <div className="newsletter-container">
        <h2>Stay Updated</h2>
        <p>Get new episodes, behind-the-scenes content, and exclusive updates delivered to your inbox.</p>

        <form onSubmit={handleSubmit} className="newsletter-form">
          <div className="form-group">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              required
              disabled={status === 'loading'}
              className="email-input"
            />
            <button
              type="submit"
              disabled={status === 'loading'}
              className="submit-button"
            >
              {status === 'loading' ? 'Subscribing...' : 'Subscribe'}
            </button>
          </div>

          {message && (
            <div className={`message ${status}`}>
              {message}
            </div>
          )}

          <div className="privacy-note">
            <p>We respect your privacy. No spam, ever. Unsubscribe anytime.</p>
          </div>
        </form>
      </div>

      <style jsx>{`
        .newsletter-signup {
          background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
          padding: 3rem 1rem;
          text-align: center;
        }

        .newsletter-container {
          max-width: 600px;
          margin: 0 auto;
        }

        .newsletter-signup h2 {
          font-size: 2rem;
          margin-bottom: 1rem;
          color: #333;
        }

        .newsletter-signup p {
          margin-bottom: 2rem;
          color: #666;
          font-size: 1.1rem;
        }

        .newsletter-form {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .form-group {
          display: flex;
          gap: 0.5rem;
          max-width: 500px;
          margin: 0 auto;
        }

        .email-input {
          flex: 1;
          padding: 1rem;
          border: 2px solid #ddd;
          border-radius: 0.5rem 0 0 0.5rem;
          font-size: 1rem;
          transition: border-color 0.3s ease;
        }

        .email-input:focus {
          outline: none;
          border-color: #007bff;
        }

        .submit-button {
          padding: 1rem 1.5rem;
          background: #000;
          color: white;
          border: none;
          border-radius: 0 0.5rem 0.5rem 0;
          font-size: 1rem;
          cursor: pointer;
          transition: background-color 0.3s ease;
        }

        .submit-button:hover {
          background: #333;
        }

        .submit-button:disabled {
          background: #666;
          cursor: not-allowed;
        }

        .message {
          padding: 0.75rem;
          border-radius: 0.5rem;
          margin-top: 0.5rem;
          font-weight: bold;
        }

        .message.success {
          background: #d4edda;
          color: #155724;
        }

        .message.error {
          background: #f8d7da;
          color: #721c24;
        }

        .privacy-note {
          font-size: 0.875rem;
          color: #666;
          margin-top: 1rem;
        }

        @media (max-width: 768px) {
          .form-group {
            flex-direction: column;
          }

          .email-input {
            border-radius: 0.5rem;
          }

          .submit-button {
            border-radius: 0.5rem;
          }
        }
      `}</style>
    </section>
  );
};

export default NewsletterSignup;