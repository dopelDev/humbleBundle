import { ref, computed, onMounted } from "vue";
import type { Bundle } from "@/types/bundle";
import { get, postLong, isAxiosError } from "@api/client";

interface ETLRunResponse {
  bundles_processed: number;
  cleanup_ran: boolean;
  images_downloaded: number;
  bundle_images_downloaded: number;
  book_images_downloaded: number;
  images_info: Array<{
    url?: string;
    path?: string;
    category?: string;
    identifier?: string;
    cached?: boolean;
  }>;
}

export function useBundles() {
  const bundles = ref<Bundle[]>([]);
  const featured = ref<Bundle | null>(null);
  const loading = ref(true);
  const error = ref<string | null>(null);
  const lastUpdate = ref<Date | null>(null);
  const etlResult = ref<ETLRunResponse | null>(null);

  const activeBundles = computed(() =>
    bundles.value.filter((bundle) => bundle.is_active),
  );

  const fetchData = async () => {
    loading.value = true;
    error.value = null;
    try {
      const [all, feat] = await Promise.all([
        get<Bundle[]>("/bundles"),
        get<Bundle>("/bundles/featured"),
      ]);
      bundles.value = all;
      featured.value = feat;
      
      // Obtener la fecha de verificación más reciente
      const allDates = [
        ...all.map(b => b.verification_date).filter(Boolean) as string[],
        feat?.verification_date
      ].filter(Boolean) as string[];
      
      if (allDates.length > 0) {
        const dates = allDates.map(d => new Date(d));
        lastUpdate.value = new Date(Math.max(...dates.map(d => d.getTime())));
      }
    } catch (err) {
      error.value =
        err instanceof Error ? err.message : "No se pudo cargar la data.";
    } finally {
      loading.value = false;
    }
  };

  const runETL = async () => {
    loading.value = true;
    error.value = null;
    etlResult.value = null;
    try {
      // Ejecutar el ETL con timeout extendido
      const result = await postLong<ETLRunResponse>("/etl/run", {});
      etlResult.value = result;
      
      // Recargar los datos después del ETL
      await fetchData();
    } catch (err) {
      console.error("Error ejecutando ETL:", err);
      if (isAxiosError(err)) {
        if (err.code === 'ECONNABORTED') {
          error.value = "El ETL está tardando demasiado. Por favor, intenta de nuevo.";
        } else if (err.response) {
          // El servidor respondió con un código de error
          const responseData = err.response.data as { detail?: string; message?: string } | undefined;
          error.value = responseData?.detail || responseData?.message || `Error del servidor: ${err.response.status}`;
        } else if (err.request) {
          // La solicitud se hizo pero no hubo respuesta
          error.value = "No se pudo conectar con el servidor. Verifica que el API esté corriendo.";
        } else {
          error.value = err.message || "Error desconocido al ejecutar ETL.";
        }
      } else {
        error.value =
          err instanceof Error ? err.message : "Error ejecutando ETL.";
      }
    } finally {
      loading.value = false;
    }
  };

  onMounted(fetchData);

  return {
    bundles,
    featured,
    loading,
    error,
    activeBundles,
    lastUpdate,
    etlResult,
    refresh: fetchData,
    runETL,
  };
}

