export default {
  'api:follow-detail': id => `/api/follows/${id}/`,
  'api:follow-list': () => '/api/follows/',
  'api:identity-detail': id => `/api/identities/${id}/`,
  'api:identity-list': () => '/api/identities/',
  'api:identity-reorder': () => '/api/identities/reorder/',
};
