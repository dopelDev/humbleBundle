import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { ref } from "vue";
import LandingPageRawDataUtility from "@/components/sections/utilities/LandingPageRawDataUtility.vue";

// Mock del composable
const mockRawDataList = ref([]);
const mockCurrentRawData = ref(null);
const mockLoading = ref(false);
const mockError = ref<string | null>(null);
const mockFetchRawDataList = vi.fn();
const mockFetchRawDataById = vi.fn();

vi.mock("@/composables/useRawData", () => ({
  useRawData: vi.fn(() => ({
    rawDataList: mockRawDataList,
    currentRawData: mockCurrentRawData,
    loading: mockLoading,
    error: mockError,
    fetchRawDataList: mockFetchRawDataList,
    fetchRawDataById: mockFetchRawDataById,
  }))
}));

describe("LandingPageRawDataUtility", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockRawDataList.value = [];
    mockCurrentRawData.value = null;
    mockLoading.value = false;
    mockError.value = null;
    mockFetchRawDataList.mockResolvedValue(undefined);
    mockFetchRawDataById.mockResolvedValue(undefined);
  });

  it("debería renderizar el componente", () => {
    const wrapper = mount(LandingPageRawDataUtility);
    expect(wrapper.find(".utility-card").exists()).toBe(true);
    expect(wrapper.find(".utility-title").text()).toContain("Landing Page Raw Data");
  });

  it("debería mostrar mensaje de carga cuando loading es true", () => {
    mockLoading.value = true;
    const wrapper = mount(LandingPageRawDataUtility);
    expect(wrapper.find(".loading").exists()).toBe(true);
    expect(wrapper.find(".loading").text()).toContain("Cargando");
  });

  it("debería mostrar error cuando hay un error", () => {
    mockError.value = "Error de prueba";
    const wrapper = mount(LandingPageRawDataUtility);
    expect(wrapper.find(".error-message").exists()).toBe(true);
    expect(wrapper.find(".error-message").text()).toContain("Error de prueba");
  });

  it("debería mostrar lista vacía cuando no hay registros", async () => {
    mockLoading.value = false;
    mockRawDataList.value = [];
    const wrapper = mount(LandingPageRawDataUtility);
    await wrapper.vm.$nextTick();
    expect(wrapper.find(".empty-state").exists()).toBe(true);
  });
});
