import Head from "next/head";
import React from "react";
import FaviconEmoji from "./FaviconEmoji";

const BasicLayout: React.FC<{ title?: string; children: React.ReactNode }> = ({
  title = "OpenDictionary",
  children,
}) => (
  <>
    <Head>
      <title>{title}</title>
      <meta name="description" content="Machine Readable Wiktionary" />
      <FaviconEmoji>{"📖"}</FaviconEmoji>
    </Head>
    {children}
  </>
);

export default BasicLayout;
