/**
 * Formatea un tamaño en bytes a una representación legible
 */
export function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

/**
 * Formatea el tamaño de un string JSON
 */
export function formatJsonSize(json: string): string {
  const bytes = new Blob([json]).size;
  return formatSize(bytes);
}
