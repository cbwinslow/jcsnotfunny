import { useEffect } from 'react';
import { useRouter } from 'next/router';

const Analytics = () => {
  const router = useRouter();

  useEffect(() => {
    // Check if Google Analytics is already loaded
    if (window.gtag) return;

    // Load Google Analytics script
    const script = document.createElement('script');
    script.src = `https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_TRACKING_ID}`;
    script.async = true;
    document.body.appendChild(script);

    // Initialize Google Analytics
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      if (window.dataLayer) {
        window.dataLayer.push(arguments);
      }
    }
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', process.env.NEXT_PUBLIC_GA_TRACKING_ID, {
      page_path: window.location.pathname,
    });

    // Track page views on route changes
    const handleRouteChange = (url) => {
      if (window.gtag) {
        gtag('config', process.env.NEXT_PUBLIC_GA_TRACKING_ID, {
          page_path: url,
        });
      }
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router.events]);

  return null;
};

export default Analytics;