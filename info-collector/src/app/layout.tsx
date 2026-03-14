import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "InfoCollector",
  description: "信息收集与知识管理",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  );
}