// // """Home page for the file conversion platform."""

// import Link from "next/link";

// const tools = [
//   { path: "/tools/jpg-to-png", label: "JPG → PNG" },
//   { path: "/tools/png-to-jpg", label: "PNG → JPG" },
//   { path: "/tools/webp-to-jpg", label: "WebP → JPG" },
//   { path: "/tools/jpg-to-webp", label: "JPG → WebP" },
//   { path: "/tools/image-resize", label: "Image Resize" },
//   { path: "/tools/image-compress", label: "Image Compress" },
//   { path: "/tools/images-to-pdf", label: "Images → PDF" },
//   { path: "/tools/pdf-merge", label: "PDF Merge" },
//   { path: "/tools/pdf-split", label: "PDF Split" },
//   { path: "/tools/zip-extractor", label: "ZIP Extractor" },
// ];

// export default function Home() {
//   return (
//     <main className="min-h-screen bg-slate-950 text-white">
//       <section className="mx-auto max-w-7xl px-6 py-16 text-center">
//         <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">File Conversion Platform</p>
//         <h1 className="mt-6 text-5xl font-semibold tracking-tight sm:text-6xl">
//           Convert Images, PDFs, and ZIP files in one place.
//         </h1>
//         <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-300">
//           Fast, secure, mobile-friendly and open-source file conversion tools with modern UI and API-first architecture.
//         </p>
//         <div className="mt-10 grid gap-4 sm:grid-cols-2 md:grid-cols-4">
//           {tools.map((tool) => (
//             <div key={tool.path} className="mx-auto max-w-sm">
//               <Link href={tool.path} className="block rounded-2xl border border-slate-800 bg-slate-950 p-6 text-center hover:shadow-lg">
//                 <div className="text-sm font-semibold text-cyan-300">Tool</div>
//                 <div className="mt-2 text-lg font-semibold">{tool.label}</div>
//               </Link>
//             </div>
//           ))}
//         </div>
//       </section>

//       <section className="border-t border-slate-800 bg-slate-900 py-16">
//         <div className="mx-auto max-w-6xl px-6">
//           <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
//             <article className="rounded-3xl border border-slate-800 bg-slate-950 p-8">
//               <h2 className="text-xl font-semibold">Tool Categories</h2>
//               <p className="mt-3 text-slate-400">Image conversions, PDF workflows, and ZIP extraction with secure upload and fast processing.</p>
//             </article>
//             <article className="rounded-3xl border border-slate-800 bg-slate-950 p-8">
//               <h2 className="text-xl font-semibold">Popular Tools</h2>
//               <p className="mt-3 text-slate-400">JPG/PNG/WebP conversions, PDF merge and split, image-to-PDF conversions, and ZIP extraction.</p>
//             </article>
//             <article className="rounded-3xl border border-slate-800 bg-slate-950 p-8">
//               <h2 className="text-xl font-semibold">Performance</h2>
//               <p className="mt-3 text-slate-400">Built with FastAPI, Next.js, and open-source processing libraries for low latency and scalability.</p>
//             </article>
//           </div>
//         </div>
//       </section>

//       <section className="mx-auto max-w-6xl px-6 py-16">
//         <div className="grid gap-8 lg:grid-cols-2">
//           <div>
//             <h2 className="text-3xl font-semibold">Why choose this platform?</h2>
//             <ul className="mt-6 space-y-4 text-slate-300">
//               <li>• Secure file handling and temporary cleanup.</li>
//               <li>• Open-source conversion stack with Pillow, pypdf, img2pdf, and zipfile.</li>
//               <li>• Mobile-first responsive design and SEO-friendly metadata.</li>
//             </ul>
//           </div>
//           <div className="rounded-3xl border border-slate-800 bg-slate-950 p-8">
//             <h3 className="text-xl font-semibold">Frequently asked questions</h3>
//             <div className="mt-6 space-y-4 text-slate-300">
//               <div>
//                 <p className="font-semibold">Is this platform free?</p>
//                 <p className="mt-2 text-sm">Yes, it uses open-source libraries only and does not rely on paid conversion services.</p>
//               </div>
//               <div>
//                 <p className="font-semibold">Are files stored permanently?</p>
//                 <p className="mt-2 text-sm">No, files are stored temporarily and cleaned up after processing.</p>
//               </div>
//             </div>
//           </div>
//         </div>
//       </section>
//     </main>
//   );
// }


