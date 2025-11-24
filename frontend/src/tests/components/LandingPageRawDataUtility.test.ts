import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { ref } from "vue";
import LandingPageRawDataUtility from "@/components/sections/LandingPageRawDataUtility.vue";

// Mock del composable
const mockRawDataList = ref([]);
const mockLoading = ref(false);
const mockError = ref<string | null>(null);
const mockFetchRawDataList = vi.fn();

vi.mock("@/composables/useRawData", () => ({
  useRawData: vi.fn(() => ({
    rawDataList: mockRawDataList,
    loading: mockLoading,
    error: mockError,
    fetchRawDataList: mockFetchRawDataList,
  }))
}));

describe("LandingPageRawDataUtility", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockRawDataList.value = [];
    mockError.value = null;
    mockFetchRawDataList.mockResolvedValue(undefined);
  });

  it("debería renderizar el componente", () => {
    const wrapper = mount(LandingPageRawDataUtility);
    expect(wrapper.find(".utility-card").exists()).toBe(true);
    expect(wrapper.find(".utility-title").text()).toContain("Landing Page Raw Data");
  });

  it("debería mostrar error cuando hay un error", () => {
    mockError.value = "Error de prueba";
    const wrapper = mount(LandingPageRawDataUtility);
    expect(wrapper.find(".error-message").exists()).toBe(true);
    expect(wrapper.find(".error-message").text()).toContain("Error de prueba");
  });

  it("debería mostrar lista vacía cuando no hay registros", async () => {
    mockRawDataList.value = [];
    const wrapper = mount(LandingPageRawDataUtility);
    await wrapper.vm.$nextTick();
    expect(wrapper.find(".empty-state").exists()).toBe(true);
  });
});
