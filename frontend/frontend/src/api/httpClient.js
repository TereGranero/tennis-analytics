import axios from 'axios';

// ---------- Backend Server API ------------

const httpClient = axios.create({
   baseURL: 'http://127.0.0.1:5000', 
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

export { httpClient, httpClientWikiData, httpClientNews, httpClientWikiCommons }; 