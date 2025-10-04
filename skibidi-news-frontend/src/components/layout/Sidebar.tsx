import { Newspaper, Laugh, Brain, Volume2 } from "lucide-react";

const items = [
  { icon: <Newspaper />, label: "News Feed" },
  { icon: <Laugh />, label: "Comedic View" },
  { icon: <Brain />, label: "Prompt Lab" },
  { icon: <Volume2 />, label: "Audio Studio" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white h-screen shadow-md p-4 flex flex-col">
      <h1 className="text-2xl font-bold mb-6">🧠 Skibidi Dashboard</h1>
      {items.map((it, i) => (
        <div
          key={i}
          className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-100 cursor-pointer transition"
        >
          {it.icon}
          <span>{it.label}</span>
        </div>
      ))}
    </aside>
  );
}
