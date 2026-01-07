import Head from 'next/head';
import Layout from '../components/Layout';
import Hero from '../components/Hero';
import TourDates from '../components/TourDates';
import Gallery from '../components/Gallery';
import Contact from '../components/Contact';

const Home = () => {
  return (
    <div>
      <Head>
        <title>JCS Not Funny | Home</title>
        <meta name="description" content="Welcome to JCS Not Funny" />
      </Head>
      <Layout>
        <Hero />
        <TourDates />
        <Gallery />
        <Contact />
      </Layout>
    </div>
  );
};

export default Home;
