export interface DateFormatOptions {
  includeTime?: boolean;
  includeSeconds?: boolean;
  format?: 'short' | 'long' | 'datetime';
  locale?: string;
}

/**
 * Formatea una fecha según el locale proporcionado o por defecto
 */
export function formatDate(
  dateString: string | undefined | null,
  options: DateFormatOptions = {}
): string {
  if (!dateString) return '—';

  const date = new Date(dateString);
  const dateLocale = options.locale === 'es' ? 'es-ES' : 'en-US';

  const {
    includeTime = true,
    includeSeconds = false,
    format = 'datetime',
  } = options;

  if (format === 'short') {
    return date.toLocaleDateString(dateLocale, {
      month: 'short',
      day: 'numeric',
    });
  }

  if (format === 'long') {
    return date.toLocaleDateString(dateLocale, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  }

  // datetime format (default)
  const formatOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  };

  if (includeTime) {
    formatOptions.hour = '2-digit';
    formatOptions.minute = '2-digit';
  }

  if (includeSeconds) {
    formatOptions.second = '2-digit';
  }

  return date.toLocaleString(dateLocale, formatOptions);
}
