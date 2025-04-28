import { tokenService } from '../api/authConnectionService.js';

export const authMiddleware = async (to, from, next) => {
   const token = tokenService.getToken();

   // Redirects to login if no token and saves destination page to redirect after successful login
   if (!token) {
      next({ path: '/login', query: { redirect: to.fullPath } });

   } else {

      try {
         // Verifies if token has expired
         // JWT = header.payload.signature
         // payload.exp is expiration time in seconds
         const payload = JSON.parse(atob(token.split('.')[1]));
         const isExpired = payload.exp * 1000 < Date.now();  //now is miliseconds
         
         if (isExpired) {
            // Deletes expired token
            tokenService.logout(); 
            next({ path: '/login', query: { redirect: to.fullPath } });

         } else {
            next();
         }

      } catch (err) {
         console.error('Error Token Verification:', err);
         tokenService.logout();
         next({ path: '/login', query: { redirect: to.fullPath } });
      }
   }
};