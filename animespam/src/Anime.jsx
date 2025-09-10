import { animeContent } from "./constants";
import Heading from "./components/Heading";
import Section from "./components/Section";
import Arrow from "./assets/svg/Arrow";
import { GradientLight } from "./components/design/Benefits";
import Header from "./components/Header";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";

const Anime = () => {
  const { name } = useParams();
  const [data, setData] = useState([]);
  const navigate = useNavigate();
  useEffect(() => {
    if (!animeContent[name.toUpperCase()]) {
      navigate("/");
    }

    setData(animeContent[name.toUpperCase()]);
  }, [name]);

  const handleAnime = (url) => {
    window.open(url, "_blank");
  };

  return (
    <>
      <Header />
      <Section id="features">
        <div className="container relative z-2 mt-8">
          <Heading
            className="md:max-w-md lg:max-w-2xl"
            title="Do support me!!! You can download clips by clicking below"
          />

          <div className="flex flex-wrap gap-10 mb-10">
            {data.map((item) => (
              <div
                className="block relative p-0.5 bg-no-repeat bg-[length:100%_100%] md:max-w-[24rem]"
                style={{
                  backgroundImage: `url(${item.backgroundUrl})`,
                }}
                key={item.id}
              >
                <div className="relative z-2 flex flex-col min-h-[22rem] p-[2.4rem] pointer-events-none">
                  <h5 className="h5 mb-5">{item.title}</h5>
                  <p className="body-2 mb-6 text-n-3">{item.text}</p>
                  <div className="flex items-center mt-auto">
                    <img
                      src={item.iconUrl}
                      width={48}
                      height={48}
                      alt={item.title}
                    />
                    <p className="ml-auto font-code text-xs font-bold text-n-1 uppercase tracking-wider">
                      Explore more
                    </p>
                    <Arrow />
                  </div>
                </div>
                <GradientLight />

                <div className="absolute inset-0.5 bg-n-8  border-2 border-white rounded-[35px] overflow-hidden">
                  <div
                    className="absolute inset-0 opacity-35 transition-opacity hover:opacity-75 cursor-pointer"
                    onClick={() => {
                      handleAnime(item.videoUrl);
                    }}
                  >
                    {item.imageUrl && (
                      <img
                        src={item.imageUrl}
                        width={380}
                        height={362}
                        alt={item.title}
                        className="w-full h-full object-cover"
                      />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Section>
    </>
  );
};

export default Anime;
