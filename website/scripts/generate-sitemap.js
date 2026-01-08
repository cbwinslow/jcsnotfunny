import { DOMParser, XMLSerializer } from 'xmldom';

const SITE_URL = 'https://jcsnotfunny.com';

const generateSitemap = (pages = []) => {
  const staticPages = [
    {
      url: SITE_URL,
      changefreq: 'weekly',
      priority: 1.0,
      lastmod: new Date().toISOString(),
    },
    {
      url: `${SITE_URL}/episodes`,
      changefreq: 'daily',
      priority: 0.9,
      lastmod: new Date().toISOString(),
    },
    {
      url: `${SITE_URL}/tour`,
      changefreq: 'weekly',
      priority: 0.8,
      lastmod: new Date().toISOString(),
    },
    {
      url: `${SITE_URL}/contact`,
      changefreq: 'monthly',
      priority: 0.7,
      lastmod: new Date().toISOString(),
    },
    {
      url: `${SITE_URL}/about`,
      changefreq: 'monthly',
      priority: 0.8,
      lastmod: new Date().toISOString(),
    },
  ];

  const allPages = [...staticPages, ...pages];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
${allPages
  .map(
    (page) => `  <url>
    <loc>${page.url}</loc>
    <lastmod>${page.lastmod}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return sitemap;
};

const generateEpisodeSitemap = (episodes = []) => {
  const episodePages = episodes.map((episode) => ({
    url: `${SITE_URL}/episodes/${episode.slug}`,
    changefreq: 'monthly',
    priority: 0.9,
    lastmod: episode.updatedAt || new Date().toISOString(),
    image: episode.coverImage,
    video: episode.youtubeUrl ? {
      title: episode.title,
      description: episode.description,
      thumbnail_loc: episode.thumbnailUrl,
    } : null,
  }));

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
${episodePages
  .map((page) => {
    let xml = `  <url>
    <loc>${page.url}</loc>
    <lastmod>${page.lastmod}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>`;
    
    if (page.image) {
      xml += `
    <image:image>
      <image:loc>${page.image}</image:loc>
      <image:title>${page.url.split('/').pop()}</image:title>
    </image:image>`;
    }
    
    if (page.video) {
      xml += `
    <video:video>
      <video:title>${page.video.title}</video:title>
      <video:description>${page.video.description}</video:description>
      <video:thumbnail_loc>${page.video.thumbnail_loc}</video:thumbnail_loc>
      <video:content_loc>${page.url}</video:content_loc>
    </video:video>`;
    }
    
    xml += `
  </url>`;
    
    return xml;
  })
  .join('\n')}
</urlset>`;

  return sitemap;
};

const generateSitemapIndex = (sitemaps = []) => {
  const sitemapIndex = `<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemaps
  .map(
    (sitemap) => `  <sitemap>
    <loc>${sitemap.loc}</loc>
    <lastmod>${sitemap.lastmod}</lastmod>
  </sitemap>`
  )
  .join('\n')}
</sitemapindex>`;

  return sitemapIndex;
};

export {
  generateSitemap,
  generateEpisodeSitemap,
  generateSitemapIndex,
};