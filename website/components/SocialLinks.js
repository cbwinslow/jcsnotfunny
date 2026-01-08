const SocialLinks = () => {
  const socialPlatforms = [
    {
      name: 'YouTube',
      url: 'https://www.youtube.com/@JaredsNotFunny',
      icon: '📺',
      color: '#FF0000'
    },
    {
      name: 'TikTok',
      url: 'https://www.tiktok.com/@jaredsnotfunny',
      icon: '🎵',
      color: '#000000'
    },
    {
      name: 'Instagram',
      url: 'https://www.instagram.com/jaredsnotfunny',
      icon: '📸',
      color: '#E1306C'
    },
    {
      name: 'Twitter',
      url: 'https://twitter.com/jaredsnotfunny',
      icon: '🐦',
      color: '#1DA1F2'
    },
    {
      name: 'Facebook',
      url: 'https://www.facebook.com/jaredsnotfunny',
      icon: '📘',
      color: '#1877F2'
    }
  ];

  return (
    <div className="social-links">
      <h3>Follow Us</h3>
      <div className="social-platforms">
        {socialPlatforms.map((platform) => (
          <a
            key={platform.name}
            href={platform.url}
            target="_blank"
            rel="noopener noreferrer"
            className="social-link"
            style={{ backgroundColor: platform.color }}
            aria-label={`Follow us on ${platform.name}`}
          >
            <span className="platform-icon">{platform.icon}</span>
            <span className="platform-name">{platform.name}</span>
          </a>
        ))}
      </div>

      <style jsx>{`
        .social-links {
          margin: 2rem 0;
        }

        .social-links h3 {
          margin-bottom: 1rem;
          font-size: 1.25rem;
        }

        .social-platforms {
          display: flex;
          gap: 0.75rem;
          flex-wrap: wrap;
        }

        .social-link {
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

        .social-link:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        .platform-icon {
          font-size: 1.2rem;
        }

        @media (max-width: 768px) {
          .social-link {
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

export default SocialLinks;