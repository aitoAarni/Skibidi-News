import Sidebar from "../components/layout/Sidebar";
import Header from "../components/layout/Header";
import NewsPanel from "../components/NewsPanel";
import HumorPanel from "../components/HumorPanel";
import AudioPanel from "../components/AudioPanel";
import { useState } from "react";

export default function Dashboard() {
  const [summary, setSummary] = useState("");
  const [humor, setHumor] = useState("");

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 flex flex-col h-screen">
        <Header />
        <div className="p-6 space-y-6 overflow-y-scroll">
          <NewsPanel />
          <HumorPanel summary={summary} />
          <AudioPanel text={humor} />
        </div>
      </main>
    </div>
  );
}
