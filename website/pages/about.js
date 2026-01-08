import SEO from '../components/SEO';
import Layout from '../components/Layout';

const AboutPage = () => {
  return (
    <Layout>
      <SEO
        title="About Jared's Not Funny Podcast | Comedy, Tech & Culture"
        description="Learn about Jared Christianson and the Jared's Not Funny podcast - a unique blend of comedy, technology insights, and cultural commentary from Roanoke, Virginia."
        canonical="/about"
        type="website"
        keywords={['about jared christianson', 'podcast mission', 'comedy podcast about', 'tech comedy podcast', 'roanoke podcast']}
      />

      <div className="about-container">
        <header className="about-header">
          <h1>About Jared's Not Funny</h1>
          <p className="subtitle">Where Comedy Meets Technology & Culture</p>
        </header>

        <main className="about-content">
          <section className="host-section">
            <div className="host-image">
              <img
                src="/images/jared-profile.jpg"
                alt="Jared Christianson - Podcast Host"
                width="300"
                height="300"
                loading="lazy"
              />
            </div>
            <div className="host-bio">
              <h2>Meet Jared Christianson</h2>
              <p>
                Jared Christianson is a comedian, tech enthusiast, and cultural commentator based in Roanoke, Virginia.
                With a unique blend of humor and insight, Jared explores the intersection of comedy, technology, and
                everyday life through engaging conversations with guests from various backgrounds.
              </p>
              <p>
                What started as a passion project has grown into a platform where comedians, tech experts, and
                cultural figures come together to discuss everything from stand-up comedy techniques to the latest
                tech trends - all with Jared's signature humorous perspective.
              </p>
            </div>
          </section>

          <section className="podcast-mission">
            <h2>Our Mission</h2>
            <p>
              Jared's Not Funny aims to bridge the gap between comedy and technology, creating a space where
              laughter and learning coexist. We believe that:
            </p>
            <ul className="mission-points">
              <li>🎤 Comedy can make complex topics accessible and enjoyable</li>
              <li>💻 Technology should be approachable and fun, not intimidating</li>
              <li>🌍 Culture thrives when diverse voices come together</li>
              <li>🎧 Great conversations can happen anywhere - even in Roanoke, VA!</li>
            </ul>
          </section>

          <section className="podcast-format">
            <h2>What to Expect</h2>
            <div className="format-grid">
              <div className="format-card">
                <h3>🎙️ Weekly Episodes</h3>
                <p>New episodes every week featuring comedians, tech experts, and cultural figures.</p>
              </div>
              <div className="format-card">
                <h3>🤣 Comedy Insights</h3>
                <p>Behind-the-scenes looks at stand-up comedy and the comedy industry.</p>
              </div>
              <div className="format-card">
                <h3>💻 Tech Talk</h3>
                <p>Discussions about technology trends, gadgets, and digital culture.</p>
              </div>
              <div className="format-card">
                <h3>🌍 Cultural Commentary</h3>
                <p>Thoughtful conversations about society, entertainment, and modern life.</p>
              </div>
            </div>
          </section>

          <section className="local-focus">
            <h2>Roanoke & Southwest Virginia Focus</h2>
            <p>
              While we cover topics of global interest, Jared's Not Funny has a special focus on the Roanoke Valley
              and Southwest Virginia comedy scene. We regularly feature local comedians, discuss regional events,
              and highlight the vibrant cultural community in our area.
            </p>
            <div className="local-highlights">
              <h3>Local Highlights:</h3>
              <ul>
                <li>🎤 Spotlight on Roanoke Valley comedians</li>
                <li>📍 Coverage of local comedy events and venues</li>
                <li>🌄 Discussions about life in Southwest Virginia</li>
                <li>🤝 Partnerships with local businesses and organizations</li>
              </ul>
            </div>
          </section>

          <section className="join-community">
            <h2>Join Our Community</h2>
            <p>
              Jared's Not Funny is more than just a podcast - it's a community of comedy lovers, tech enthusiasts,
              and cultural explorers. Here's how you can get involved:
            </p>
            <div className="community-actions">
              <div className="action-card">
                <h3>🎧 Listen & Subscribe</h3>
                <p>Available on all major podcast platforms.</p>
              </div>
              <div className="action-card">
                <h3>📧 Join Our Newsletter</h3>
                <p>Get episode updates and behind-the-scenes content.</p>
              </div>
              <div className="action-card">
                <h3>💬 Engage on Social</h3>
                <p>Follow us on TikTok, Instagram, and YouTube.</p>
              </div>
              <div className="action-card">
                <h3>🎤 Be a Guest</h3>
                <p>Interested in being on the show? Contact us!</p>
              </div>
            </div>
          </section>

          <section className="testimonials">
            <h2>What Listeners Say</h2>
            <div className="testimonial-grid">
              <div className="testimonial-card">
                <p className="quote">"Jared has a unique ability to make tech topics hilarious while keeping the conversation insightful."</p>
                <p className="attribution">- Tech Weekly Review</p>
              </div>
              <div className="testimonial-card">
                <p className="quote">"The perfect blend of comedy and substance - I learn something new every episode while laughing my butt off."</p>
                <p className="attribution">- Comedy Fan</p>
              </div>
              <div className="testimonial-card">
                <p className="quote">"Finally, a podcast that represents the Roanoke comedy scene with professional quality."</p>
                <p className="attribution">- Local Listener</p>
              </div>
            </div>
          </section>
        </main>

        <style jsx>{`
          .about-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
          }

          .about-header {
            text-align: center;
            margin-bottom: 3rem;
          }

          .about-header h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
          }

          .subtitle {
            font-size: 1.5rem;
            color: #666;
          }

          .host-section {
            display: flex;
            gap: 3rem;
            align-items: center;
            margin-bottom: 4rem;
            flex-wrap: wrap;
          }

          .host-image img {
            border-radius: 50%;
            object-fit: cover;
          }

          .host-bio h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
          }

          .host-bio p {
            line-height: 1.6;
            margin-bottom: 1rem;
          }

          .podcast-mission {
            margin-bottom: 3rem;
          }

          .podcast-mission h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
          }

          .mission-points {
            line-height: 1.8;
            margin-left: 1.5rem;
          }

          .mission-points li {
            margin-bottom: 0.5rem;
          }

          .format-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
          }

          .format-card {
            background: #f8f8f8;
            padding: 2rem;
            border-radius: 1rem;
            text-align: center;
          }

          .format-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
          }

          .local-focus {
            margin: 3rem 0;
            background: #f9f9f9;
            padding: 2rem;
            border-radius: 1rem;
          }

          .local-highlights {
            margin-top: 1.5rem;
          }

          .local-highlights ul {
            line-height: 1.8;
            margin-left: 1.5rem;
          }

          .join-community {
            margin: 3rem 0;
          }

          .community-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
          }

          .action-card {
            background: #f0f0f0;
            padding: 1.5rem;
            border-radius: 0.75rem;
            text-align: center;
          }

          .testimonial-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
          }

          .testimonial-card {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          }

          .quote {
            font-style: italic;
            margin-bottom: 1rem;
            color: #333;
          }

          .attribution {
            font-weight: bold;
            text-align: right;
            color: #666;
          }

          @media (max-width: 768px) {
            .about-header h1 {
              font-size: 2rem;
            }

            .host-section {
              flex-direction: column;
              text-align: center;
            }

            .host-image {
              margin-bottom: 2rem;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default AboutPage;