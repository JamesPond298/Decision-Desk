/* Public configuration only. Never place AP or DDHQ API keys in this file. */
window.DECISION_DESK_CONFIG = {
  // HTTPS endpoint for a secure server-side relay. The relay keeps vendor keys private
  // and returns { rows: [...] } in the normalized election-results shape.
  liveEndpoint: ""
};
