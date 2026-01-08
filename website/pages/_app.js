import '../styles/globals.css';
import Head from 'next/head';
import Analytics from '../components/Analytics';

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        {/* Google Analytics 4 */}
        <script async src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_TRACKING_ID}`}></script>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${process.env.NEXT_PUBLIC_GA_TRACKING_ID}', {
                anonymize_ip: true,
                cookie_expires: 0
              });
            `,
          }}
        />
         
        {/* Preconnect for performance */}
        <link rel="preconnect" href="https://www.googletagmanager.com" />
        <link rel="preconnect" href="https://www.google-analytics.com" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
         
        {/* DNS prefetch for external domains */}
        <link rel="dns-prefetch" href="//fonts.googleapis.com" />
        <link rel="dns-prefetch" href="//www.googletagmanager.com" />
        <link rel="dns-prefetch" href="//www.google-analytics.com" />
        <link rel="dns-prefetch" href="//www.youtube.com" />
        <link rel="dns-prefetch" href="//www.tiktok.com" />
      </Head>
      <Analytics />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
