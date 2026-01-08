import fs from 'fs';
import path from 'path';

const SITE_URL = 'https://jcsnotfunny.com';

const generateRSSFeed = (episodes = []) => {
  const header = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Jared's Not Funny</title>
    <description>A comedy podcast exploring technology, culture, and everything in between. Join Jared Christianson for weekly episodes featuring tech insights, cultural commentary, and hilarious conversations.</description>
    <link>${SITE_URL}</link>
    <language>en-us</language>
    <copyright>© 2025 Jared Christianson</copyright>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <pubDate>${episodes[0]?.publishDate || new Date().toUTCString()}</pubDate>
    <generator>JCS Not Funny RSS Generator</generator>
    <docs>https://www.rssboard.org/rss-specification</docs>
    <itunes:author>Jared Christianson</itunes:author>
    <itunes:subtitle>Comedy meets Technology</itunes:subtitle>
    <itunes:summary>A comedy podcast exploring technology, culture, and everything in between.</itunes:summary>
    <itunes:owner>
      <itunes:name>Jared Christianson</itunes:name>
      <itunes:email>jared@jcsnotfunny.com</itunes:email>
    </itunes:owner>
    <itunes:explicit>no</itunes:explicit>
    <itunes:image href="${SITE_URL}/images/podcast-cover.jpg" />
    <itunes:category text="Comedy">
      <itunes:category text="Technology" />
    </itunes:category>
    <image>
      <url>${SITE_URL}/images/podcast-cover.jpg</url>
      <title>Jared's Not Funny</title>
      <link>${SITE_URL}</link>
      <width>1400</width>
      <height>1400</height>
    </image>`;

  const items = episodes.map((episode) => {
    const episodeUrl = `${SITE_URL}/episodes/${episode.slug}`;
    const audioUrl = episode.audioUrl || `${SITE_URL}/audio/${episode.slug}.mp3`;
    const description = episode.description || '';
    
    return `
    <item>
      <title>${episode.title}</title>
      <link>${episodeUrl}</link>
      <guid isPermaLink="true">${episodeUrl}</guid>
      <pubDate>${new Date(episode.publishDate).toUTCString()}</pubDate>
      <description><![CDATA[${description}]]></description>
      <content:encoded><![CDATA[
        <p><strong>Show Notes:</strong></p>
        ${description}
        
        <p><strong>Listen:</strong> <a href="${audioUrl}">Download Episode</a></p>
        
        ${episode.youtubeUrl ? `<p><strong>Watch:</strong> <a href="${episode.youtubeUrl}">YouTube Video</a></p>` : ''}
        
        ${episode.guests && episode.guests.length > 0 ? 
          `<p><strong>Guests:</strong> ${episode.guests.map(g => g.name).join(', ')}</p>` : ''}
      ]]></content:encoded>
      
      <enclosure 
        url="${audioUrl}" 
        type="audio/mpeg" 
        length="${episode.fileSize || '0'}"
      />
      
      <itunes:author>Jared Christianson${episode.guests && episode.guests.length > 0 ? 
        ` with ${episode.guests.map(g => g.name).join(' & ')}` : ''}</itunes:author>
      
      <itunes:subtitle>${episode.title}</itunes:subtitle>
      <itunes:summary>${description.substring(0, 255)}...</itunes:summary>
      <itunes:explicit>no</itunes:explicit>
      <itunes:duration>${episode.duration || '00:00'}</itunes:duration>
      
      ${episode.coverImage ? 
        `<itunes:image href="${SITE_URL}${episode.coverImage}" />` : ''}
      
      ${episode.tags && episode.tags.length > 0 ? 
        episode.tags.map(tag => `<category>${tag}</category>`).join('') : ''}
    </item>`;
  }).join('');

  const footer = `
  </channel>
</rss>`;

  const rss = header + items + footer;
  
  // Write to public directory
  const rssPath = path.join(process.cwd(), 'public', 'feed.xml');
  fs.writeFileSync(rssPath, rss, 'utf8');
  
  console.log('RSS feed generated at:', rssPath);
  return rss;
};

// Sample episode data - replace with your actual episodes
const sampleEpisodes = [
  {
    slug: 'episode-125-seo-strategies',
    title: 'Episode 125: SEO Strategies for Podcasts in 2025',
    description: 'Deep dive into podcast SEO best practices, including GA4 setup, schema markup, and technical SEO requirements.',
    publishDate: '2025-01-08T10:00:00Z',
    duration: '00:45:30',
    coverImage: '/images/episodes/ep125-cover.jpg',
    audioUrl: 'https://jcsnotfunny.com/audio/episode-125.mp3',
    youtubeUrl: 'https://www.youtube.com/watch?v=example',
    tags: ['SEO', 'Marketing', 'Technology', 'Podcasting'],
    guests: [
      { name: 'SEO Expert', socials: {} }
    ],
    fileSize: '43543244'
  }
];

// Generate the feed
generateRSSFeed(sampleEpisodes);

export { generateRSSFeed };