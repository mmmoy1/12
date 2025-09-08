import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { CartProvider } from "@/contexts/CartContext";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Drip Lab - Luxury Jewelry Studio",
  description: "Discover exquisite handcrafted jewelry pieces at Drip Lab. Premium gold, silver, and platinum collections with 3D visualization.",
  keywords: "jewelry, luxury, gold, silver, platinum, rings, necklaces, earrings, handcrafted",
  authors: [{ name: "Drip Lab" }],
  openGraph: {
    title: "Drip Lab - Luxury Jewelry Studio",
    description: "Discover exquisite handcrafted jewelry pieces at Drip Lab.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans antialiased bg-background text-foreground`}>
        <CartProvider>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
        </CartProvider>
      </body>
    </html>
  );
}
