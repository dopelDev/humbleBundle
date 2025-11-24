import { ref } from "vue";
import { get } from "@/api/client";
import { isAxiosError } from "@/api/client";
import type { LandingPageRawData } from "@/types/rawData";

export function useRawData() {
	const rawDataList = ref<LandingPageRawData[]>([]);
	const latestRawData = ref<LandingPageRawData | null>(null);
	const currentRawData = ref<LandingPageRawData | null>(null);
	const loading = ref(false);
	const error = ref<string | null>(null);

	async function fetchRawDataList() {
		loading.value = true;
		error.value = null;
		try {
			rawDataList.value = await get<LandingPageRawData[]>(
				"/landing-page-raw-data",
			);
		} catch (err) {
			if (isAxiosError(err)) {
				if (err.response) {
					const responseData = err.response.data as
						| { detail?: string; message?: string }
						| undefined;
					error.value =
						responseData?.detail ||
						responseData?.message ||
						`Error del servidor: ${err.response.status}`;
				} else {
					error.value = err.message || "Error al obtener la lista de raw data";
				}
			} else {
				error.value =
					err instanceof Error
						? err.message
						: "Error desconocido al obtener raw data";
			}
			rawDataList.value = [];
		} finally {
			loading.value = false;
		}
	}

	async function fetchLatestRawData() {
		loading.value = true;
		error.value = null;
		try {
			latestRawData.value = await get<LandingPageRawData>(
				"/landing-page-raw-data/latest",
			);
		} catch (err) {
			if (isAxiosError(err)) {
				if (err.response) {
					const responseData = err.response.data as
						| { detail?: string; message?: string }
						| undefined;
					error.value =
						responseData?.detail ||
						responseData?.message ||
						`Error del servidor: ${err.response.status}`;
				} else {
					error.value =
						err.message || "Error al obtener el raw data más reciente";
				}
			} else {
				error.value =
					err instanceof Error
						? err.message
						: "Error desconocido al obtener raw data";
			}
			latestRawData.value = null;
		} finally {
			loading.value = false;
		}
	}

	async function fetchRawDataById(id: string) {
		loading.value = true;
		error.value = null;
		try {
			currentRawData.value = await get<LandingPageRawData>(
				`/landing-page-raw-data/${id}`,
			);
		} catch (err) {
			if (isAxiosError(err)) {
				if (err.response) {
					const responseData = err.response.data as
						| { detail?: string; message?: string }
						| undefined;
					error.value =
						responseData?.detail ||
						responseData?.message ||
						`Error del servidor: ${err.response.status}`;
				} else {
					error.value = err.message || "Error al obtener el raw data";
				}
			} else {
				error.value =
					err instanceof Error
						? err.message
						: "Error desconocido al obtener raw data";
			}
			currentRawData.value = null;
		} finally {
			loading.value = false;
		}
	}

	return {
		rawDataList,
		latestRawData,
		currentRawData,
		loading,
		error,
		fetchRawDataList,
		fetchLatestRawData,
		fetchRawDataById,
	};
}
