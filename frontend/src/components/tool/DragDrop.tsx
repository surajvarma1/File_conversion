"use client";

import { useRef, useState } from "react";

export default function DragDrop({ 
  onFiles, 
  accept, 
  multiple = false 
}: { 
  onFiles: (files: FileList | File[]) => void;
  accept?: string;
  multiple?: boolean;
}) {
  const ref = useRef<HTMLInputElement | null>(null);
  const [hover, setHover] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setHover(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length) {
      const files = Array.from(e.dataTransfer.files);
      setSelectedFiles(multiple ? files : [files[0]]);
      onFiles(multiple ? files : [files[0]]);
    }
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    if (e.target.files && e.target.files.length) {
      const files = Array.from(e.target.files);
      setSelectedFiles(multiple ? files : [files[0]]);
      onFiles(multiple ? files : [files[0]]);
    }
  }

  return (
    <div className="w-full">
      <div
        className={`relative cursor-pointer rounded-2xl border-2 border-dashed p-8 text-center transition-all duration-200 ease-in-out ${
          hover 
            ? "border-cyan-400 bg-cyan-950/20 shadow-[0_0_15px_rgba(34,211,238,0.2)]" 
            : "border-slate-700 bg-slate-900/50 hover:border-slate-500 hover:bg-slate-800/50"
        }`}
        onDragOver={(e) => { e.preventDefault(); setHover(true); }}
        onDragLeave={(e) => { e.preventDefault(); setHover(false); }}
        onDrop={handleDrop}
        onClick={() => ref.current?.click()}
      >
        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="rounded-full bg-slate-800 p-4">
            <svg className="h-8 w-8 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <p className="text-lg font-medium text-slate-200">Drag & drop files here</p>
          <p className="text-sm text-slate-400">or click to browse your computer</p>
        </div>

        <input
          ref={ref}
          type="file"
          accept={accept}
          multiple={multiple}
          className="hidden"
          onChange={handleChange}
        />
      </div>

      {/* Display selected files so the user knows it worked */}
      {selectedFiles.length > 0 && (
        <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900 p-4">
          <h4 className="mb-2 text-sm font-semibold text-slate-300">Selected File(s):</h4>
          <ul className="space-y-2 text-sm text-cyan-300">
            {selectedFiles.map((f, i) => (
              <li key={i} className="flex items-center gap-2">
                 <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                 {f.name} ({(f.size / 1024 / 1024).toFixed(2)} MB)
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}