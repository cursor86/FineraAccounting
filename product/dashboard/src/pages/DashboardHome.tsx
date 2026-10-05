import { DonutCard } from '@/components/dashboard/DonutCard';
import { FeatureCard } from '@/components/dashboard/FeatureCard';
import { GaugeCard } from '@/components/dashboard/GaugeCard';
import { KpiCard } from '@/components/dashboard/KpiCard';
import { TrendCard } from '@/components/dashboard/TrendCard';

const DashboardHome = () => {
  return (
    <div className="flex h-full flex-col gap-5 px-5 py-7 sm:px-8">
      <header className="flex flex-col gap-1.5 pb-1">
        <span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-cyan-400">
          Dashboard template
        </span>
        <h1 className="text-2xl font-extrabold text-foreground sm:text-[28px]">Ecosystem Pulse</h1>
        <p className="max-w-[62ch] text-sm text-muted-foreground">
          A reusable dashboard layout — donut, trend, gauge, scored progress bars and KPI loaders — built with
          sample data. Swap in real figures from a verified source before sharing it as fact.
        </p>
      </header>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <DonutCard />
        <TrendCard />
        <GaugeCard />
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <FeatureCard />
        <KpiCard />
      </section>

      <footer className="border-t border-border pt-3 text-xs leading-relaxed text-muted-foreground">
        Every number on this page is illustrative sample data for layout purposes, not a researched or sourced
        claim about any real vendor or market. Replace each card&apos;s dataset with verified figures before
        presenting it as market research.
      </footer>
    </div>
  );
};

export default DashboardHome;
