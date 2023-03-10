import React from "react";
import Link from "next/link";

import JobItem from "./job/JobItem";

const Home = () => {
  return (
    <div className="container container-fluid">
      <div className="row">
        <div className="col-xl-3 col-lg-4">{/* <Filters /> */}</div>

        <div className="col-xl-9 col-lg-8 content-left-offset">
          <div className="my-5">
            <h4 className="page-title">Job List </h4>
            <Link href="/stats">
              <button className="btn btn-secondary float-right stats_btn">
                Get Topic stats
              </button>
            </Link>
            <div className="d-block">
              <Link href="/search">Search</Link>
            </div>
          </div>
          <JobItem />
          <JobItem />
        </div>
      </div>
    </div>
  );
};

export default Home;