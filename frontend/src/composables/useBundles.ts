import { ref, computed, onMounted } from "vue";
import type { Bundle } from "@/types/bundle";
import { get, postLong, isAxiosError } from "@api/client";
import { useAuth } from "@composables/useAuth";

interface ETLRunResponse {
  bundles_processed: number;
  cleanup_ran: boolean;
}

export function useBundles() {
  const bundles = ref<Bundle[]>([]);
  const featured = ref<Bundle | null>(null);
  const loading = ref(true);
  const error = ref<string | null>(null);
  const lastUpdate = ref<Date | null>(null);
  const etlResult = ref<ETLRunResponse | null>(null);
  const auth = useAuth();

  const activeBundles = computed(() =>
    bundles.value.filter((bundle) => bundle.is_active),
  );

  const fetchData = async () => {
    loading.value = true;
    error.value = null;
    try {
      // Cargar bundles primero
      const all = await get<Bundle[]>("/bundles");
      bundles.value = all;
      
      // Intentar cargar featured, pero no fallar si no existe (404)
      try {
        const feat = await get<Bundle>("/bundles/featured");
        featured.value = feat;
      } catch (featErr) {
        // Si es 404, simplemente no hay featured bundle (es normal si no hay bundles)
        if (isAxiosError(featErr) && featErr.response?.status === 404) {
          featured.value = null;
        } else {
          // Si es otro error, loguearlo pero no romper la carga
          console.warn("Error cargando featured bundle:", featErr);
          featured.value = null;
        }
      }
      
      // Obtener la fecha de verificación más reciente
      const allDates = [
        ...all.map(b => b.verification_date).filter(Boolean) as string[],
        featured.value?.verification_date
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
    if (!auth.isAuthenticated.value) {
      error.value = "Debes iniciar sesión para ejecutar el ETL.";
      return;
    }
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
