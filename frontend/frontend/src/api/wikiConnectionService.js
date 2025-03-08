import { httpClientWiki } from './httpClient';

const wikiEndpoint = '/w/api.php';

export const getWikiPlayerImage = async (wikidata_id) => {
   console.log('Requesting to Wikidata for player image...');
   const res = await httpClientWiki.get(wikiEndpoint, {
      params: {
      action: 'wbgetclaims',
      format: 'json',
      origin: '*',
      entity: wikidata_id,
      property: 'P18'
      },
   });

   if (res.data.claims && res.data.claims.P18) {
      const file_name = res.data.claims.P18[0].mainsnak.datavalue.value;
      console.log(`URL: https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file_name)}`);
      return `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file_name)}`;

   }
   return null;
};

