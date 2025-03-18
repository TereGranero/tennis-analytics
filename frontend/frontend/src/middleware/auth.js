import { tokenService } from '../api/authConnectionService.js';

export const authMiddleware = async (to, from, next) => {
   const token = tokenService.getToken();

   if (!token) {
      next({ path: '/login', query: { redirect: to.fullPath } });

   } else {

      try {
         // Verifies if token has expired
         const payload = JSON.parse(atob(token.split('.')[1]));
         const isExpired = payload.exp * 1000 < Date.now();
         
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