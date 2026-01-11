import { HTMLAttributes, forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
    'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold transition-colors',
    {
        variants: {
            variant: {
                low: 'bg-success-100 text-success-800 border border-success-200',
                medium: 'bg-warning-100 text-warning-800 border border-warning-200',
                high: 'bg-danger-100 text-danger-800 border border-danger-200',
                critical: 'bg-danger-600 text-white shadow-md',
                info: 'bg-primary-100 text-primary-800 border border-primary-200',
                neutral: 'bg-neutral-100 text-neutral-800 border border-neutral-200',
            },
        },
        defaultVariants: {
            variant: 'neutral',
        },
    }
);

export interface BadgeProps
    extends HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> { }

const Badge = forwardRef<HTMLDivElement, BadgeProps>(
    ({ className, variant, ...props }, ref) => {
        return <div ref={ref} className={cn(badgeVariants({ variant }), className)} {...props} />;
    }
);

Badge.displayName = 'Badge';

export { Badge, badgeVariants };
