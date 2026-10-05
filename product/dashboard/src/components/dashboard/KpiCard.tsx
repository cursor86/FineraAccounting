import { ShieldCheck, Timer, TrendingUp, Users } from 'lucide-react';
import type { ComponentType } from 'react';

import { DashboardCard } from '@/components/dashboard/DashboardCard';
import { CHART_COLORS } from '@/components/dashboard/colors';

const kpis: { name: string; icon: ComponentType<{ className?: string }>; value: number; sub: string }[] = [
  { name: 'Implementation Time', icon: Timer, value: 70, sub: 'faster vs. baseline' },
  { name: 'Scalability Index', icon: TrendingUp, value: 43, sub: 'headroom used' },
  { name: 'User Adoption', icon: Users, value: 50, sub: 'of target cohort' },
  { name: 'Compliance Readiness', icon: ShieldCheck, value: 40, sub: 'controls verified' },
];

function Radial({ value }: { value: number }) {
  return (
    <div
      className="relative flex h-11 w-11 shrink-0 items-center justify-center rounded-full"
      style={{ background: `conic-gradient(${CHART_COLORS.cyan} ${value * 3.6}deg, hsl(var(--secondary)) 0deg)` }}
    >
      <div className="absolute inset-[3px] flex items-center justify-center rounded-full bg-card">
        <span className="font-mono text-[10px] font-bold text-card-foreground">{value}%</span>
      </div>
    </div>
  );
}

export function KpiCard() {
  return (
    <DashboardCard
      title="Illustrative Strategic KPIs"
      note="Sample metrics shown for layout — replace with real figures before use"
    >
      <div className="flex flex-col divide-y divide-border">
        {kpis.map((k) => {
          const Icon = k.icon;
          return (
            <div key={k.name} className="flex items-center gap-3 py-2.5 first:pt-0 last:pb-0">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-secondary text-cyan-400">
                <Icon className="h-4 w-4" />
              </span>
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm text-card-foreground">{k.name}</p>
                <p className="text-[11px] text-muted-foreground">{k.sub}</p>
              </div>
              <Radial value={k.value} />
            </div>
          );
        })}
      </div>
    </DashboardCard>
  );
}
