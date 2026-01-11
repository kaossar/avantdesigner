import type { Metadata } from 'next';
import { Inter, Lexend } from 'next/font/google';
import './globals.css';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

const inter = Inter({
  variable: '--font-sans',
  subsets: ['latin'],
  display: 'swap',
});

const lexend = Lexend({
  variable: '--font-display',
  subsets: ['latin'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'AvantDeSigner – Vérifiez votre contrat',
  description:
    'Identifiez les clauses à risque, comprenez les pièges, et obtenez des reformulations protectrices avant de signer. À partir de 2€.',
  keywords: [
    'vérification contrat',
    'clause abusive',
    'analyse contrat',
    'protection contractuelle',
    'arnaque contrat',
  ],
  authors: [{ name: 'AvantDeSigner' }],
  openGraph: {
    title: 'AvantDeSigner – Vérifiez votre contrat',
    description:
      'Identifiez les clauses à risque et protégez-vous avant de signer. Analyse de contrats accessible à tous.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className={`${inter.variable} ${lexend.variable}`}>
      <body className="antialiased">
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}

