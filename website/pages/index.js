import Head from 'next/head';
import Layout from '../components/Layout';
import Hero from '../components/Hero';
import TourDates from '../components/TourDates';
import Gallery from '../components/Gallery';
import Contact from '../components/Contact';
import NewsletterSignup from '../components/NewsletterSignup';

const Home = () => {
  return (
    <div>
      <Head>
        {/* Primary SEO Meta Tags */}
        <title>Jared's Not Funny - Comedy Podcast | Tech, Culture & Entertainment</title>
        <meta name="description" content="Jared's Not Funny is a comedy podcast exploring technology, culture, and everything in between. Join Jared Christianson for weekly episodes featuring tech insights, cultural commentary, and hilarious conversations." />
        <meta name="keywords" content="comedy podcast, technology podcast, jared christianson, tech comedy, culture podcast, entertainment, weekly podcast" />
        <meta name="author" content="Jared Christianson" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://jcsnotfunny.com/" />

        {/* Open Graph Meta Tags for Social Media */}
        <meta property="og:type" content="website" />
        <meta property="og:title" content="Jared's Not Funny - Comedy Podcast" />
        <meta property="og:description" content="A comedy podcast exploring technology, culture, and everything in between. Weekly episodes featuring tech insights and hilarious conversations." />
        <meta property="og:url" content="https://jcsnotfunny.com/" />
        <meta property="og:image" content="https://jcsnotfunny.com/images/og-image.jpg" />
        <meta property="og:image:width" content="1200" />
        <meta property="og:image:height" content="630" />
        <meta property="og:site_name" content="Jared's Not Funny" />
        <meta property="og:locale" content="en_US" />

        {/* Twitter Card Meta Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Jared's Not Funny - Comedy Podcast" />
        <meta name="twitter:description" content="A comedy podcast exploring technology, culture, and everything in between." />
        <meta name="twitter:image" content="https://jcsnotfunny.com/images/twitter-card.jpg" />
        <meta name="twitter:site" content="@jaredsnotfunny" />

        {/* Additional SEO Meta Tags */}
        <meta name="theme-color" content="#000000" />
        <meta name="msapplication-TileColor" content="#000000" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />

        {/* Podcast Schema Markup for SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "PodcastSeries",
              "name": "Jared's Not Funny",
              "description": "A comedy podcast exploring technology, culture, and everything in between. Join Jared Christianson for weekly episodes featuring tech insights, cultural commentary, and hilarious conversations.",
              "url": "https://jcsnotfunny.com",
              "image": "https://jcsnotfunny.com/images/podcast-cover.jpg",
              "author": {
                "@type": "Person",
                "name": "Jared Christianson"
              },
              "inLanguage": "en",
              "genre": ["Comedy", "Technology", "Culture"],
              "keywords": "comedy podcast, technology podcast, tech comedy, culture podcast"
            }),
          }}
        />
      </Head>
      <Layout>
        <Hero />
        <TourDates />
        <Gallery />
        <NewsletterSignup />
        <Contact />
      </Layout>
    </div>
  );
};

export default Home;
