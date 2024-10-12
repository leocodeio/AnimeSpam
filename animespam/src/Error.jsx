import React from "react";
import { smallSphere, stars } from "./assets";
import { LeftLine, RightLine } from "./components/design/Pricing";
import Heading from "./components/Heading";
import Section from "./components/Section";
import { Link } from "react-router-dom";
import { FaHome } from "react-icons/fa";

const Error = () => {
  return (
    <Section className="overflow-hidden">
      <div className="container relative items-center flex flex-col z-2 mt-10">
        <Link
          to="/"
          className="button hidden text-n-1/60 transition-colors hover:text-n-1 lg:block"
        >
          <div className="h-20 flex gap-4 items-center">
            <p>Home</p>
            <FaHome />
          </div >
        </Link>
        <div className="hidden relative justify-center mb-[6.5rem] lg:flex">
          <img
            src={smallSphere}
            className="relative z-1"
            width={255}
            height={255}
            alt="Sphere"
          />
          <div className="absolute top-1/2 left-1/2 w-[60rem] -translate-x-1/2 -translate-y-1/2 pointer-events-none">
            <img
              src={stars}
              className="w-full"
              width={950}
              height={400}
              alt="Stars"
            />
          </div>
        </div>

        <Heading
          tag="Your path is messed up go back"
          title="Please, retrun to AnimeSpam"
        />
        <div className="relative">
          <LeftLine />
          <RightLine />
        </div>
      </div>
    </Section>
  );
};

export default Error;
