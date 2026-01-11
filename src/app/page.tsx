import { HeroSection } from '@/components/home/HeroSection';
import { HowItWorks } from '@/components/home/HowItWorks';
import { ContractTypes } from '@/components/home/ContractTypes';
import { PricingSection } from '@/components/home/PricingSection';
import { FAQ } from '@/components/home/FAQ';

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <HowItWorks />
      <ContractTypes />
      <PricingSection />
      <FAQ />
    </>
  );
}
