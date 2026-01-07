import Link from 'next/link';

const Header = () => {
  return (
    <header>
      <nav>
        <Link href="/">Home</Link>
        <Link href="/tour">Tour Dates</Link>
        <Link href="/gallery">Gallery</Link>
        <Link href="/contact">Contact</Link>
      </nav>
    </header>
  );
};

export default Header;
