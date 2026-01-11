import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
    'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
    {
        variants: {
            variant: {
                primary:
                    'bg-primary-800 text-white hover:bg-primary-900 focus-visible:ring-primary-600 shadow-lg hover:shadow-xl font-bold',
                secondary:
                    'bg-slate-100 text-slate-900 hover:bg-slate-200 focus-visible:ring-slate-500 font-semibold',
                outline:
                    'border-2 border-primary-800 text-primary-800 bg-white hover:bg-primary-50 focus-visible:ring-primary-600 font-semibold',
                ghost: 'text-slate-700 hover:bg-slate-100 focus-visible:ring-slate-500',
                danger:
                    'bg-danger-600 text-white hover:bg-danger-700 focus-visible:ring-danger-500 shadow-lg hover:shadow-xl font-bold',
                success:
                    'bg-success-600 text-white hover:bg-success-700 focus-visible:ring-success-500 shadow-lg hover:shadow-xl font-bold',
            },
            size: {
                sm: 'h-9 px-3 text-sm',
                md: 'h-11 px-5 text-base',
                lg: 'h-13 px-7 text-lg',
                xl: 'h-15 px-9 text-xl',
            },
            fullWidth: {
                true: 'w-full',
            },
        },
        defaultVariants: {
            variant: 'primary',
            size: 'md',
        },
    }
);

export interface ButtonProps
    extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> { }

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant, size, fullWidth, ...props }, ref) => {
        return (
            <button
                className={cn(buttonVariants({ variant, size, fullWidth }), className)}
                ref={ref}
                {...props}
            />
        );
    }
);

Button.displayName = 'Button';

export { Button, buttonVariants };
