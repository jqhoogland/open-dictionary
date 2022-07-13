import Head from "next/head";
import React from "react";
import BasicLayout from "./BasicLayout";
import FaviconEmoji from "./FaviconEmoji";
import NavBar from "./NavBar";

const DocsLayout: React.FC<{ title?: string; children: React.ReactNode }> = ({
    title = "OpenDictionary",
    children,
}) => (
    <BasicLayout title={title}>
        <NavBar />
        <main className="px-8 mx-auto max-w-screen-md py-16 min-h-[80vh] !prose">
            {children}
        </main>
    </BasicLayout >
);

export default DocsLayout;
