import { InputHTMLAttributes, forwardRef, useId } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className = "", label, error, id: externalId, ...props }, ref) => {
    const autoId = useId();
    const id = externalId || autoId;
    const errorId = `${id}-error`;

    return (
      <div className="space-y-1">
        <label htmlFor={id} className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          {label}
        </label>
        <input
          ref={ref}
          id={id}
          aria-invalid={!!error}
          aria-describedby={error ? errorId : undefined}
          className={`block w-full rounded-md border px-3 py-2 text-sm shadow-sm placeholder:text-gray-400 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:bg-gray-800 dark:text-gray-100 dark:placeholder:text-gray-500 ${
            error
              ? "border-red-300 text-red-900 placeholder:text-red-300 focus:border-red-500 focus:ring-red-500 dark:border-red-700 dark:text-red-300"
              : "border-gray-300 text-gray-900 dark:border-gray-700"
          } ${className}`}
          {...props}
        />
        {error && (
          <p id={errorId} className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";
export { Input };
