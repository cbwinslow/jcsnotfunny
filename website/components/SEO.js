import { NextSeo, ArticleJsonLd } from 'next-seo';

const SEO = ({ 
  title, 
  description, 
  canonical, 
  image, 
  type = 'website',
  keywords = [],
  author = 'Jared Christianson',
  publishDate,
  modifiedDate
}) => {
  const siteUrl = 'https://jcsnotfunny.com';
  const fullUrl = canonical ? `${siteUrl}${canonical}` : siteUrl;
  const imageUrl = image ? `${siteUrl}${image}` : `${siteUrl}/images/default-og.jpg`;

  return (
    <>
      <NextSeo
        title={title}
        description={description}
        canonical={fullUrl}
        openGraph={{
          type,
          url: fullUrl,
          title,
          description,
          images: [
            {
              url: imageUrl,
              width: 1200,
              height: 630,
              alt: title,
            },
          ],
          site_name: "Jared's Not Funny",
          locale: 'en_US',
        }}
        twitter={{
          handle: '@jaredsnotfunny',
          site: '@jaredsnotfunny',
          cardType: 'summary_large_image',
        }}
        additionalMetaTags={[
          {
            name: 'keywords',
            content: keywords.join(', '),
          },
          {
            name: 'author',
            content: author,
          },
          {
            name: 'theme-color',
            content: '#000000',
          },
        ]}
        additionalLinkTags={[
          {
            rel: 'icon',
            href: '/favicon.ico',
          },
          {
            rel: 'apple-touch-icon',
            href: '/apple-touch-icon.png',
            sizes: '180x180',
          },
          {
            rel: 'manifest',
            href: '/site.webmanifest',
          },
        ]}
      />
      
      {/* Breadcrumb Schema Markup */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
              {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": siteUrl
              },
              {
                "@type": "ListItem",
                "position": 2,
                "name": canonical ? canonical.replace('/', '') : "Jared's Not Funny",
                "item": fullUrl
              }
            ]
          }),
        }}
      />

      {/* Podcast Schema Markup */}
      {type === 'website' && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "PodcastSeries",
              "name": "Jared's Not Funny",
              "description": description,
              "url": siteUrl,
              "image": imageUrl,
              "author": {
                "@type": "Person",
                "name": author,
              },
              "inLanguage": "en",
              "genre": ["Comedy", "Technology", "Culture"],
              "keywords": keywords.join(', '),
              "sameAs": [
                "https://www.youtube.com/@JaredsNotFunny",
                "https://www.tiktok.com/@jaredsnotfunny",
                "https://www.instagram.com/jaredsnotfunny"
              ]
            }),
          }}
        />
      )}

      {/* Episode Schema Markup */}
      {type === 'article' && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "PodcastEpisode",
              "name": title,
              "description": description,
              "url": fullUrl,
              "datePublished": publishDate,
              "dateModified": modifiedDate,
              "image": imageUrl,
              "author": {
                "@type": "Person",
                "name": author,
              },
              "publisher": {
                "@type": "Organization",
                "name": "Jared's Not Funny",
                "logo": {
                  "@type": "ImageObject",
                  "url": `${siteUrl}/images/logo.jpg`,
                },
              },
              "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": fullUrl,
              },
            }),
          }}
        />
      )}
    </>
  );
};

export default SEO;