import { useState } from 'react';

const SocialShare = ({ title, url, description, image }) => {
  const [copyStatus, setCopyStatus] = useState('Copy Link');
  
  const shareUrl = typeof window !== 'undefined' ? window.location.href : url || 'https://jcsnotfunny.com';
  const shareTitle = title || "Jared's Not Funny Podcast";
  const shareDescription = description || "A comedy podcast exploring technology, culture, and everything in between.";
  const shareImage = image || 'https://jcsnotfunny.com/images/og-image.jpg';

  const socialPlatforms = [
    {
      name: 'Twitter',
      icon: '🐦',
      url: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareTitle)}&url=${encodeURIComponent(shareUrl)}`,
      color: '#1DA1F2'
    },
    {
      name: 'Facebook',
      icon: '📘',
      url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`,
      color: '#1877F2'
    },
    {
      name: 'LinkedIn',
      icon: '💼',
      url: `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(shareTitle)}&summary=${encodeURIComponent(shareDescription)}`,
      color: '#0A66C2'
    },
    {
      name: 'Reddit',
      icon: '👽',
      url: `https://www.reddit.com/submit?url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(shareTitle)}`,
      color: '#FF4500'
    },
    {
      name: 'Email',
      icon: '✉️',
      url: `mailto:?subject=${encodeURIComponent(shareTitle)}&body=${encodeURIComponent(`${shareDescription}\n\n${shareUrl}`)}`,
      color: '#666666'
    }
  ];

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareUrl).then(() => {
      setCopyStatus('Copied!');
      setTimeout(() => setCopyStatus('Copy Link'), 2000);
    });
  };

  return (
    <div className="social-share">
      <h3>Share This Episode</h3>
      <div className="share-platforms">
        {socialPlatforms.map((platform) => (
          <a
            key={platform.name}
            href={platform.url}
            target="_blank"
            rel="noopener noreferrer"
            className="share-button"
            style={{ backgroundColor: platform.color }}
            aria-label={`Share on ${platform.name}`}
          >
            <span className="platform-icon">{platform.icon}</span>
            <span className="platform-name">{platform.name}</span>
          </a>
        ))}
        
        <button
          onClick={copyToClipboard}
          className="share-button copy-button"
          aria-label="Copy link to clipboard"
        >
          <span className="platform-icon">🔗</span>
          <span className="platform-name">{copyStatus}</span>
        </button>
      </div>

      <style jsx>{`
        .social-share {
          margin: 2rem 0;
        }

        .social-share h3 {
          margin-bottom: 1rem;
          font-size: 1.25rem;
        }

        .share-platforms {
          display: flex;
          gap: 0.75rem;
          flex-wrap: wrap;
        }

        .share-button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1rem;
          border: none;
          border-radius: 0.5rem;
          color: white;
          font-weight: bold;
          text-decoration: none;
          transition: all 0.2s ease;
          cursor: pointer;
        }

        .share-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .copy-button {
          background-color: #333;
        }

        .platform-icon {
          font-size: 1.2rem;
        }

        @media (max-width: 768px) {
          .share-button {
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
          }

          .platform-name {
            display: none;
          }
        }
      `}</style>
    </div>
  );
};

export default SocialShare;