import axios from 'axios';

// ---------- Backend Server API ------------

const httpClient = axios.create({
   baseURL: process.env.VUE_APP_API_URL, 
   timeout: 15000,                              
   headers: {
      'Content-Type': 'application/json',
   },
});

httpClient.interceptors.response.use(
   response => response,
   error => {
      console.error(`Server Error: ${error}`);
      return Promise.reject(error);
   }
);

// ---------- Backend Server API with authentication ------------

const httpAuthClient = axios.create({
   baseURL: process.env.VUE_APP_API_URL, 
   timeout: 15000,                              
   headers: {
      'Content-Type': 'application/json',
   },
});

// Adds token for requests
httpAuthClient.interceptors.request.use( 
   config => {
      const token = localStorage.getItem('token');
      if (token) {
         config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
   },
   error => {
      console.error(`Server Authentication Error: ${error}`);
      return Promise.reject(error);
   }
);

httpAuthClient.interceptors.response.use(
   response => response,
   error => {
      console.error(`Server Error: ${error}`);
      return Promise.reject(error);
   }
);

// -------------- Wikidata API ----------------

const httpClientWikiData = axios.create({
   baseURL: 'https://www.wikidata.org', 
   timeout: 5000,                              
   headers: {
      'Content-Type': 'application/json',
   },
});

httpClientWikiData.interceptors.response.use(
   response => response,
   error => {
      console.error(`WikiDataServer Error: ${error}`);
      return Promise.reject(error);
   }
);


// --------------- News API --------------------

const httpClientNews = axios.create({
   baseURL: 'https://newsapi.org', 
   timeout: 5000,                              
   headers: {
      'Content-Type': 'application/json',
   },
});

httpClientNews.interceptors.response.use(
   response => response,
   error => {
      console.error(`NewsServer Error: ${error}`);
      return Promise.reject(error);
   }
);


// --------------- WikiCommons API --------------------

const httpClientWikiCommons = axios.create({
   baseURL: 'https://commons.wikimedia.org', 
   timeout: 5000,                              
   headers: {
      'Content-Type': 'application/json',
   },
});

httpClientNews.interceptors.response.use(
   response => response,
   error => {
      console.error(`WikiCommonsServer Error: ${error}`);
      return Promise.reject(error);
   }
);

export { 
   httpClient, 
   httpAuthClient, 
   httpClientWikiData, 
   httpClientNews, 
   httpClientWikiCommons 
}; 