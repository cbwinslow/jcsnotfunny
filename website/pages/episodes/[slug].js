import { getEpisodeBySlug, getAllEpisodes } from '../../lib/episodes';
import EpisodeTemplate from '../../components/EpisodeTemplate';

export default function Episode({ episode }) {
  return <EpisodeTemplate episode={episode} />;
}

export async function getStaticPaths() {
  const episodes = await getAllEpisodes();
  const paths = episodes.map((episode) => ({
    params: { slug: episode.slug },
  }));

  return {
    paths,
    fallback: false,
  };
}

export async function getStaticProps({ params }) {
  const episode = await getEpisodeBySlug(params.slug);
  
  if (!episode) {
    return { notFound: true };
  }

  return {
    props: { episode },
  };
}
