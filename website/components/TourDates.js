const TourDates = () => {
  const tourDates = [
    { date: '2026-02-15', location: 'New York, NY', venue: 'Madison Square Garden' },
    { date: '2026-02-20', location: 'Los Angeles, CA', venue: 'Staples Center' },
    { date: '2026-02-25', location: 'Chicago, IL', venue: 'United Center' },
  ];

  return (
    <section>
      <h2>Tour Dates</h2>
      <ul>
        {tourDates.map((tour, index) => (
          <li key={index}>
            <h3>{tour.date}</h3>
            <p>{tour.location}</p>
            <p>{tour.venue}</p>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default TourDates;
