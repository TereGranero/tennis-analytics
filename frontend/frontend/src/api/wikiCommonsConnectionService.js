import { httpClientWikiCommons } from './httpClients';

const wikiCommonsEndpoint = '/w/api.php';

export const getWikiCommonsImage = async (query) => {
   console.log('Requesting to WikiCommons for image...');
   const res = await httpClientWikiCommons.get(wikiCommonsEndpoint, {
      params: {
         action: 'query',
         format: 'json',
         list: 'search',
         srsearch: `${query} filetype:jpg`,  // only images
         srnamespace: 6,  // only files
         srlimit: 1,       // 1 result
         origin: '*'      // CORS
      },
   });

   if (res.data.query?.search?.length > 0) {
      const imageTitle = res.data.query.search[0].title;
      const imageUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(imageTitle)}`;
      console.log(`URL: ${imageUrl}`);
      return imageUrl;
   }
   return null;
};

