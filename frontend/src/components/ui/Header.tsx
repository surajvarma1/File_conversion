

import Link from "next/link";
import Image from "next/image";

// 1. Define the navigation structure for easy maintenance
const navMenus = [
  {
    title: "Converters",
    items: [
      { name: "JPG → PNG", path: "/tools/jpg-to-png" },
      { name: "PNG → JPG", path: "/tools/png-to-jpg" },
      { name: "WebP → JPG", path: "/tools/webp-to-jpg" },
      { name: "JPG → WebP", path: "/tools/jpg-to-webp" },
      { name: "Image Resize", path: "/tools/image-resize" },
      { name: "Image Compress", path: "/tools/image-compress" },
    ],
  },
  {
    title: "PDF Tools",
    items: [
      { name: "Images → PDF", path: "/tools/images-to-pdf" },
      { name: "PDF Merge", path: "/tools/pdf-merge" },
      { name: "PDF Split", path: "/tools/pdf-split" },
    ],
  },
  {
    title: "Extractors",
    items: [
      { name: "ZIP Extractor", path: "/tools/zip-extractor" },
    ],
  }
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/60 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6">
        
        {/* Brand Logo & Name */}
        <Link href="/" className="group flex items-center gap-3 transition-transform hover:scale-[1.02]">
          <div className="relative flex h-12 w-12 items-center justify-center rounded-xl bg-slate-900/50 border border-slate-700/50 shadow-lg shadow-cyan-500/20 transition-all duration-300 group-hover:shadow-cyan-500/40 group-hover:border-cyan-500/50 overflow-hidden">
            {/* <Image 
              src="/FileConversion_logo.png" 
              alt="FileConverter Logo"  
              width={48} 
              height={48} 
              className="object-contain scale-110 drop-shadow-[0_0_8px_rgba(34,211,238,0.3)] transition-all duration-300 group-hover:drop-shadow-[0_0_12px_rgba(34,211,238,0.8)]"
              priority 
            /> */}
            
            <svg 
              className="h-7 w-7 text-white" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              {/* Document/File Icon Paths */}
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
             </svg>
          </div>
          <span className="text-2xl font-extrabold tracking-tight text-white">
            File<span className="text-cyan-400">Converter</span>
          </span>
        </Link>

        {/* Desktop Navigation with Dropdowns */}
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
          
          {/* Map through the menus array */}
          {navMenus.map((menu, index) => (
            <div key={index} className="relative group">
              {/* Dropdown Trigger */}
              <button className="flex items-center gap-1.5 py-8 hover:text-cyan-400 transition-colors">
                {menu.title}
                {/* Simple SVG Chevron Arrow */}
                <svg className="w-4 h-4 text-slate-500 transition-transform group-hover:rotate-180 group-hover:text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* Dropdown Menu Container */}
              {/* The pt-6 bridge ensures the hover state doesn't break when moving the mouse down */}
              <div className="absolute left-0 top-full -mt-2 hidden w-48 pt-2 opacity-0 transition-opacity group-hover:block group-hover:opacity-100">
                <div className="overflow-hidden rounded-xl border border-slate-700/60 bg-slate-900/95 backdrop-blur-lg shadow-xl shadow-black/50 py-2">
                  {menu.items.map((item, i) => (
                    <Link 
                      key={i} 
                      href={item.path}
                      className="block px-4 py-2.5 text-sm text-slate-300 hover:bg-slate-800 hover:text-cyan-400 transition-colors"
                    >
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          ))}

          {/* Standalone API Docs Link */}
          {/* <Link href="/api-docs" className="hover:text-cyan-400 transition py-8">API Docs</Link>
           */}
        </nav>
      </div>
    </header>
  );
}