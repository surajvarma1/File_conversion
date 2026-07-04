// "use client";

// import { useState } from "react";
// import { useForm, Controller } from "react-hook-form";
// import axios from "axios";
// import { PDFDocument } from "pdf-lib";
// import { toolDefinitions } from "@/constants/tools";
// import DragDrop from "./DragDrop";

// type FormValues = {
//   files: File[] | null;
//   quality?: number;
//   width?: number;
//   height?: number;
//   maintainAspect?: boolean;
//   maxSize?: number;
//   pages?: string;
//   split_mode?: string;
// };

// interface ToolFormProps {
//   tool: string;
// }

// export default function ToolForm({ tool }: ToolFormProps) {
//   const toolConfig = toolDefinitions[tool];
  
//   const [result, setResult] = useState<{ download_url?: string } | null>(null);
//   const [error, setError] = useState<string | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
  
//   const [fileMeta, setFileMeta] = useState<{ pages?: number; size: string } | null>(null);

//   const { register, handleSubmit, setValue, control, watch, formState: { errors } } = useForm<FormValues>({
//     defaultValues: { 
//       maintainAspect: true, 
//       quality: toolConfig?.defaultQuality || 80, 
//       width: 1024, 
//       height: 768,
//       split_mode: "specific" 
//     },
//   });

//   const currentSplitMode = watch("split_mode");

//   const onSubmit = async (data: FormValues) => {
//     if (!toolConfig) return;
//     if (!data.files || data.files.length === 0) {
//       setError("Please select a file to convert.");
//       return;
//     }

//     const formData = new FormData();
//     data.files.forEach((file) => formData.append(toolConfig.supportsMultiple ? "files" : "file", file));

//     const queryParams: Record<string, string | number | boolean> = {};

//     if (toolConfig.supportsQuality && data.quality) queryParams.quality = data.quality;
//     if (toolConfig.supportsResize) {
//       if (data.width) queryParams.width = data.width;
//       if (data.height) queryParams.height = data.height;
//       if (data.maintainAspect !== undefined) queryParams.maintain_aspect = data.maintainAspect;
//     }
//     if (toolConfig.supportsMaxSize && data.maxSize) queryParams.max_size = data.maxSize;
    
//     if (toolConfig.supportsPages) {
//       if (data.split_mode) queryParams.split_mode = data.split_mode;
//       if (data.pages && (data.split_mode === "specific" || data.split_mode === "range")) {
//         queryParams.pages = data.pages;
//       }
//     }

//     setError(null);
//     setResult(null);
//     setIsLoading(true);

//     try {
//       const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";
      
//       // Step 1: Initial Generation Request
//       const response = await axios.post(toolConfig.apiEndpoint, formData, {
//         baseURL,
//         headers: { "Content-Type": "multipart/form-data" },
//         params: queryParams, 
//       });
      
//       let finalData = response.data;

//       // Step 2: Handle Two-Step Download Architecture (PDF & ZIP tools)
//       if (!finalData.download_url && (finalData.output_directory || finalData.output_file)) {
//         // Extract filename from the Windows/Linux path string (e.g. "app\outputs\filename_123")
//         const rawPath = finalData.output_directory || finalData.output_file;
//         const filename = rawPath.split(/\\|\//).pop(); 
        
//         // Extract the category from the endpoint (e.g. "/zip/extract" -> "zip")
//         const endpointParts = toolConfig.apiEndpoint.split('/');
//         const category = endpointParts[1]; 
        
//         // Fetch the signed download link
//         const downloadResponse = await axios.get(`/${category}/download/${filename}`, {
//           baseURL,
//         });

//         if (downloadResponse.data && downloadResponse.data.url) {
//           finalData.download_url = downloadResponse.data.url;
//         }
//       }

