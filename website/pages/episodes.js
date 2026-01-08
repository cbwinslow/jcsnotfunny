import { useState, useEffect } from 'react';
import SEO from '../components/SEO';
import EpisodeTemplate from '../components/EpisodeTemplate';

const EpisodesPage = ({ episodes = [] }) => {
  const [selectedEpisode, setSelectedEpisode] = useState(null);
  const [filterTag, setFilterTag] = useState('');
  const [sortBy, setSortBy] = useState('newest');

  // Filter and sort episodes
  const filteredEpisodes = episodes
    .filter(episode => 
      filterTag === '' || episode.tags.includes(filterTag)
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'newest':
          return new Date(b.publishDate) - new Date(a.publishDate);
        case 'oldest':
          return new Date(a.publishDate) - new Date(b.publishDate);
        case 'title':
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });

  // Get all unique tags
  const allTags = [...new Set(
    episodes.flatMap(episode => episode.tags)
  )].sort();

  return (
    <div className="episodes-page">
      <SEO
        title="Episodes | Jared's Not Funny Podcast"
        description="Browse all episodes of Jared's Not Funny podcast - comedy, technology, culture, and entertaining conversations with guests from around the world."
        canonical="/episodes"
        type="website"
        keywords={['podcast episodes', 'comedy episodes', 'tech podcast', 'jared christianson']}
      />

      {/* Episodes Schema Markup */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "Jared's Not Funny - All Episodes",
            "description": "Complete archive of Jared's Not Funny podcast episodes",
            "url": "https://jcsnotfunny.com/episodes",
            "mainEntity": {
              "@type": "ItemList",
              "itemListElement": episodes.map((episode, index) => ({
                "@type": "ListItem",
                "position": index + 1,
                "item": {
                  "@type": "PodcastEpisode",
                  "name": episode.title,
                  "url": `https://jcsnotfunny.com/episodes/${episode.slug}`,
                  "datePublished": episode.publishDate,
                  "image": episode.coverImage
                }
              }))
            }
          })
        }}
      />

      <div className="episodes-container">
        <header className="episodes-header">
          <h1>All Episodes</h1>
          <p>Complete archive of Jared's Not Funny podcast episodes</p>
        </header>

        {/* Filters and Sorting */}
        <section className="episodes-filters">
          <div className="filter-group">
            <label htmlFor="tag-filter">Filter by tag:</label>
            <select
              id="tag-filter"
              value={filterTag}
              onChange={(e) => setFilterTag(e.target.value)}
            >
              <option value="">All Episodes</option>
              {allTags.map(tag => (
                <option key={tag} value={tag}>{tag}</option>
              ))}
            </select>
          </div>

          <div className="sort-group">
            <label htmlFor="sort-by">Sort by:</label>
            <select
              id="sort-by"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="title">Alphabetical</option>
            </select>
          </div>
        </section>

        {/* Episodes Grid */}
        <main className="episodes-grid">
          {filteredEpisodes.map((episode) => (
            <article key={episode.slug} className="episode-card">
              <a href={`/episodes/${episode.slug}`}>
                {episode.coverImage && (
                  <div className="episode-image-container">
                    <img
                      src={episode.coverImage}
                      alt={episode.title}
                      className="episode-cover"
                      loading="lazy"
                    />
                    <div className="play-overlay">
                      <button className="play-button" aria-label="Play episode">
                        ▶
                      </button>
                    </div>
                  </div>
                )}
                
                <div className="episode-info">
                  <header className="episode-card-header">
                    <h2>{episode.title}</h2>
                    <div className="episode-meta">
                      <time dateTime={episode.publishDate}>
                        {new Date(episode.publishDate).toLocaleDateString()}
                      </time>
                      {episode.duration && (
                        <span className="duration">{episode.duration}</span>
                      )}
                    </div>
                  </header>
                  
                  <p className="episode-description">
                    {episode.description.substring(0, 150)}
                    {episode.description.length > 150 && '...'}
                  </p>
                  
                  <div className="episode-footer">
                    <div className="tags">
                      {episode.tags.slice(0, 3).map(tag => (
                        <span key={tag} className="tag">{tag}</span>
                      ))}
                      {episode.tags.length > 3 && (
                        <span className="tag">+{episode.tags.length - 3}</span>
                      )}
                    </div>
                    
                    {episode.guests && episode.guests.length > 0 && (
                      <div className="guests-preview">
                        with {episode.guests.map(g => g.name).join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              </a>
            </article>
          ))}
        </main>

        {/* Empty State */}
        {filteredEpisodes.length === 0 && (
          <div className="empty-state">
            <h2>No episodes found</h2>
            <p>Try adjusting your filters or check back later for new episodes.</p>
          </div>
        )}

        {/* Search Box */}
        <section className="episodes-search">
          <div className="search-container">
            <input
              type="search"
              placeholder="Search episodes..."
              aria-label="Search episodes"
              onChange={(e) => {
                // Implement search functionality
                const searchTerm = e.target.value.toLowerCase();
                // This would typically filter episodes on the server
              }}
            />
            <button type="submit" aria-label="Search">
              🔍
            </button>
          </div>
        </section>

        {/* Newsletter Signup */}
        <section className="episodes-newsletter">
          <div className="newsletter-content">
            <h2>Never Miss an Episode</h2>
            <p>Get new episodes delivered to your inbox every week.</p>
            <form className="newsletter-form" onSubmit={(e) => e.preventDefault()}>
              <input
                type="email"
                placeholder="Enter your email"
                required
                aria-label="Email address"
              />
              <button type="submit">Subscribe</button>
            </form>
          </div>
        </section>

        {/* RSS and Podcast Links */}
        <section className="podcast-links">
          <h2>Subscribe Everywhere</h2>
          <div className="podcast-platforms">
            <a href="/feed.xml" className="platform-link">
              <span className="platform-icon">📡</span>
              <span>RSS Feed</span>
            </a>
            <a href="https://podcasts.apple.com" className="platform-link">
              <span className="platform-icon">🍎</span>
              <span>Apple Podcasts</span>
            </a>
            <a href="https://open.spotify.com" className="platform-link">
              <span className="platform-icon">🎵</span>
              <span>Spotify</span>
            </a>
            <a href="https://podcastaddict.com" className="platform-link">
              <span className="platform-icon">🎙️</span>
              <span>Podcast Addict</span>
            </a>
          </div>
        </section>
      </div>

      <style jsx>{`
        .episodes-page {
          min-height: 100vh;
          background: #fff;
        }

        .episodes-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2rem 1rem;
        }

        .episodes-header {
          text-align: center;
          margin-bottom: 3rem;
        }

        .episodes-header h1 {
          font-size: 3rem;
          margin-bottom: 1rem;
        }

        .episodes-header p {
          font-size: 1.2rem;
          color: #666;
        }

        .episodes-filters {
          display: flex;
          justify-content: center;
          gap: 2rem;
          margin-bottom: 3rem;
          flex-wrap: wrap;
        }

        .filter-group, .sort-group {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .filter-group select, .sort-group select {
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 0.5rem;
          background: white;
          font-size: 1rem;
        }

        .episodes-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
          gap: 2rem;
          margin-bottom: 4rem;
        }

        .episode-card {
          border: 1px solid #ddd;
          border-radius: 1rem;
          overflow: hidden;
          transition: all 0.3s ease;
          background: white;
        }

        .episode-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }

        .episode-card a {
          text-decoration: none;
          color: inherit;
          display: block;
        }

        .episode-image-container {
          position: relative;
          aspect-ratio: 1;
          overflow: hidden;
        }

        .episode-cover {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.3s ease;
        }

        .episode-card:hover .episode-cover {
          transform: scale(1.05);
        }

        .play-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          opacity: 0;
          transition: opacity 0.3s ease;
        }

        .episode-card:hover .play-overlay {
          opacity: 1;
        }

        .play-button {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background: rgba(255,255,255,0.9);
          border: none;
          font-size: 1.5rem;
          cursor: pointer;
          transition: background 0.3s ease;
        }

        .play-button:hover {
          background: white;
        }

        .episode-info {
          padding: 1.5rem;
        }

        .episode-card-header h2 {
          font-size: 1.25rem;
          margin: 0 0 0.5rem 0;
          line-height: 1.3;
        }

        .episode-meta {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1rem;
          font-size: 0.875rem;
          color: #666;
        }

        .duration {
          background: #f0f0f0;
          padding: 0.25rem 0.5rem;
          border-radius: 1rem;
          font-size: 0.75rem;
        }

        .episode-description {
          margin: 0 0 1rem 0;
          color: #333;
          line-height: 1.5;
        }

        .episode-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
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
          font-size: 0.75rem;
          color: #666;
        }

        .guests-preview {
          font-size: 0.875rem;
          color: #666;
          font-style: italic;
        }

        .empty-state {
          grid-column: 1 / -1;
          text-align: center;
          padding: 4rem 2rem;
        }

        .episodes-search {
          margin-bottom: 4rem;
        }

        .search-container {
          display: flex;
          max-width: 500px;
          margin: 0 auto;
          border: 2px solid #ddd;
          border-radius: 2rem;
          overflow: hidden;
        }

        .search-container input {
          flex: 1;
          padding: 1rem;
          border: none;
          font-size: 1rem;
        }

        .search-container button {
          padding: 1rem 1.5rem;
          background: #000;
          color: white;
          border: none;
          font-size: 1rem;
          cursor: pointer;
        }

        .episodes-newsletter {
          background: #f8f8f8;
          padding: 3rem;
          border-radius: 1rem;
          text-align: center;
          margin-bottom: 4rem;
        }

        .newsletter-content h2 {
          font-size: 2rem;
          margin-bottom: 1rem;
        }

        .newsletter-form {
          display: flex;
          max-width: 400px;
          margin: 2rem auto 0;
          border-radius: 2rem;
          overflow: hidden;
        }

        .newsletter-form input {
          flex: 1;
          padding: 1rem;
          border: none;
        }

        .newsletter-form button {
          padding: 1rem 2rem;
          background: #000;
          color: white;
          border: none;
          cursor: pointer;
        }

        .podcast-links {
          text-align: center;
          margin-bottom: 4rem;
        }

        .podcast-platforms {
          display: flex;
          justify-content: center;
          gap: 2rem;
          flex-wrap: wrap;
          margin-top: 2rem;
        }

        .platform-link {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-decoration: none;
          color: #333;
          transition: transform 0.2s ease;
        }

        .platform-link:hover {
          transform: translateY(-2px);
        }

        .platform-icon {
          font-size: 2rem;
          margin-bottom: 0.5rem;
        }

        @media (max-width: 768px) {
          .episodes-header h1 {
            font-size: 2rem;
          }

          .episodes-filters {
            flex-direction: column;
            align-items: center;
          }

          .episodes-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
          }

          .episode-footer {
            flex-direction: column;
            align-items: flex-start;
          }

          .podcast-platforms {
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
          }
        }
      `}</style>
    </div>
  );
};

export default EpisodesPage;