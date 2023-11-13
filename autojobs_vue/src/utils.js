export function parseJwt(token) {
  if (typeof token !== 'string') {
    console.error('Token não é uma string válida:', token);
    return null;  // ou lance um erro, dependendo do comportamento desejado
  }

  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));

  return JSON.parse(jsonPayload);
}
