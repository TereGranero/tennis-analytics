import { httpClientNews } from './httpClient';

// GET https://newsapi.org/v2/everything?q=bitcoin&apiKey=67f0427492e14efd9231262983d61fe9

const NEWS_API_KEY = "67f0427492e14efd9231262983d61fe9"; //developer 
const newsEndpoint = '/v2/everything';
const sourcesEndpoint = '/v2/top-headlines/sources'

export const getTennisNews = async (sources) => {
   const res = await httpClientNews.get(newsEndpoint, {
      params: {
         q: 'tennis',
         sources: sources,
         language: 'es',
         sortBy: 'popularity',
         apiKey: NEWS_API_KEY
      }
   });

   return res.data;
}


//GET https://newsapi.org/v2/top-headlines/sources?country=usapiKey=API_KEY

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





