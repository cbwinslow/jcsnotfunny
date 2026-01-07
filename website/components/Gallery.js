const Gallery = () => {
  const images = [
    { src: '/images/image1.jpg', alt: 'Image 1' },
    { src: '/images/image2.jpg', alt: 'Image 2' },
    { src: '/images/image3.jpg', alt: 'Image 3' },
  ];

  return (
    <section>
      <h2>Gallery</h2>
      <div>
        {images.map((image, index) => (
          <img key={index} src={image.src} alt={image.alt} />
        ))}
      </div>
    </section>
  );
};

export default Gallery;
