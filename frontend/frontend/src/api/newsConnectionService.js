import { httpClientNews } from './httpClients';

// GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=APIKEY

const NEWS_API_KEY = process.env.VUE_APP_NEWS_API_KEY;
// THIS KEY IS NOT SAFE. REQUESTS SHOULD BE DONE FROM BACKEND

const newsEndpoint = '/v2/everything';
const sourcesEndpoint = '/v2/top-headlines/sources'

// Last month
const today = new Date();
const lastMonth = new Date();
lastMonth.setMonth(today.getMonth() - 1);

// Formats 'YYYY-MM-DD'
const from = lastMonth.toISOString().split('T')[0];
const to = today.toISOString().split('T')[0];

export const getTennisNews = async (sources) => {
   const res = await httpClientNews.get(newsEndpoint, {
      params: {
         q: 'tennis',
         sources: sources,
         language: 'es',
         sortBy: 'popularity',
         apiKey: NEWS_API_KEY,
         from: from, // a month ago
         to: to // today
      }
   });

   return res.data;
}


//GET https://newsapi.org/v2/top-headlines/sources?country=us&apiKey=API_KEY

export const getSourcesForTennisNews = async () => {
   const res = await httpClientNews.get(sourcesEndpoint, {
      params: {
         language: 'es',
         category: 'sports',
         apiKey: NEWS_API_KEY
      }
   });
   
   return res.data;
}





