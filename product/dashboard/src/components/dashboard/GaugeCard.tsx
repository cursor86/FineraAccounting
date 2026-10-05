import { RadialBar, RadialBarChart, ResponsiveContainer } from 'recharts';

import { DashboardCard } from '@/components/dashboard/DashboardCard';
import { CHART_COLORS } from '@/components/dashboard/colors';

const value = 82;

const ecosystems = [
  { k: 'G', name: 'Search', color: '#6366F1' },
  { k: 'M', name: 'Productivity', color: '#22D3EE' },
  { k: 'L', name: 'Professional', color: '#2563EB' },
  { k: 'S', name: 'Collaboration', color: '#F59E0B' },
];

export function GaugeCard() {
  return (
    <DashboardCard
      title="Illustrative Integration Coverage"
      note="Sample score — generic ecosystem categories, not vendor-branded"
    >
      <div className="relative h-28">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart
            cx="50%"
            cy="100%"
            innerRadius="130%"
            outerRadius="220%"
            barSize={16}
            startAngle={180}
            endAngle={0}
            data={[{ value, fill: CHART_COLORS.cyan }]}
          >
            <RadialBar
              background={{ fill: 'hsl(var(--secondary))' }}
              dataKey="value"
              cornerRadius={8}
              isAnimationActive={false}
            />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-end pb-1">
          <span className="font-mono text-2xl font-extrabold text-card-foreground">{value}%</span>
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground">integrated</span>
        </div>
      </div>
      <div className="grid grid-cols-4 gap-2 pt-1">
        {ecosystems.map((e) => (
          <div key={e.name} className="flex flex-col items-center gap-1.5">
            <span
              className="flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold text-white"
              style={{ background: e.color }}
            >
              {e.k}
            </span>
            <span className="text-center text-[10px] leading-tight text-muted-foreground">{e.name}</span>
          </div>
        ))}
      </div>
    </DashboardCard>
  );
}
