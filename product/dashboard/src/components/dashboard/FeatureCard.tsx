import { Bar, BarChart, ResponsiveContainer } from 'recharts';

import { DashboardCard } from '@/components/dashboard/DashboardCard';
import { CHART_COLORS } from '@/components/dashboard/colors';

const features = [
  { name: 'Automated Predictive Cash Flow', score: 76, target: 85 },
  { name: 'Seamless Omni-channel Sync', score: 64, target: 80 },
  { name: 'Embedded HR & Payroll', score: 58, target: 70 },
];

const weeklyActivity = [
  { day: 'M', value: 4 },
  { day: 'T', value: 6 },
  { day: 'W', value: 5 },
  { day: 'T2', value: 8 },
  { day: 'F', value: 7 },
  { day: 'S', value: 3 },
  { day: 'S2', value: 2 },
];

export function FeatureCard() {
  return (
    <DashboardCard title="Illustrative Feature Adoption Scores" note="Sample scoring model — not a vendor benchmark">
      <div className="flex flex-col gap-3.5">
        {features.map((f) => (
          <div key={f.name} className="flex flex-col gap-1.5">
            <div className="flex justify-between text-xs">
              <span className="text-card-foreground">{f.name}</span>
              <span className="font-mono text-muted-foreground">{f.score}%</span>
            </div>
            <div className="relative h-2 rounded-full bg-secondary">
              <div
                className="absolute inset-y-0 left-0 rounded-full"
                style={{ width: `${f.score}%`, background: CHART_COLORS.indigo }}
              />
              <div
                className="absolute top-1/2 h-3.5 w-0.5 -translate-y-1/2 bg-foreground/60"
                style={{ left: `${f.target}%` }}
                title={`Target ${f.target}%`}
              />
            </div>
          </div>
        ))}
      </div>
      <div className="border-t border-border pt-1">
        <p className="pb-1 pt-2 text-[10px] uppercase tracking-wider text-muted-foreground">Weekly activity</p>
        <div className="h-16">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={weeklyActivity} barGap={4}>
              <Bar dataKey="value" fill={CHART_COLORS.indigo} radius={[3, 3, 0, 0]} isAnimationActive={false} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </DashboardCard>
  );
}
