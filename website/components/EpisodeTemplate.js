import SEO from '../components/SEO';
import SocialShare from '../components/SocialShare';

const EpisodeTemplate = ({ 
  episode,
  transcript,
  relatedEpisodes = []
}) => {
  const {
    title,
    description,
    slug,
    publishDate,
    updatedAt,
    coverImage,
    audioUrl,
    youtubeUrl,
    duration,
    guests,
    tags,
    chapters = []
  } = episode;

  return (
    <div className="episode-container">
      <SEO
        title={`${title} | Jared's Not Funny Podcast`}
        description={description}
        canonical={`/episodes/${slug}`}
        image={coverImage}
        type="article"
        keywords={tags}
        publishDate={publishDate}
        modifiedDate={updatedAt}
      />

      {/* Episode Schema Markup */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "PodcastEpisode",
            "name": title,
            "description": description,
            "url": `https://jcsnotfunny.com/episodes/${slug}`,
            "datePublished": publishDate,
            "dateModified": updatedAt,
            "timeRequired": `PT${duration}`,
            "episodeNumber": episode.number,
            "partOfSeries": {
              "@type": "PodcastSeries",
              "name": "Jared's Not Funny",
              "url": "https://jcsnotfunny.com"
            },
            "associatedMedia": {
              "@type": "MediaObject",
              "contentUrl": audioUrl,
              "encodingFormat": "audio/mpeg",
              "duration": `PT${duration}`
            },
            "transcript": transcript ? `https://jcsnotfunny.com/episodes/${slug}/transcript` : null,
            "author": {
              "@type": "Person",
              "name": "Jared Christianson"
            },
            "actor": guests?.map(guest => ({
              "@type": "Person",
              "name": guest.name,
              "sameAs": guest.socials || []
            })) || []
          })
        }}
      />

      <article className="episode-content">
        <header className="episode-header">
          <h1>{title}</h1>
          <div className="episode-meta">
            <time dateTime={publishDate}>
              {new Date(publishDate).toLocaleDateString()}
            </time>
            <span className="duration">{duration}</span>
            <div className="tags">
              {tags.map(tag => (
                <span key={tag} className="tag">{tag}</span>
              ))}
            </div>
          </div>
        </header>

        {/* Audio Player */}
        <section className="audio-player">
          <audio controls preload="metadata">
            <source src={audioUrl} type="audio/mpeg" />
            <p>Your browser doesn't support HTML5 audio.</p>
          </audio>
        </section>

        {/* YouTube Embed */}
        {youtubeUrl && (
          <section className="video-embed">
            <iframe
              src={`https://www.youtube.com/embed/${youtubeUrl.split('v=')[1]}`}
              title={title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="youtube-player"
            />
          </section>
        )}

        {/* Episode Description */}
        <section className="episode-description">
          <h2>About This Episode</h2>
          <div dangerouslySetInnerHTML={{ __html: description }} />
        </section>

        {/* Chapters/Timestamps */}
        {chapters.length > 0 && (
          <section className="episode-chapters">
            <h2>Chapters</h2>
            <nav className="chapter-nav">
              <ol>
                {chapters.map((chapter, index) => (
                  <li key={index}>
                    <a href={`#t=${chapter.timestamp}`}>
                      <span className="timestamp">{chapter.timestamp}</span>
                      <span className="chapter-title">{chapter.title}</span>
                    </a>
                  </li>
                ))}
              </ol>
            </nav>
          </section>
        )}

        {/* Guests */}
        {guests && guests.length > 0 && (
          <section className="episode-guests">
            <h2>Guests</h2>
            <div className="guests-list">
              {guests.map((guest, index) => (
                <div key={index} className="guest-card">
                  {guest.image && (
                    <img
                      src={guest.image}
                      alt={guest.name}
                      className="guest-image"
                    />
                  )}
                  <div className="guest-info">
                    <h3>{guest.name}</h3>
                    {guest.bio && <p>{guest.bio}</p>}
                    {guest.socials && (
                      <div className="guest-socials">
                        {Object.entries(guest.socials).map(([platform, url]) => (
                          <a
                            key={platform}
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`social-link ${platform}`}
                          >
                            {platform}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Full Transcript */}
        {transcript && (
          <section className="episode-transcript" id="transcript">
            <h2>Full Transcript</h2>
            <div 
              className="transcript-content"
              dangerouslySetInnerHTML={{ __html: transcript }}
            />
          </section>
        )}

        {/* Related Episodes */}
        {relatedEpisodes.length > 0 && (
          <section className="related-episodes">
            <h2>Related Episodes</h2>
            <div className="episodes-grid">
              {relatedEpisodes.map((related) => (
                <article key={related.slug} className="episode-card">
                  <a href={`/episodes/${related.slug}`}>
                    {related.coverImage && (
                      <img
                        src={related.coverImage}
                        alt={related.title}
                        className="episode-thumbnail"
                      />
                    )}
                    <div className="episode-card-content">
                      <h3>{related.title}</h3>
                      <p>{related.description}</p>
                      <time>{new Date(related.publishDate).toLocaleDateString()}</time>
                    </div>
                  </a>
                </article>
              ))}
            </div>
          </section>
        )}

        {/* Social Sharing */}
        <section className="episode-share">
          <SocialShare
            title={title}
            url={`https://jcsnotfunny.com/episodes/${slug}`}
            description={description}
            image={coverImage}
          />
        </section>

        {/* Call to Action */}
        <section className="episode-cta">
          <h2>Enjoyed This Episode?</h2>
          <div className="cta-actions">
            <a href="https://podcastAddict.com" className="cta-button primary">
              Subscribe on Podcast Apps
            </a>
            <a href="https://patreon.com/jaredsnotfunny" className="cta-button secondary">
              Support on Patreon
            </a>
            <a href="/contact" className="cta-button tertiary">
              Suggest a Topic
            </a>
          </div>
        </section>
      </article>

      <style jsx>{`
        .episode-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 2rem 1rem;
        }

        .episode-header h1 {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          line-height: 1.2;
        }

        .episode-meta {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 2rem;
          flex-wrap: wrap;
        }

        .tags {
          display: flex;
          gap: 0.5rem;
          flex-wrap: wrap;
        }

        .tag {
          background: #f0f0f0;
          padding: 0.25rem 0.75rem;
          border-radius: 1rem;
          font-size: 0.875rem;
        }

        .audio-player {
          margin-bottom: 2rem;
        }

        .audio-player audio {
          width: 100%;
        }

        .video-embed {
          margin-bottom: 2rem;
          position: relative;
          padding-bottom: 56.25%;
          height: 0;
          overflow: hidden;
        }

        .youtube-player {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border: none;
        }

        .episode-chapters {
          margin-bottom: 2rem;
        }

        .chapter-nav ol {
          list-style: none;
          padding: 0;
        }

        .chapter-nav a {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.75rem;
          text-decoration: none;
          border-bottom: 1px solid #eee;
        }

        .chapter-nav a:hover {
          background: #f9f9f9;
        }

        .timestamp {
          font-family: monospace;
          color: #666;
          min-width: 80px;
        }

        .guests-list {
          display: grid;
          gap: 2rem;
          margin-top: 1rem;
        }

        .guest-card {
          display: flex;
          gap: 1rem;
          align-items: flex-start;
        }

        .guest-image {
          width: 80px;
          height: 80px;
          border-radius: 50%;
          object-fit: cover;
        }

        .guest-socials {
          display: flex;
          gap: 0.5rem;
          margin-top: 0.5rem;
        }

        .social-link {
          padding: 0.25rem 0.5rem;
          background: #eee;
          text-decoration: none;
          border-radius: 0.25rem;
          font-size: 0.875rem;
        }

        .transcript-content {
          max-height: 600px;
          overflow-y: auto;
          padding: 1rem;
          background: #f9f9f9;
          border-radius: 0.5rem;
          font-family: monospace;
          line-height: 1.6;
        }

        .episodes-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
          margin-top: 1rem;
        }

        .episode-card {
          border: 1px solid #ddd;
          border-radius: 0.5rem;
          overflow: hidden;
          transition: transform 0.2s;
        }

        .episode-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .episode-card a {
          text-decoration: none;
          color: inherit;
        }

        .episode-thumbnail {
          width: 100%;
          height: 200px;
          object-fit: cover;
        }

        .episode-card-content {
          padding: 1rem;
        }

        .episode-card h3 {
          margin: 0 0 0.5rem 0;
        }

        .episode-card p {
          margin: 0 0 1rem 0;
          color: #666;
        }

        .cta-actions {
          display: flex;
          gap: 1rem;
          flex-wrap: wrap;
          margin-top: 1rem;
        }

        .cta-button {
          padding: 0.75rem 1.5rem;
          border-radius: 0.5rem;
          text-decoration: none;
          font-weight: bold;
          transition: background-color 0.2s;
        }

        .cta-button.primary {
          background: #000;
          color: white;
        }

        .cta-button.secondary {
          background: #f0f0f0;
          color: #000;
        }

        .cta-button.tertiary {
          background: transparent;
          color: #000;
          border: 2px solid #000;
        }

        @media (max-width: 768px) {
          .episode-header h1 {
            font-size: 2rem;
          }

          .episode-meta {
            flex-direction: column;
            align-items: flex-start;
          }

          .guest-card {
            flex-direction: column;
            text-align: center;
          }

          .cta-actions {
            flex-direction: column;
          }
        }
      `}</style>
    </div>
  );
};

export default EpisodeTemplate;