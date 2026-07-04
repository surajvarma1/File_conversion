import Link from "next/link";
import { notFound } from "next/navigation";
import ToolForm from "@/components/tool/ToolForm";
import AdBanner from "@/components/ui/AdBanner";
import { toolDefinitions } from "@/constants/tools";

interface ToolPageProps {
  params: Promise<{ tool: string }>;
}

export const dynamic = "force-dynamic";

export async function generateMetadata({ params }: ToolPageProps) {
  const resolvedParams = await params;
  const tool = toolDefinitions[resolvedParams.tool];
  
  return {
    title: tool ? `${tool.label} | File Conversion Platform` : "Tool | File Conversion Platform",
    description: tool ? tool.description : "Convert files quickly and securely.",
  };
}

export default async function ToolPage({ params }: ToolPageProps) {
  const resolvedParams = await params;
  const tool = toolDefinitions[resolvedParams.tool];

  if (!tool) { 
    notFound(); 
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-white">
      <div className="mx-auto max-w-6xl">
        
        {/* Top Header */}
        <div className="mb-8 flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900 p-8 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">{tool.category}</p>
            <h1 className="mt-4 text-4xl font-semibold">{tool.label}</h1>
          </div>
          <Link href="/" className="rounded-full bg-slate-800 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-700">
            Back to Home
          </Link>
        </div>

        {/* Top Banner AdSlot */}
        <AdBanner dataAdSlot="1234567890" /> 

        <div className="grid gap-8 lg:grid-cols-[1.4fr_minmax(280px,1fr)] mt-8">
          {/* Main Form Area */}
          <div>
            <ToolForm tool={resolvedParams.tool} />
          </div>

          {/* Sidebar */}
          <aside className="space-y-6">
            <div className="rounded-3xl border border-slate-800 bg-slate-950 p-6">
              <h3 className="text-xl font-semibold">How it works</h3>
              <ol className="mt-4 space-y-4 text-slate-300">
                <li className="flex gap-3"><span className="text-cyan-500 font-bold">1.</span> Upload your file using the drag & drop zone.</li>
                <li className="flex gap-3"><span className="text-cyan-500 font-bold">2.</span> Configure your desired settings.</li>
                <li className="flex gap-3"><span className="text-cyan-500 font-bold">3.</span> Click the convert button.</li>
                <li className="flex gap-3"><span className="text-green-500 font-bold">4.</span> Instantly download your new file.</li>
              </ol>
            </div>

            {/* Sidebar AdSlot */}
            <AdBanner dataAdSlot="0987654321" />
          </aside>
        </div>
      </div>
    </main>
  );
}