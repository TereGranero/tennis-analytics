export const cleanAttribution = (attribution) => {
   /* Removes some parts of Attributions in  title and author fields
      Args:
         attribution: object
      Returns:
         object: clean attribution
   */
  
   // Attribution parts to be removed
   const partsToRemove = [
      'Photographed by', 
      '(no real name)',
      'croped',
      'Crop'
   ];

   // Removes any substring like (...)
   const regexParentheses = /\([^)]*\)/g;
  
   if (attribution.author) {
      partsToRemove.forEach(part => {
         attribution.author = attribution.author.replace(part, '');
      });
      attribution.author = attribution.author.replace(regexParentheses, '').trim();
   }

   if (attribution.title) {
      partsToRemove.forEach(part => {
         attribution.title = attribution.title.replace(part, '');
      });
      attribution.title = attribution.title.replace(regexParentheses, '').trim();
   }

   return attribution;
};
 