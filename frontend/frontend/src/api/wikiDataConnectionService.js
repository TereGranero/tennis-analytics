import { httpClientWikiData } from './httpClients';
import { getImageAttribution } from './wikiCommonsConnectionService';
import { cleanAttribution } from '@/services/attribution_services';

const wikiDataEndpoint = '/w/api.php';


export const getWikiDataImage = async (wikidata_id) => {
   console.log('Requesting to WikiData for image...');
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbgetclaims',
         format: 'json',
         origin: '*',
         entity: wikidata_id,
         property: 'P18'
      },
   });

      const fileName = res.data.claims?.P18?.[0]?.mainsnak?.datavalue?.value;
      if (fileName) {
         const imageUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(fileName)}`;
         console.log(`Image URL: ${imageUrl}`);

         let imageAttribution = await getImageAttribution(fileName);
         imageAttribution = cleanAttribution(imageAttribution)

         return { imageUrl, imageAttribution };
      }

   console.log('Image URL no encontrada');
   return null;
};

// Searches entities by tournament name. Returns wikidata_id
// In the future, try to query Wikimedia Commons too
export const getWikiDataId = async (name) => {
   console.log(`Requesting to WikiData for ${name} Id...`);
   const nameLow = name.toLowerCase();
   const query = ( nameLow.includes('open') || nameLow.includes('masters') || nameLow.includes('roland') || nameLow.includes('wimbledon') )? name : `${name} open`;
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbsearchentities',
         format: 'json',
         language: 'en',
         search: query,
         type: 'item',
         limit: 5,
         origin: '*'
      },
   });


   // // Get claims for each result    NOT USED IT IS SLOW
   // const resultsWithClaims = await Promise.all(
   //    res.data.search.map(async (item) => {
   //       const entityRes = await httpClientWikiData.get(wikiDataEndpoint, {
   //          params: {
   //             action: 'wbgetentities',
   //             ids: item.id,
   //             format: 'json',
   //             origin: '*'
   //          }
   //       });
   //       return {
   //          ...item,
   //          claims: entityRes.data.entities[item.id]?.claims || {}
   //       };
   //    })
   // );

   // const tournament = resultsWithClaims.find(item => {
   //    const tennisInstance = item.claims.P31?.some(claim => 
   //       ['Q300007', 'Q13219666'].includes(claim.mainsnak.datavalue?.value.id)
   //    );
   //    const tennisDescription = item.description?.toLowerCase().includes('tennis');
   //    return tennisInstance || tennisDescription;
   // });

   const tournament = res.data.search.find(item => {
      const isTennisDescription = item.description?.toLowerCase().includes('tennis');
      return isTennisDescription;
      });
      
      if (tournament) {
      console.log(`Wikidata_id encontrado: ${tournament.id}`)
      return tournament.id;
      }
      
      console.log('Wikidata_id no encontrado')
      return null;
};


// Gets complete entity by wikidata_id and searches logo in images properties
export const getWikiDataLogo = async (wikidata_id) => {
   console.log('Requesting to WikiData for logo...');
   const res = await httpClientWikiData.get(wikiDataEndpoint, {
      params: {
         action: 'wbgetentities',
         ids: wikidata_id,
         format: 'json',
         props: 'claims',
         origin: '*'
      },
   });

   const entity = res.data.entities[wikidata_id];

   const imageProperties = ['P154', 'P2910', 'P18']; // Logo, image, icon
   let fileName;

   for (const property of imageProperties) {
      fileName = entity?.claims?.[property]?.[0]?.mainsnak?.datavalue?.value;
      if (fileName) {
         break;
      }
   }
    
   if (fileName) {

      const logoUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(fileName)}`;
      console.log(`Logo URL: ${logoUrl}`);
      
      let imageAttribution = await getImageAttribution(fileName);
      imageAttribution = cleanAttribution(imageAttribution)

      return {logoUrl, imageAttribution };
   }
   console.log('Logo URL no encontrada');
   return null;
};