import Link from "next/link";
import AdBanner from "@/components/ui/AdBanner";

const tools = [
  { path: "/tools/jpg-to-png", label: "JPG → PNG", icon: "🖼️" },
  { path: "/tools/png-to-jpg", label: "PNG → JPG", icon: "📸" },
  { path: "/tools/webp-to-jpg", label: "WebP → JPG", icon: "🌐" },
  { path: "/tools/jpg-to-webp", label: "JPG → WebP", icon: "⚡" },
  { path: "/tools/image-resize", label: "Image Resize", icon: "📐" },
  { path: "/tools/image-compress", label: "Image Compress", icon: "🗜️" },
  { path: "/tools/images-to-pdf", label: "Images → PDF", icon: "📑" },
  { path: "/tools/pdf-merge", label: "PDF Merge", icon: "🔗" },
  { path: "/tools/pdf-split", label: "PDF Split", icon: "✂️" },
  { path: "/tools/zip-extractor", label: "ZIP Extractor", icon: "📦" },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white relative overflow-hidden">
      {/* Background Ambient Glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-cyan-500/10 blur-[120px] rounded-full pointer-events-none" />

      <section className="relative mx-auto max-w-7xl px-6 py-20 text-center">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-400 font-semibold mb-6">
          File Conversion Platform
        </p>
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-7xl bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
          Convert Images, PDFs, <br className="hidden sm:block" /> and ZIP files instantly.
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-300">
          Fast, secure, mobile-friendly and open-source file conversion tools with a modern API-first architecture.
        </p>

        {/* Top AdSense Banner */}
        <div className="mt-12 max-w-4xl mx-auto">
          <AdBanner dataAdSlot="HOME_TOP_AD_SLOT" />
        </div>

        {/* Tools Grid (Uniform heights, glassy look) */}
        <div className="mt-16 grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 lg:gap-8">
          {tools.map((tool) => (
            <Link 
              key={tool.path} 
              href={tool.path} 
              className="group flex flex-col h-full rounded-3xl border border-slate-700/50 bg-slate-900/40 p-8 text-center backdrop-blur-xl transition-all duration-300 hover:-translate-y-2 hover:border-cyan-500/50 hover:bg-slate-800/60 hover:shadow-[0_0_30px_rgba(34,211,238,0.15)]"
            >
              <div className="mb-4 text-4xl">{tool.icon}</div>
              <div className="mt-auto">
                <div className="text-sm font-semibold tracking-wider text-cyan-400 opacity-80 group-hover:opacity-100 transition-opacity">TOOL</div>
                <div className="mt-2 text-xl font-bold text-slate-100 group-hover:text-white">{tool.label}</div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Middle AdSense Banner */}
      <section className="mx-auto max-w-5xl px-6 py-8 relative z-10">
        <AdBanner dataAdSlot="HOME_MIDDLE_AD_SLOT" />
      </section>

      {/* Info Sections (Glassy) */}
      <section className="relative border-t border-slate-800/50 bg-slate-900/20 py-20 backdrop-blur-sm">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-6 md:grid-cols-3">
            <article className="rounded-3xl border border-slate-800/60 bg-slate-950/50 p-8 backdrop-blur-md">
              <div className="h-12 w-12 rounded-full bg-cyan-500/20 flex items-center justify-center mb-6">
                <svg className="h-6 w-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              </div>
              <h2 className="text-xl font-bold">Lightning Fast</h2>
              <p className="mt-3 text-slate-400 leading-relaxed">Built with Next.js and robust Python libraries to ensure your files are processed instantly.</p>
            </article>
            
            <article className="rounded-3xl border border-slate-800/60 bg-slate-950/50 p-8 backdrop-blur-md">
              <div className="h-12 w-12 rounded-full bg-green-500/20 flex items-center justify-center mb-6">
                <svg className="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
              </div>
              <h2 className="text-xl font-bold">Highly Secure</h2>
              <p className="mt-3 text-slate-400 leading-relaxed">Your files are completely safe. They are stored temporarily during conversion and deleted immediately after.</p>
            </article>
            
            <article className="rounded-3xl border border-slate-800/60 bg-slate-950/50 p-8 backdrop-blur-md">
              <div className="h-12 w-12 rounded-full bg-purple-500/20 flex items-center justify-center mb-6">
                <svg className="h-6 w-6 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>
              </div>
              <h2 className="text-xl font-bold">Open Source Core</h2>
              <p className="mt-3 text-slate-400 leading-relaxed">Powered by reliable open-source tech like Pillow, PyPDF, and FastAPI for maximum transparency.</p>
            </article>
          </div>
        </div>
      </section>

      {/* Bottom AdSense Banner */}
      <section className="mx-auto max-w-5xl px-6 py-12 relative z-10">
        <AdBanner dataAdSlot="HOME_BOTTOM_AD_SLOT" />
      </section>
    </main>
  );
}

// import Link from "next/link";
// import { notFound } from "next/navigation"; // <-- 1. Import notFound
// import ToolForm from "@/components/tool/ToolForm";
// import AdBanner from "@/components/ui/AdBanner";
// import { toolDefinitions } from "@/constants/tools";

// // ... [interfaces and generateMetadata stay the same] ...


// export default async function ToolPage({ params }: ToolPageProps) {
//   const resolvedParams = await params;
//   const tool = toolDefinitions[resolvedParams.tool];

//   if (!tool) { 
//     notFound(); // <-- 2. Call it here. This throws an error that Next.js catches to show your 404 page.
//   } 





//   return (
//     <main className="min-h-screen bg-slate-950 px-6 py-8 text-white">
//       <div className="mx-auto max-w-6xl">
        
//         {/* Top Header */}
//         <div className="mb-8 flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900 p-8 md:flex-row md:items-center md:justify-between">
//           <div>
//             <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">{tool.description}</p>
//             <h1 className="mt-4 text-4xl font-semibold">{tool.label}</h1>
//           </div>
//           <Link href="/" className="rounded-full bg-slate-800 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-700">
//             Back to Home
//           </Link>
//         </div>

//         {/* Top Banner AdSlot */}
//         <AdBanner dataAdSlot="1234567890" /> 

//         <div className="grid gap-8 lg:grid-cols-[1.4fr_minmax(280px,1fr)] mt-8">
//           {/* Main Form Area */}
//           <div>
//             {/* 4. Pass the safely awaited param string to your form */}
//             <ToolForm tool={resolvedParams.tool} />
//           </div>

//           {/* Sidebar */}
//           <aside className="space-y-6">
//             <div className="rounded-3xl border border-slate-800 bg-slate-950 p-6">
//               <h3 className="text-xl font-semibold">How it works</h3>
//               <ol className="mt-4 space-y-4 text-slate-300">
//                 <li className="flex gap-3"><span className="text-cyan-500 font-bold">1.</span> Upload your file using the drag & drop zone.</li>
//                 <li className="flex gap-3"><span className="text-cyan-500 font-bold">2.</span> Configure your desired settings.</li>
//                 <li className="flex gap-3"><span className="text-cyan-500 font-bold">3.</span> Click the convert button.</li>
//                 <li className="flex gap-3"><span className="text-green-500 font-bold">4.</span> Instantly download your new file.</li>
//               </ol>
//             </div>

//             {/* Sidebar AdSlot */}
//             <AdBanner dataAdSlot="0987654321" />
//           </aside>
//         </div>
//       </div>
//     </main>
//   );
// }