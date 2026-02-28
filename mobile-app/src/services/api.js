import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const DEFAULT_API_URL = 'http://10.0.2.2:8000'; // Android emulator localhost

const getApiUrl = async () => {
  const stored = await AsyncStorage.getItem('api_url');
  return stored || DEFAULT_API_URL;
};

const api = {
  async analyze(text, categories = ['Policy', 'Technology', 'Economics', 'Social']) {
    const baseUrl = await getApiUrl();
    const response = await axios.post(`${baseUrl}/analyze`, { text, categories });
    return response.data;
  },

  async summarize(text, maxLength = 150) {
    const baseUrl = await getApiUrl();
    const response = await axios.post(`${baseUrl}/summarize`, { text, max_length: maxLength });
    return response.data;
  },

  async compare(textA, textB) {
    const baseUrl = await getApiUrl();
    const response = await axios.post(`${baseUrl}/compare`, { text_a: textA, text_b: textB });
    return response.data;
  },

  async search(query, topK = 5) {
    const baseUrl = await getApiUrl();
    const response = await axios.post(`${baseUrl}/search`, { query, top_k: topK });
    return response.data;
  },

  async healthCheck() {
    const baseUrl = await getApiUrl();
    const response = await axios.get(`${baseUrl}/`);
    return response.data;
  },
};

export default api;
