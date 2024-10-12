import ButtonGradient from "./assets/svg/ButtonGradient";
import Benefits from "./components/Benefits";
import Footer from "./components/Footer";
import Header from "./components/Header";
import Hero from "./components/Hero";
import Pricing from "./components/Pricing";
import Slider from "./components/Slider";

const Landing = () => {
  return (
    <>
      <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden">
        <Header />
        <Hero />
        <Slider />
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
