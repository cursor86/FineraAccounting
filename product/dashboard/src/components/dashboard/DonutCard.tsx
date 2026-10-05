import { Cell, Pie, PieChart, ResponsiveContainer } from 'recharts';

import { DashboardCard, DashboardLegend } from '@/components/dashboard/DashboardCard';
import { CHART_COLORS } from '@/components/dashboard/colors';

const data = [
  { label: 'Core Platform', value: 42, color: CHART_COLORS.indigo },
  { label: 'Integrations', value: 27, color: CHART_COLORS.cyan },
  { label: 'Analytics', value: 18, color: CHART_COLORS.amber },
  { label: 'Support', value: 13, color: CHART_COLORS.emerald },
];

export function DonutCard() {
  return (
    <DashboardCard
      title="Illustrative Platform Mix"
      note="Example allocation — sample data, not a sourced market figure"
    >
      <div className="relative h-44">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="label"
              innerRadius="66%"
              outerRadius="100%"
              paddingAngle={2}
              stroke="hsl(var(--card))"
              strokeWidth={3}
              isAnimationActive={false}
            >
              {data.map((d) => (
                <Cell key={d.label} fill={d.color} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
        <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
          <span className="font-mono text-2xl font-extrabold text-card-foreground">{data[0].value}%</span>
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground">top share</span>
        </div>
      </div>
      <DashboardLegend items={data.map((d) => ({ label: `${d.label} · ${d.value}%`, color: d.color }))} />
    </DashboardCard>
  );
}