//       setResult(finalData);
//     } catch (err) {
//       setError(axios.isAxiosError(err) ? err.response?.data?.detail || err.message : "Unknown error occurred");
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const getFinalDownloadUrl = () => {
//     if (!result?.download_url) return null;
//     const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";
//     const serverRoot = baseURL.replace('/api/v1', '');
//     return result.download_url.startsWith('http') ? result.download_url : `${serverRoot}${result.download_url.startsWith('/') ? '' : '/'}${result.download_url}`;
//   };

//   if (!toolConfig) return <p className="text-red-400">Tool not found.</p>;

//   return (
//     <div className="space-y-6">
//       <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 rounded-3xl border border-slate-800 bg-slate-950 p-8 shadow-2xl">
        
//         <div>
//           <label className="mb-3 block text-sm font-semibold text-slate-300">Upload your file</label>
//           <DragDrop 
//             accept={toolConfig.acceptedFormats} 
//             multiple={toolConfig.supportsMultiple}
//             onFiles={async (files) => {
//               const fileArray = Array.isArray(files) ? files : Array.from(files);
//               setValue("files", fileArray, { shouldValidate: true });
              
//               if (fileArray.length > 0) {
//                 const file = fileArray[0];
//                 const sizeStr = (file.size / (1024 * 1024)).toFixed(2) + " MB";
//                 let pages = undefined;

//                 if (file.type === "application/pdf") {
//                   try {
//                     const arrayBuffer = await file.arrayBuffer();
//                     const pdfDoc = await PDFDocument.load(arrayBuffer, { ignoreEncryption: true });
//                     pages = pdfDoc.getPageCount();
//                   } catch (e) {
//                     console.error("Failed to parse PDF metadata", e);
//                   }
//                 }
//                 setFileMeta({ pages, size: sizeStr });
//               } else {
//                 setFileMeta(null);
//               }
//             }}
//           />
//           {errors.files && <p className="mt-2 text-sm text-red-400">{errors.files.message}</p>}
          
//           {fileMeta && (
//             <div className="mt-3 flex items-center gap-4 text-sm text-cyan-400">
//               <span>Size: {fileMeta.size}</span>
//               {fileMeta.pages && <span>Pages: {fileMeta.pages}</span>}
//             </div>
//           )}
//         </div>

//         <div className="grid gap-6 sm:grid-cols-2 bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
//           {toolConfig.supportsQuality && (
//             <div>
//               <label className="mb-2 block text-sm font-medium text-slate-300">Quality (1-100)</label>
//               <input type="number" min={1} max={100} {...register("quality")} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 focus:border-cyan-500 outline-none transition text-slate-200" />
//             </div>
//           )}
          
//           {toolConfig.supportsResize && (
//             <>
//               <div>
//                 <label className="mb-2 block text-sm font-medium text-slate-300">Width (px)</label>
//                 <input type="number" min={1} {...register("width")} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500 text-slate-200" />
//               </div>
//               <div>
//                 <label className="mb-2 block text-sm font-medium text-slate-300">Height (px)</label>
//                 <input type="number" min={1} {...register("height")} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500 text-slate-200" />
//               </div>
//             </>
//           )}

//           {toolConfig.supportsPages && (
//             <div className="sm:col-span-2 grid gap-6 sm:grid-cols-2">
//               <div>
//                 <label className="mb-2 block text-sm font-medium text-slate-300">Split Mode</label>
//                 <select 
//                   {...register("split_mode")} 
//                   className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500 text-slate-200"
//                 >
//                   <option value="specific">Specific Pages</option>
//                   <option value="range">Page Range</option>
//                   <option value="even">Even Pages Only</option>
//                   <option value="odd">Odd Pages Only</option>
//                 </select>
//               </div>

//               <Controller
//                 name="pages"
//                 control={control}
//                 rules={{
//                   validate: (value) => {
//                     if ((currentSplitMode !== "specific" && currentSplitMode !== "range")) return true;
//                     if (!value) return "This field is required.";
                    
//                     if (fileMeta?.pages) {
//                       const max = fileMeta.pages;
                      
//                       if (currentSplitMode === "specific") {
//                         const pages = value.split(',').map(p => parseInt(p.trim()));
//                         if (pages.some(p => isNaN(p) || p < 1 || p > max)) {
//                           return `Enter valid pages between 1 and ${max}.`;
//                         }
//                       } 
                      
//                       if (currentSplitMode === "range") {
//                         const parts = value.split('-');
//                         if (parts.length !== 2) return "Use format: start-end (e.g., 1-5)";
//                         const start = parseInt(parts[0].trim());
//                         const end = parseInt(parts[1].trim());
//                         if (isNaN(start) || isNaN(end) || start < 1 || end > max || start > end) {
//                           return `Enter a valid range between 1 and ${max}.`;
//                         }
//                       }
//                     }
//                     return true;
//                   }
//                 }}
//                 render={({ field }) => (
//                   (currentSplitMode === "specific" || currentSplitMode === "range") ? (
//                     <div>
//                       <label className="mb-2 block text-sm font-medium text-slate-300">
//                         {currentSplitMode === "specific" ? "Pages (e.g., 1,4,5)" : "Range (e.g., 1-5)"}
//                       </label>
//                       <input 
//                         type="text" 
//                         placeholder={currentSplitMode === "specific" ? "1,4,5" : "1-5"} 
//                         {...field}
//                         className={`w-full rounded-xl border bg-slate-900 px-4 py-3 outline-none transition text-slate-200 ${errors.pages ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-cyan-500'}`} 
//                       />
//                       {errors.pages && <p className="mt-1 text-sm text-red-400">{errors.pages.message}</p>}
//                     </div>
//                   ) : <div /> 
//                 )}
//               />
//             </div>
//           )}
//         </div>

//         <button type="submit" disabled={isLoading} className="group relative flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-8 py-4 text-lg font-bold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60 overflow-hidden">
//           {isLoading ? (
//              <span className="flex items-center gap-2">
//                 <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
//                 Processing...
//              </span>
//           ) : toolConfig.actionLabel}
//         </button>
//       </form>

//       {error && (
//         <div className="rounded-2xl border-l-4 border-red-500 bg-red-950/40 p-5 text-red-200">
//           <p className="font-semibold text-red-400">Conversion Failed</p>
//           <p className="mt-1 text-sm">{error}</p>
//         </div>
//       )}

//       {result && (
//         <div className="flex flex-col items-center justify-center rounded-3xl border border-green-500/30 bg-green-950/10 p-8 shadow-[0_0_30px_rgba(34,197,94,0.05)] text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
//           <div className="mb-4 rounded-full bg-green-500/20 p-4">
//             <svg className="h-10 w-10 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
//           </div>
//           <h3 className="text-2xl font-bold text-slate-100">Conversion Complete!</h3>
//           <p className="mt-2 text-slate-400">Your file has been successfully processed and is ready to download.</p>
          
//           {getFinalDownloadUrl() && (
//             <a 
//               href={getFinalDownloadUrl()!}
//               target="_blank"
//               rel="noopener noreferrer"
//               className="mt-8 flex items-center gap-2 rounded-full bg-green-500 px-8 py-4 font-bold text-slate-950 transition hover:scale-105 hover:bg-green-400 hover:shadow-lg hover:shadow-green-500/30"
//             >
//               <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
//               Download File
//             </a>
//           )}
//         </div>
//       )}
//     </div>
//   );
// }


"use client";

import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import axios from "axios";
import { PDFDocument } from "pdf-lib";
import { toolDefinitions } from "@/constants/tools";
import DragDrop from "./DragDrop";

type FormValues = {
  files: File[] | null;
  quality?: number;
  width?: number;
  height?: number;
  maintainAspect?: boolean;
  maxSize?: number;
  pages?: string;
  split_mode?: string;
};

interface ToolFormProps {
  tool: string;
}

// Added type for the new ZIP extractor file response
type ExtractedFile = {
  filename: string;
  filepath: string;
  download_url: string;
};

export default function ToolForm({ tool }: ToolFormProps) {
  const toolConfig = toolDefinitions[tool];
  
  // Updated state to handle both single download_url and the new files array
  const [result, setResult] = useState<{ 
    download_url?: string; 
    files?: ExtractedFile[] 
  } | null>(null);
  
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const [fileMeta, setFileMeta] = useState<{ pages?: number; size: string } | null>(null);

  const { register, handleSubmit, setValue, control, watch, formState: { errors } } = useForm<FormValues>({
    defaultValues: { 
      maintainAspect: true, 
      quality: toolConfig?.defaultQuality || 80, 
      width: 1024, 
      height: 768,
      split_mode: "specific" 
    },
  });

  const currentSplitMode = watch("split_mode");

  const onSubmit = async (data: FormValues) => {
    if (!toolConfig) return;
    if (!data.files || data.files.length === 0) {
      setError("Please select a file to convert.");
      return;
    }

    const formData = new FormData();
    data.files.forEach((file) => formData.append(toolConfig.supportsMultiple ? "files" : "file", file));

    const queryParams: Record<string, string | number | boolean> = {};

    if (toolConfig.supportsQuality && data.quality) queryParams.quality = data.quality;
    if (toolConfig.supportsResize) {
      if (data.width) queryParams.width = data.width;
      if (data.height) queryParams.height = data.height;
      if (data.maintainAspect !== undefined) queryParams.maintain_aspect = data.maintainAspect;
    }
    if (toolConfig.supportsMaxSize && data.maxSize) queryParams.max_size = data.maxSize;
    
    if (toolConfig.supportsPages) {
      if (data.split_mode) queryParams.split_mode = data.split_mode;
      if (data.pages && (data.split_mode === "specific" || data.split_mode === "range")) {
        queryParams.pages = data.pages;
      }
    }

    setError(null);
    setResult(null);
    setIsLoading(true);

    try {
      const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";
      
      // Step 1: Initial Generation Request
      const response = await axios.post(toolConfig.apiEndpoint, formData, {
        baseURL,
        headers: { "Content-Type": "multipart/form-data" },
        params: queryParams, 
      });
      
      let finalData = response.data;

      // Step 2: Handle Two-Step Download Architecture (PDF & ZIP tools)
      // Skip this if the backend already returned our `files` array (like the updated ZIP route does)
      if (!finalData.download_url && !finalData.files && (finalData.output_directory || finalData.output_file)) {
        const rawPath = finalData.output_directory || finalData.output_file;
        const filename = rawPath.split(/\\|\//).pop(); 
        
        const endpointParts = toolConfig.apiEndpoint.split('/');
        const category = endpointParts[1]; 
        
        const downloadResponse = await axios.get(`/${category}/download/${filename}`, {
          baseURL,
        });

        if (downloadResponse.data && downloadResponse.data.url) {
          finalData.download_url = downloadResponse.data.url;
        }
      }

      setResult(finalData);
    } catch (err) {
      setError(axios.isAxiosError(err) ? err.response?.data?.detail || err.message : "Unknown error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  // Replaced getFinalDownloadUrl with a flexible formatter for both single files and arrays
  const formatDownloadUrl = (url?: string) => {
    if (!url) return "";
    const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";
    const serverRoot = baseURL.replace('/api/v1', '');
    return url.startsWith('http') ? url : `${serverRoot}${url.startsWith('/') ? '' : '/'}${url}`;
  };

  if (!toolConfig) return <p className="text-red-400">Tool not found.</p>;

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8 rounded-3xl border border-slate-800 bg-slate-950 p-8 shadow-2xl">
        
        <div>
          <label className="mb-3 block text-sm font-semibold text-slate-300">Upload your file</label>
          <DragDrop 
            accept={toolConfig.acceptedFormats} 
            multiple={toolConfig.supportsMultiple}
            onFiles={async (files) => {
              const fileArray = Array.isArray(files) ? files : Array.from(files);
              setValue("files", fileArray, { shouldValidate: true });
              
              if (fileArray.length > 0) {
                const file = fileArray[0];
                const sizeStr = (file.size / (1024 * 1024)).toFixed(2) + " MB";
                let pages = undefined;

                if (file.type === "application/pdf") {
                  try {
                    const arrayBuffer = await file.arrayBuffer();
                    const pdfDoc = await PDFDocument.load(arrayBuffer, { ignoreEncryption: true });
                    pages = pdfDoc.getPageCount();
                  } catch (e) {
                    console.error("Failed to parse PDF metadata", e);
                  }
                }
                setFileMeta({ pages, size: sizeStr });
              } else {
                setFileMeta(null);
              }
            }}
          />
          {errors.files && <p className="mt-2 text-sm text-red-400">{errors.files.message}</p>}
          
          {fileMeta && (
            <div className="mt-3 flex items-center gap-4 text-sm text-cyan-400">
              <span>Size: {fileMeta.size}</span>
              {fileMeta.pages && <span>Pages: {fileMeta.pages}</span>}
            </div>
          )}
        </div>

        <div className="grid gap-6 sm:grid-cols-2 bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
          {toolConfig.supportsQuality && (
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-300">Quality (1-100)</label>
              <input type="number" min={1} max={100} {...register("quality")} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 focus:border-cyan-500 outline-none transition text-slate-200" />
            </div>
          )}
          
          {toolConfig.supportsResize && (
            <>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Width (px)</label>
                <input type="number" min={1} {...register("width")} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500 text-slate-200" />
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Height (px)</label>
                <input type="number" min={1} {...register("height")} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500 text-slate-200" />
              </div>
            </>
          )}

          {toolConfig.supportsPages && (
            <div className="sm:col-span-2 grid gap-6 sm:grid-cols-2">
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Split Mode</label>
                <select 
                  {...register("split_mode")} 
                  className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 outline-none focus:border-cyan-500 text-slate-200"
                >
                  <option value="specific">Specific Pages</option>
                  <option value="range">Page Range</option>
                  <option value="even">Even Pages Only</option>
                  <option value="odd">Odd Pages Only</option>
                </select>
              </div>

              <Controller
                name="pages"
                control={control}
                rules={{
                  validate: (value) => {
                    if ((currentSplitMode !== "specific" && currentSplitMode !== "range")) return true;
                    if (!value) return "This field is required.";
                    
                    if (fileMeta?.pages) {
                      const max = fileMeta.pages;
                      
                      if (currentSplitMode === "specific") {
                        const pages = value.split(',').map(p => parseInt(p.trim()));
                        if (pages.some(p => isNaN(p) || p < 1 || p > max)) {
                          return `Enter valid pages between 1 and ${max}.`;
                        }
                      } 
                      
                      if (currentSplitMode === "range") {
                        const parts = value.split('-');
                        if (parts.length !== 2) return "Use format: start-end (e.g., 1-5)";
                        const start = parseInt(parts[0].trim());
                        const end = parseInt(parts[1].trim());
                        if (isNaN(start) || isNaN(end) || start < 1 || end > max || start > end) {
                          return `Enter a valid range between 1 and ${max}.`;
                        }
                      }
                    }
                    return true;
                  }
                }}
                render={({ field }) => (
                  (currentSplitMode === "specific" || currentSplitMode === "range") ? (
                    <div>
                      <label className="mb-2 block text-sm font-medium text-slate-300">
                        {currentSplitMode === "specific" ? "Pages (e.g., 1,4,5)" : "Range (e.g., 1-5)"}
                      </label>
                      <input 
                        type="text" 
                        placeholder={currentSplitMode === "specific" ? "1,4,5" : "1-5"} 
                        {...field}
                        className={`w-full rounded-xl border bg-slate-900 px-4 py-3 outline-none transition text-slate-200 ${errors.pages ? 'border-red-500 focus:border-red-500' : 'border-slate-700 focus:border-cyan-500'}`} 
                      />
                      {errors.pages && <p className="mt-1 text-sm text-red-400">{errors.pages.message}</p>}
                    </div>
                  ) : <div /> 
                )}
              />
            </div>
          )}
        </div>

        <button type="submit" disabled={isLoading} className="group relative flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-500 px-8 py-4 text-lg font-bold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60 overflow-hidden">
          {isLoading ? (
             <span className="flex items-center gap-2">
                <svg className="h-5 w-5 animate-spin" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Processing...
             </span>
          ) : toolConfig.actionLabel}
        </button>
      </form>

      {error && (
        <div className="rounded-2xl border-l-4 border-red-500 bg-red-950/40 p-5 text-red-200">
          <p className="font-semibold text-red-400">Conversion Failed</p>
          <p className="mt-1 text-sm">{error}</p>
        </div>
      )}

      {result && (
        <div className="flex flex-col items-center justify-center rounded-3xl border border-green-500/30 bg-green-950/10 p-8 shadow-[0_0_30px_rgba(34,197,94,0.05)] text-center animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="mb-4 rounded-full bg-green-500/20 p-4">
            <svg className="h-10 w-10 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
          </div>
          <h3 className="text-2xl font-bold text-slate-100">Conversion Complete!</h3>
          <p className="mt-2 text-slate-400">Your file has been successfully processed and is ready to download.</p>
          
          {/* Scenario A: Single File Download (Merge, Split, Images to PDF, etc.) */}
          {result.download_url && !result.files && (
            <a 
              href={formatDownloadUrl(result.download_url)}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-8 flex items-center gap-2 rounded-full bg-green-500 px-8 py-4 font-bold text-slate-950 transition hover:scale-105 hover:bg-green-400 hover:shadow-lg hover:shadow-green-500/30"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
              Download File
            </a>
          )}

          {/* Scenario B: Multiple Files Download (ZIP Extractor) */}
          {result.files && result.files.length > 0 && (
            <div className="mt-8 w-full max-w-lg text-left">
              <h4 className="mb-4 text-lg font-semibold text-slate-200 border-b border-slate-700 pb-2">Extracted Files</h4>
              <ul className="max-h-60 overflow-y-auto space-y-3 pr-2 scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-transparent">
                {result.files.map((file, idx) => (
                  <li key={idx} className="flex items-center justify-between gap-4 rounded-xl bg-slate-900/80 p-4 border border-slate-800 hover:border-slate-600 transition">
                    <span className="truncate text-sm font-medium text-slate-300" title={file.filename}>
                      {file.filename}
                    </span>
                    <a
                      href={formatDownloadUrl(file.download_url)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-shrink-0 flex items-center gap-2 rounded-lg bg-cyan-500/10 px-4 py-2 text-sm font-bold text-cyan-400 transition hover:bg-cyan-500 hover:text-slate-950 border border-cyan-500/20 hover:border-transparent"
                    >
                      <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                      Download
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}