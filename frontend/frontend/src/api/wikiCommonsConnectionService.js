import { httpClientWikiCommons } from './httpClients';
import { cleanAttribution } from '@/services/attribution_services';

// Connects to Wikimedia Commons to retrieve images and their metadata

const wikiCommonsEndpoint = '/w/api.php';

// Searches jpg image by a query
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
      const filtered = res.data.query.search.filter(img => !img.title.includes('vs'));

      if (filtered.length === 0) {
         console.log('No results found without "vs".');
         return null;
      }

      const imageTitle = filtered[0].title;
      const imageUrl = `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(imageTitle)}`;
      console.log(`URL: ${imageUrl}`);

      const fileName = imageTitle.replace(/^File:/, '');
      let imageAttribution = await getImageAttribution(fileName);
      imageAttribution = cleanAttribution(imageAttribution)

      return { imageUrl, imageAttribution };
   }

   console.log(`Image URL not found for query: ${query}.`);
   return null;
};

// Retrieves metadata from image for attribution
export const getImageAttribution = async (fileName) => {
   console.log(`Requesting to WikiCommons for attribution...`);
   const res = await httpClientWikiCommons.get(wikiCommonsEndpoint, {
      params: {
         action: 'query',
         format: 'json',
         titles: `File:${fileName}`,
         prop: 'imageinfo',
         iiprop: 'url|extmetadata',
         origin: '*'
      },
   });

   const pages = res.data.query?.pages;
   const imageInfo = Object.values(pages)[0]?.imageinfo?.[0];

   if (imageInfo) {
      const metadata = imageInfo.extmetadata;
      const title = metadata?.ObjectName?.value || '';
      const author = metadata?.Artist?.value || '';
      const license = metadata?.LicenseShortName?.value || '';
      const licenseUrl = metadata?.LicenseUrl?.value || '#';
      const description = metadata?.ImageDescription?.value || '';

      return {
         title,
         author,
         license,
         licenseUrl,
         description,
         filePageUrl: imageInfo.descriptionurl // Commons url
      };
   }

   return null;
};


