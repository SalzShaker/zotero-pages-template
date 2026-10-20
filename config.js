// ------------------------------------------------------------------
//  Edit this file – nothing else is needed to get started.
// ------------------------------------------------------------------
const CONFIG = {
  // Page title and the text below it
  title: "My DH bibliography",
  intro: "An annotated bibliography on … Built from my Zotero library via the Zotero API.",

  // Which library?
  //   group library:  libraryType "groups", libraryId = number in zotero.org/groups/<number>/…
  //   own library:    libraryType "users",  libraryId = your userID (zotero.org/settings/keys)
  //                   – your library must be public: zotero.org/settings/privacy → «Publish Entire Library»
  libraryType: "users",
  libraryId: "21774691",          // dh_unibe (open group of DH Bern)

  // Optional: only one collection (the 8-character key in the collection's URL), "" = whole library
  collectionKey: "BT3NCKZK",     // dh_unibe → lecture-introduction

  // Citation style (any CSL style id, e.g. "apa", "chicago-author-date", "modern-language-association")
  style: "chicago-author-date",

  // Group the list: "none", "year", "type" or "tag"
  groupBy: "year",

  // Show child notes from Zotero below each entry (your annotations!)
  showNotes: true,

  // Safety net: stop after this many items (the API sends 100 per request)
  maxItems: 500
};
// NEVER put an API key in this file – everything here is public.
