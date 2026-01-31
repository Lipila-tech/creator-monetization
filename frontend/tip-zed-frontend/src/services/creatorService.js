import api from "./api";

export const creatorService = {
  // Fetch all creators for the catalog page
  getAllCreators: async () => {
    try {
      const response = await api.get("/creators/all/"); 
      return response.data; // Expecting { status: "success", data: [...] }
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  // Fetch a single creator by their URL slug
  getCreatorBySlug: async (slug) => {
    try {
      const response = await api.get(`/creators/${slug}/`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};