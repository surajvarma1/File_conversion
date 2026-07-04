// """Root layout for Next.js application."""

import "./globals.css";
import type { Metadata } from "next";
import Header from "@/components/ui/Header";
import Footer from "@/components/ui/Footer";

export const metadata: Metadata = {
  title: "File Conversion Platform",
  description: "Convert images, PDF, and ZIP files securely and quickly.",
  metadataBase: new URL("http://localhost:3000"),
  openGraph: {
    title: "File Conversion Platform",
    description: "Convert images, PDF, and ZIP files securely and quickly.",
    url: "http://localhost:3000",
    siteName: "File Conversion Platform",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "File Conversion Platform",
    description: "Convert images, PDF, and ZIP files securely and quickly.",
  },
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // Add suppressHydrationWarning here
    <html lang="en" suppressHydrationWarning>
      <body>
        <Header />
        {children}
        <Footer />
      </body>
    </html>
  );
}
