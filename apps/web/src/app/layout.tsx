import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TerraAlerta Chile — prototipo experimental",
  description:
    "Plataforma experimental de inteligencia territorial para San José de Maipo. No sustituye a SENAPRED.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es-CL">
      <body>{children}</body>
    </html>
  );
}
