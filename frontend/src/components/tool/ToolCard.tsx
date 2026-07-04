"use client";

import Link from "next/link";

export default function ToolCard({ href, title, description }: { href: string; title: string; description: string }) {
  return (
    <Link href={href} className="block rounded-2xl border border-slate-800 bg-slate-950 p-6 hover:scale-[1.01]">
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="mt-2 text-sm text-slate-400">{description}</p>
    </Link>
  );
}
