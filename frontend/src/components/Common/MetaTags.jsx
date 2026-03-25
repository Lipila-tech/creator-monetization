const MetaTags = ({ title, description, keywords, image, type = "website" }) => {

  // Get current URL dynamically
  const currentUrl = typeof window !== 'undefined' 
    ? window.location.href 
    : '';

  return (
    <>
      <title>{title}</title>
      <meta name="description" content={description} />
      {keywords && <meta name="keywords" content={keywords} />}
      
      {/* Open Graph */}
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      {image && <meta property="og:image" content={image} />}
      <meta property="og:url" content={currentUrl} />
      <meta property="og:type" content={type} />
      
      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      {image && <meta name="twitter:image" content={image} />}
      
      {/* Canonical URL */}
      <link rel="canonical" href={currentUrl} />
    </>
  );
};

export default MetaTags;