import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import { DashboardCard, DashboardLegend } from '@/components/dashboard/DashboardCard';
import { CHART_COLORS } from '@/components/dashboard/colors';

const data = [
  { period: "Q1 '25", sales: 12, marketing: 8, operations: 6, finance: 4 },
  { period: "Q2 '25", sales: 18, marketing: 11, operations: 7, finance: 5 },
  { period: "Q3 '25", sales: 24, marketing: 15, operations: 9, finance: 6 },
  { period: "Q4 '25", sales: 31, marketing: 19, operations: 13, finance: 8 },
  { period: "Q1 '26", sales: 38, marketing: 25, operations: 16, finance: 10 },
  { period: "Q2 '26", sales: 44, marketing: 29, operations: 18, finance: 13 },
];

const series = [
  { key: 'sales', label: 'Sales', color: CHART_COLORS.indigo },
  { key: 'marketing', label: 'Marketing', color: CHART_COLORS.cyan },
  { key: 'operations', label: 'Operations', color: CHART_COLORS.amber },
  { key: 'finance', label: 'Finance', color: CHART_COLORS.emerald },
];

export function TrendCard() {
  return (
    <DashboardCard title="Illustrative Adoption Trend (2025–2026)" note="Sample series, for layout purposes only">
      <div className="h-44">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 6, right: 8, bottom: 0, left: -18 }}>
            <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="2 4" vertical={false} />
            <XAxis
              dataKey="period"
              tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
              axisLine={{ stroke: 'hsl(var(--border))' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: 'hsl(var(--muted-foreground))', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) => `${v}%`}
            />
            <Tooltip
              contentStyle={{
                background: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: 8,
                fontSize: 12,
              }}
            />
            {series.map((s) => (
              <Line
                key={s.key}
                type="monotone"
                dataKey={s.key}
                name={s.label}
                stroke={s.color}
                strokeWidth={2}
                dot={{ r: 2.5 }}
                isAnimationActive={false}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
      <DashboardLegend items={series.map((s) => ({ label: s.label, color: s.color }))} />
    </DashboardCard>
  );
}
