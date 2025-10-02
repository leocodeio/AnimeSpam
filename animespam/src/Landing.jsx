import ButtonGradient from "./assets/svg/ButtonGradient";
import Benefits from "./components/Benefits";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Pricing from "./components/Pricing";
import Slider from "./components/Slider";
import { Helmet } from "react-helmet-async";

const Landing = () => {
  return (
    <>
      <Helmet>
        <title>AnimeSpam - Premium Anime Clips & Edits</title>
        <meta name="description" content="Discover high-quality anime clips and edits from popular series like JJK, Naruto, One Piece, and Solo Leveling. Download premium anime content." />
        <meta name="keywords" content="anime clips, anime edits, jujutsu kaisen, naruto, one piece, solo leveling, anime videos" />
        <meta property="og:title" content="AnimeSpam - Premium Anime Clips & Edits" />
        <meta property="og:description" content="Discover high-quality anime clips and edits from popular series like JJK, Naruto, One Piece, and Solo Leveling." />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://animespam.com/" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="AnimeSpam - Premium Anime Clips & Edits" />
        <meta name="twitter:description" content="Discover high-quality anime clips and edits from popular series." />
        <link rel="canonical" href="https://animespam.com/" />
      </Helmet>
      <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden">
        <Header />
        <Slider />
        <Hero />
        {/* <Benefits /> */}
        {/* <Collaboration /> */}
        {/* <Services /> */}
        <Pricing />
        {/* <Roadmap /> */}
        <Footer />
      </div>

      <ButtonGradient />
    </>
  );
};

export default Landing;
