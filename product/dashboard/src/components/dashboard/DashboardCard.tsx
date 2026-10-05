import type { ReactNode } from 'react';

import { cn } from '@/lib/utils';

interface DashboardCardProps {
  title: string;
  note?: string;
  className?: string;
  children: ReactNode;
}

export function DashboardCard({ title, note, className, children }: DashboardCardProps) {
  return (
    <div className={cn('flex flex-col gap-3.5 rounded-2xl border border-border bg-card p-5', className)}>
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-[15px] font-semibold leading-snug text-card-foreground">{title}</h3>
      </div>
      {note && <p className="-mt-2 text-xs text-muted-foreground">{note}</p>}
      {children}
    </div>
  );
}

interface LegendItem {
  label: string;
  color: string;
}

export function DashboardLegend({ items }: { items: LegendItem[] }) {
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-1.5 text-xs text-muted-foreground">
      {items.map((it) => (
        <span key={it.label} className="inline-flex items-center gap-1.5">
          <span className="inline-block h-2 w-2 rounded-full" style={{ background: it.color }} />
          {it.label}
        </span>
      ))}
    </div>
  );
}
